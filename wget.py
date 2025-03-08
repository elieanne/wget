import os
import argparse
import time
import subprocess
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
from tqdm import tqdm
import requests

# Function to download a single file
def download_file(url, output_path=None, directory=None, rate_limit=None):
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"start at {start_time}")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        print(f"sending request, awaiting response... status {response.status_code} {response.reason}")

        file_size = int(response.headers.get('content-length', 0))
        print(f"content size: {file_size} bytes [~{file_size / 1024 / 1024:.2f} MB]")

        if directory:
            os.makedirs(directory, exist_ok=True)
            output_path = os.path.join(directory, output_path or os.path.basename(url))
        else:
            output_path = output_path or os.path.basename(url)

        print(f"saving file to: {output_path}")

        progress = tqdm(total=file_size, unit='B', unit_scale=True, desc=output_path)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    progress.update(len(chunk))
                    if rate_limit:
                        time.sleep(len(chunk) / (rate_limit * 1024))
        progress.close()

        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Downloaded [{url}]")
        print(f"finished at {end_time}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Function to download in the background
def background_download(url, output_path=None, directory=None, rate_limit=None):
    log_file = "wget-log"
    with open(log_file, 'w') as log:
        subprocess.Popen(
            ["python3", __file__, url] +
            (["-O", output_path] if output_path else []) +
            (["-P", directory] if directory else []) +
            (["--rate-limit", str(rate_limit)] if rate_limit else []),
            stdout=log, stderr=log
        )
    print(f"Output will be written to '{log_file}'.")

# Function to download multiple files asynchronously
async def async_download_file(session, url, output_path=None, directory=None):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            file_size = int(response.headers.get('content-length', 0))

            if directory:
                os.makedirs(directory, exist_ok=True)
                output_path = os.path.join(directory, output_path or os.path.basename(url))
            else:
                output_path = output_path or os.path.basename(url)

            with open(output_path, 'wb') as f:
                async for chunk in response.content.iter_chunked(1024):
                    f.write(chunk)

            print(f"Downloaded [{url}] to [{output_path}]")

    except aiohttp.ClientError as e:
        print(f"Error downloading {url}: {e}")

async def download_multiple_files(urls, output_paths=None, directories=None):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls):
            output_path = output_paths[i] if output_paths else None
            directory = directories[i] if directories else None
            tasks.append(async_download_file(session, url, output_path, directory))
        await asyncio.gather(*tasks)

# Function to mirror a website
async def mirror_website(session, url, base_url, visited, reject=None, exclude=None, convert_links=False):
    if url in visited:
        return
    visited.add(url)

    try:
        async with session.get(url) as response:
            if response.status == 404:
                print(f"404 error: The file or directory does not exist at {url}")
                return

            response.raise_for_status()
            content = await response.text()

            soup = BeautifulSoup(content, 'html.parser')
            for tag in soup.find_all(['a', 'link', 'img', 'script']):
                if tag.name == 'a' and 'href' in tag.attrs:
                    link = urllib.parse.urljoin(base_url, tag['href'])
                    if not any(link.endswith(ext) for ext in (reject or [])) and not any(link.startswith(ex) for ex in (exclude or [])):
                        await mirror_website(session, link, base_url, visited, reject, exclude, convert_links)
                elif tag.name == 'link' and 'href' in tag.attrs:
                    link = urllib.parse.urljoin(base_url, tag['href'])
                    if not any(link.endswith(ext) for ext in (reject or [])) and not any(link.startswith(ex) for ex in (exclude or [])):
                        await mirror_website(session, link, base_url, visited, reject, exclude, convert_links)
                elif tag.name == 'img' and 'src' in tag.attrs:
                    link = urllib.parse.urljoin(base_url, tag['src'])
                    if not any(link.endswith(ext) for ext in (reject or [])) and not any(link.startswith(ex) for ex in (exclude or [])):
                        await async_download_file(session, link, directory=os.path.dirname(url))
                elif tag.name == 'script' and 'src' in tag.attrs:
                    link = urllib.parse.urljoin(base_url, tag['src'])
                    if not any(link.endswith(ext) for ext in (reject or [])) and not any(link.startswith(ex) for ex in (exclude or [])):
                        await async_download_file(session, link, directory=os.path.dirname(url))

            if convert_links:
                for tag in soup.find_all(['a', 'link', 'img', 'script']):
                    if tag.name == 'a' and 'href' in tag.attrs:
                        tag['href'] = urllib.parse.urljoin(base_url, tag['href'])
                    elif tag.name == 'link' and 'href' in tag.attrs:
                        tag['href'] = urllib.parse.urljoin(base_url, tag['href'])
                    elif tag.name == 'img' and 'src' in tag.attrs:
                        tag['src'] = urllib.parse.urljoin(base_url, tag['src'])
                    elif tag.name == 'script' and 'src' in tag.attrs:
                        tag['src'] = urllib.parse.urljoin(base_url, tag['src'])

            # Handle empty paths
            parsed_url = urllib.parse.urlparse(url)
            output_path = parsed_url.path.lstrip('/')
            if not output_path:
                output_path = 'index.html'
            else:
                # Ensure the path ends with .html if it doesn't have an extension
                if not os.path.splitext(output_path)[1]:
                    output_path = os.path.join(output_path, 'index.html')

            # Create directories if they don't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

    except aiohttp.ClientError as e:
        print(f"Error mirroring {url}: {e}")
    except Exception as e:
        print(f"Unexpected error while mirroring {url}: {e}")

async def mirror(url, reject=None, exclude=None, convert_links=False):
    async with aiohttp.ClientSession() as session:
        visited = set()
        await mirror_website(session, url, url, visited, reject, exclude, convert_links)

# Main function
def main():
    parser = argparse.ArgumentParser(description="A simple wget clone in Python")
    parser.add_argument('url', nargs='?', help="URL of the file to download")
    parser.add_argument('-O', '--output', help="Save the file with a different name")
    parser.add_argument('-P', '--directory', help="Save the file to a specific directory")
    parser.add_argument('--rate-limit', help="Limit the download speed (e.g., 200k, 2M)")
    parser.add_argument('-B', '--background', action='store_true', help="Download in the background")
    parser.add_argument('-i', '--input-file', help="File containing multiple URLs to download")
    parser.add_argument('--mirror', action='store_true', help="Mirror a website")
    parser.add_argument('-R', '--reject', help="Comma-separated list of file suffixes to reject")
    parser.add_argument('-X', '--exclude', help="Comma-separated list of directories to exclude")
    parser.add_argument('--convert-links', action='store_true', help="Convert links for offline viewing")
    args = parser.parse_args()

    if args.mirror:
        reject = args.reject.split(',') if args.reject else None
        exclude = args.exclude.split(',') if args.exclude else None
        asyncio.run(mirror(args.url, reject, exclude, args.convert_links))
    elif args.input_file:
        with open(args.input_file, 'r') as f:
            urls = f.read().splitlines()
        asyncio.run(download_multiple_files(urls))
    else:
        if args.background:
            background_download(args.url, args.output, args.directory, args.rate_limit)
        else:
            rate_limit = None
            if args.rate_limit:
                rate_limit = float(args.rate_limit[:-1]) * (1024 if args.rate_limit[-1].lower() == 'k' else 1024 * 1024)

            download_file(args.url, args.output, args.directory, rate_limit)

if __name__ == "__main__":
    main()
