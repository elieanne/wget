# WGET
# français
Objectifs
L'objectif de ce projet consiste à recréer certaines fonctionnalités en wgetutilisant un langage compilé de votre choix (comme C, Rust, Go ou autre).

Ces fonctionnalités consisteront en :

L'utilisation normale de wget: télécharger un fichier à partir d'une URL, exemple :wget https://some_url.ogr/file.zip
Télécharger un seul fichier et l'enregistrer sous un nom différent
Téléchargement et enregistrement du fichier dans un répertoire spécifique
Définissez la vitesse de téléchargement, en limitant la vitesse d'un téléchargement
Téléchargement d'un fichier en arrière-plan
Téléchargement de plusieurs fichiers en même temps, en lisant un fichier contenant plusieurs liens de téléchargement de manière asynchrone
La fonctionnalité principale sera de télécharger un site Web entier, en reflétant un site Web
Introduction
Wget est un utilitaire gratuit permettant le téléchargement non interactif de fichiers depuis le Web. Il prend en charge les protocoles HTTP, HTTPS et FTP, ainsi que la récupération via des proxys HTTP.

Pour en savoir plus sur wget, vous pouvez visiter le manuel en utilisant la commande man wget, ou vous pouvez visiter le site Web ici .

Usage
Votre programme doit avoir comme arguments le lien à partir duquel vous souhaitez télécharger le fichier, par exemple :

$ go run . https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
Le programme devrait être capable de donner un retour d'information, en affichant :

Heure de démarrage du programme : elle doit avoir le format suivant aaaa-mm-jj hh:mm:ss
Statut de la requête. Pour que le programme puisse procéder au téléchargement, il doit répondre à la requête par le statut OK ( 200 OK). Dans le cas contraire, il doit indiquer le statut obtenu et terminer l'opération par un avertissement d'erreur.
Taille du contenu téléchargé : la longueur du contenu peut être présentée brute (octets) et arrondie à Mo ou Go en fonction de la taille du fichier téléchargé
Nom et chemin du fichier qui est sur le point d'être enregistré
Une barre de progression, comportant les éléments suivants :
Une quantité de KiBou MiB(selon la taille du téléchargement) qui a été téléchargée
Un pourcentage de la quantité téléchargée
Temps restant pour terminer le téléchargement
Heure à laquelle le téléchargement s'est terminé en respectant le format précédent
Cela devrait ressembler à quelque chose comme ça

$ go run . https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
start at 2017-10-14 03:46:06
sending request, awaiting response... status 200 OK
content size: 56370 [~0.06MB]
saving file to: ./EMtmPFLWkAA8CIS.jpg
 55.05 KiB / 55.05 KiB [================================================================================================================] 100.00% 1.24 MiB/s 0s

Downloaded [https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg]
finished at 2017-10-14 03:46:07
Drapeaux
Votre programme devrait être capable de gérer différents indicateurs.

L'indicateur -Bdoit être géré : il doit télécharger immédiatement un fichier en arrière-plan et la sortie doit être redirigée vers un fichier journal. À l'exécution du programme contenant cet indicateur, il doit afficher : Output will be written to "wget-log". Exemple :
$ go run . -B https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
Output will be written to "wget-log".
$ cat wget-log
start at 2017-10-14 03:46:06
sending request, awaiting response... status 200 OK
content size: 56370 [~0.06MB]
saving file to: ./EMtmPFLWkAA8CIS.jpg
Downloaded [https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg]
finished at 2017-10-14 03:46:07
$
Téléchargez un fichier et enregistrez-le sous un nom différent en utilisant le drapeau -Osuivi du nom sous lequel vous souhaitez enregistrer le fichier, exemple :
$ go run . -O=meme.jpg https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
start at 2017-10-14 03:46:06
sending request, awaiting response... status 200 OK
content size: 56370 [~0.06MB]
saving file to: ./meme.jpg
 55.05 KiB / 55.05 KiB [================================================================================================================] 100.00% 1.24 MiB/s 0s

Downloaded [https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg]
finished at 2017-10-14 03:46:07
$ ls -l
-rw-r--r-- 1 student student 56370 ago 13 16:59 meme.jpg
-rw-r--r-- 1 student student 11489 ago 13 10:28 main.go
Il doit également gérer le chemin vers lequel votre fichier va être enregistré en utilisant l'indicateur -Psuivi du chemin vers lequel vous souhaitez enregistrer le fichier, par exemple :
$ go run . -P=~/Downloads/ -O=meme.jpg https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
start at 2017-10-14 03:46:06
sending request, awaiting response... status 200 OK
content size: 56370 [~0.06MB]
saving file to: ~/Downloads/meme.jpg
 55.05 KiB / 55.05 KiB [================================================================================================================] 100.00% 1.24 MiB/s 0s

Downloaded [https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg]
finished at 2017-10-14 03:46:07
$ ls -l ~/Downloads/meme.jpg
-rw-r--r-- 1 student student 56370 ago 13 16:59 /home/student/Downloads/meme.jpg
Le programme doit gérer la limitation de vitesse. Il peut contrôler la vitesse de téléchargement grâce à l'indicateur --rate-limit. Si vous téléchargez un fichier volumineux, vous pouvez limiter la vitesse de téléchargement, empêchant ainsi le programme d'utiliser toute la bande passante de votre connexion. Exemple :
$ go run . --rate-limit=400k https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
Cet indicateur doit accepter différents types de valeurs, par exemple : k et M. Vous pouvez donc définir la limite de débit comme rate-limit=200kourate-limit=2M

Le téléchargement de différents fichiers doit être possible. Pour cela, le programme recevra l' -iindicateur suivi d'un nom de fichier contenant tous les liens à télécharger. Exemple :
$ ls
download.txt   main.go
$ cat download.txt
https://assets.01-edu.org/wgetDataSamples/20MB.zip
https://assets.01-edu.org/wgetDataSamples/Image_10MB.zip
$ go run . -i=download.txt
content size: [10485760, 20971520]
finished 10MB.zip
finished 20MB.zip

Download finished:  [https://assets.01-edu.org/wgetDataSamples/20MB.zip https://assets.01-edu.org/wgetDataSamples/Image_10MB.zip]

Les téléchargements doivent fonctionner de manière asynchrone : les deux fichiers doivent être téléchargés simultanément. Vous êtes libre d'afficher ce que vous souhaitez pour cette option.

Dupliquez un site web . Cette option permet de télécharger l'intégralité du site web, permettant ainsi d'utiliser une partie du site hors ligne et pour d'autres raisons utiles . Pour cela, vous devrez télécharger le système de fichiers du site web et l'enregistrer dans un dossier portant le nom de domaine. Exemple :http://www.example.com, sera stocké dans un dossier portant le nomwww.example.comcontenant tous les fichiers du site web dupliqué. L'option doit être--mirror.
Par défaut, l'indicateur récupère et analyse le code HTML ou CSS de l'URL donnée. Il récupère ainsi les fichiers auxquels le document fait référence via des balises. Les balises utilisées pour cette récupération doivent être a, linket imgcontenir les attributs hrefet src.

Vous devrez implémenter certains indicateurs facultatifs pour accompagner l' --mirrorindicateur.

Ces indicateurs fonctionneront en fonction des liens « Suivre » . La commande wgetdispose de plusieurs mécanismes permettant d'affiner le suivi des liens. Pour ce projet, vous devrez implémenter le comportement de (notez que ces indicateurs seront utilisés conjointement avec l' --mirrorindicateur) :

Types de fichiers ( --rejecten abrégé -R)
ce drapeau aura une liste de suffixes de fichiers que le programme évitera de télécharger lors de la récupération

exemple:

$ go run . --mirror -R=jpg,gif https://example.com
Limites basées sur le répertoire ( --excludeen abrégé -X)
Cet indicateur affichera une liste de chemins que le programme évitera de suivre et de récupérer. Ainsi, si l'URL est https://example.comet les répertoires sont /js, /cssvous /assetspouvez éviter tout chemin en utilisant -X=/js,/assets. Le système de fichiers n'aura alors plus que /css.

exemple:

$ go run . --mirror -X=/assets,/css https://example.com
Convertir les liens pour une visualisation hors ligne ( --convert-links)
cet indicateur convertira les liens dans les fichiers téléchargés afin qu'ils puissent être consultés hors ligne, en les modifiant pour pointer vers les ressources téléchargées localement au lieu des URL d'origine.

exemple:

$ go run . --mirror --convert-links https://example.com
Indice
Vous pouvez consulter le package HTML pour obtenir de l'aide.
Essayez les indicateurs réels de la commande wget pour mieux comprendre leur utilisation.

Ce projet vous aidera à en apprendre davantage sur :

GNU Wget
HTTP
FTP
Algorithmes (récursivité)
Sites Web miroirs
Suivre les liens
Système de fichiers (fs)

# anglais
Objectives
This project objective consists on recreating some functionalities of wget using a compiled language of your choice (like C, Rust, Go or other).

These functionalities will consist in:

The normal usage of wget: downloading a file given an URL, example: wget https://some_url.ogr/file.zip
Downloading a single file and saving it under a different name
Downloading and saving the file in a specific directory
Set the download speed, limiting the rate speed of a download
Downloading a file in background
Downloading multiple files at the same time, by reading a file containing multiple download links asynchronously
Main feature will be to download an entire website, mirroring a website
Introduction
Wget is a free utility for non-interactive download of files from the Web. It supports HTTP, HTTPS, and FTP protocols, as well as retrieval through HTTP proxies.

To see more about wget you can visit the manual by using the command man wget, or you can visit the website here.

Usage
Your program must have as arguments the link from where you want to download the file, for instance:

$ go run . https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
The program should be able to give feedback, displaying the:

Time that the program started: it must have the following format yyyy-mm-dd hh:mm:ss
Status of the request. For the program to proceed to the download, it must present a response to the request as status OK (200 OK) if not, it should say which status it got and finish the operation with an error warning
Size of the content downloaded: the content length can be presented as raw (bytes) and rounded to Mb or Gb depending on the size of the file downloaded
Name and path of the file that is about to be saved
A progress bar, having the following:
A amount of KiB or MiB (depending on the download size) that was downloaded
A percentage of how much was downloaded
Time that remains to finish the download
Time that the download finished respecting the previous format
It should look something like this

$ go run . https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
start at 2017-10-14 03:46:06
sending request, awaiting response... status 200 OK
content size: 56370 [~0.06MB]
saving file to: ./EMtmPFLWkAA8CIS.jpg
 55.05 KiB / 55.05 KiB [================================================================================================================] 100.00% 1.24 MiB/s 0s

Downloaded [https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg]
finished at 2017-10-14 03:46:07
Flags
Your program should be able to handle different flags.

The flag -B should be handled, this flag should download a file immediately to the background and the output should be redirected to a log file. When the program containing this flag is executed it should output : Output will be written to "wget-log". Example:
$ go run . -B https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
Output will be written to "wget-log".
$ cat wget-log
start at 2017-10-14 03:46:06
sending request, awaiting response... status 200 OK
content size: 56370 [~0.06MB]
saving file to: ./EMtmPFLWkAA8CIS.jpg
Downloaded [https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg]
finished at 2017-10-14 03:46:07
$
Download a file and save it under a different name by using the flag -O followed by the name you wish to save the file, example:
$ go run . -O=meme.jpg https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
start at 2017-10-14 03:46:06
sending request, awaiting response... status 200 OK
content size: 56370 [~0.06MB]
saving file to: ./meme.jpg
 55.05 KiB / 55.05 KiB [================================================================================================================] 100.00% 1.24 MiB/s 0s

Downloaded [https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg]
finished at 2017-10-14 03:46:07
$ ls -l
-rw-r--r-- 1 student student 56370 ago 13 16:59 meme.jpg
-rw-r--r-- 1 student student 11489 ago 13 10:28 main.go
It should also handle the path to where your file is going to be saved using the flag -P followed by the path to where you want to save the file, example:
$ go run . -P=~/Downloads/ -O=meme.jpg https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
start at 2017-10-14 03:46:06
sending request, awaiting response... status 200 OK
content size: 56370 [~0.06MB]
saving file to: ~/Downloads/meme.jpg
 55.05 KiB / 55.05 KiB [================================================================================================================] 100.00% 1.24 MiB/s 0s

Downloaded [https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg]
finished at 2017-10-14 03:46:07
$ ls -l ~/Downloads/meme.jpg
-rw-r--r-- 1 student student 56370 ago 13 16:59 /home/student/Downloads/meme.jpg
The program should handle speed limit. Basically the program can control the speed of the download by using the flag --rate-limit. If you download a huge file you can limit the speed of your download, preventing the program from using the full possible bandwidth of your connection, example:
$ go run . --rate-limit=400k https://pbs.twimg.com/media/EMtmPFLWkAA8CIS.jpg
This flag should accept different value types, example: k and M. So you can put the rate limit as rate-limit=200k or rate-limit=2M

Downloading different files should be possible. For this the program will receive the -i flag followed by a file name that will contain all links that are to be downloaded. Example:
$ ls
download.txt   main.go
$ cat download.txt
https://assets.01-edu.org/wgetDataSamples/20MB.zip
https://assets.01-edu.org/wgetDataSamples/Image_10MB.zip
$ go run . -i=download.txt
content size: [10485760, 20971520]
finished 10MB.zip
finished 20MB.zip

Download finished:  [https://assets.01-edu.org/wgetDataSamples/20MB.zip https://assets.01-edu.org/wgetDataSamples/Image_10MB.zip]

The Downloads should work asynchronously, it should download both files at the same time. You are free to display what you want for this option.

Mirror a website. This option should download the entire website being possible to use "part" of the website offline and for other useful reasons. For this you will have to download the website file system and save it into a folder that will have the domain name. Example: http://www.example.com, will be stored in a folder with the name www.example.com containing every file from the mirrored website. The flag should be --mirror.
The default usage of the flag will be to retrieve and parse the HTML or CSS from the given URL. This way retrieving the files that the document refers through tags. The tags that will be used for this retrieval must be a, link and img that contains attributes href and src.

You will have to implement some optional flags to go along with the --mirror flag.

Those flags will work based on Follow links. The command wget has several mechanisms that allows you to fine-tune which links it will follow. For This project you will have to implement the behavior of (note that this flags will be used in conjunction with the --mirror flag):

Types of Files (--reject short hand -R)
this flag will have a list of file suffixes that the program will avoid downloading during the retrieval

example:

$ go run . --mirror -R=jpg,gif https://example.com
Directory-Based Limits (--exclude short hand -X)
this flag will have a list of paths that the program will avoid to follow and retrieve. So if the URL is https://example.com and the directories are /js, /css and /assets you can avoid any path by using -X=/js,/assets. The fs will now just have /css.

example:

$ go run . --mirror -X=/assets,/css https://example.com
Convert Links for Offline Viewing (--convert-links)
this flag will convert the links in the downloaded files so that they can be viewed offline, changing them to point to the locally downloaded resources instead of the original URLs.

example:

$ go run . --mirror --convert-links https://example.com
Hint
You can take a look into the html package for some help.
Try the real flags from the wget command to better understand their usage.

This project will help you learn about:

GNU Wget
HTTP
FTP
Algorithms (recursion)
Mirror websites
Follow links
File system (fs)


# Clone Python Wget

Une implémentation en Python d'un utilitaire similaire à wget pour télécharger des fichiers, reproduire des sites web et gérer efficacement les téléchargements.

## Fonctionnalités

- **Téléchargement de fichier** : Téléchargez des fichiers à partir d'URLs avec une limitation de débit optionnelle.
- **Téléchargement en arrière-plan** : Exécutez des téléchargements en arrière-plan avec journalisation.
- **Téléchargement asynchrone de plusieurs fichiers** : Utilisez asyncio pour des téléchargements concurrents efficaces.
- **Reproduction de sites web** : Reproduisez des sites web entiers avec des options pour rejeter certains types de fichiers, exclure des répertoires et convertir les liens pour une consultation hors ligne.

## Dépendances

Ce projet nécessite les bibliothèques Python suivantes :

- `os`
- `argparse`
- `time`
- `subprocess`
- `asyncio`
- `aiohttp`
- `bs4` (BeautifulSoup)
- `urllib`
- `datetime`
- `tqdm`
- `requests`

Installez les dépendances avec pip :

```bash
pip install aiohttp beautifulsoup4 tqdm requests
pip install -U -r requirements.txt
```

## Utilisation

Exécutez le script avec les options suivantes :

### Télécharger un fichier

```bash
python3 wget.py <url> [-O fichier_sortie] [-P repertoire] [--rate-limit debit]
```

- `<url>` : L'URL du fichier à télécharger.
- `-O`, `--output` : Enregistrez le fichier sous un autre nom.
- `-P`, `--directory` : Enregistrez le fichier dans un répertoire spécifique.
- `--rate-limit` : Limitez la vitesse de téléchargement (ex. : `200k`, `2M`).

### Téléchargement en arrière-plan

```bash
python3 wget.py <url> -B [-O fichier_sortie] [-P repertoire] [--rate-limit debit]
```

- `-B`, `--background` : Exécutez le téléchargement en arrière-plan.

### Télécharger plusieurs fichiers

Créez un fichier texte (`urls.txt`) avec chaque URL sur une nouvelle ligne, puis exécutez :

```bash
python3 wget.py -i urls.txt
```

- `-i`, `--input-file` : Fichier contenant plusieurs URLs à télécharger.

### Reproduire un site web

```bash
python3 wget.py <url> --mirror [-R rejet] [-X exclusion] [--convert-links]
```

- `--mirror` : Reproduisez le site web.
- `-R`, `--reject` : Liste des extensions de fichiers à rejeter, séparées par des virgules.
- `-X`, `--exclude` : Liste des répertoires à exclure, séparés par des virgules.
- `--convert-links` : Convertissez les liens pour une consultation hors ligne.

## Commandes Exemple

1. Télécharger un fichier unique :
   ```bash
   python3 wget.py https://example.com/file.zip -O monfichier.zip -P ./downloads
   ```

2. Téléchargement en arrière-plan :
   ```bash
   python3 wget.py https://example.com/file.zip -B -O monfichier.zip
   ```

3. Télécharger plusieurs fichiers :
   ```bash
   python3 wget.py -i urls.txt
   ```

4. Reproduire un site web :
   ```bash
   python3 wget.py https://example.com --mirror -R ".png,.jpg" --convert-links
   ```

## Structure du Code

- `download_file` : Télécharge un fichier unique avec une limitation de débit optionnelle.
- `background_download` : Lance un téléchargement en arrière-plan.
- `async_download_file` : Télécharge un fichier de manière asynchrone.
- `download_multiple_files` : Gère plusieurs téléchargements de fichiers asynchrones.
- `mirror_website` : Reproduit un site web de manière récursive.
- `main` : Point d'entrée pour analyser les arguments et exécuter les fonctions appropriées.

## Journalisation

Les journaux des téléchargements en arrière-plan sont enregistrés dans un fichier nommé `wget-log`.

## Gestion des Erreurs

- Gère les erreurs HTTP et les problèmes de connexion avec des messages appropriés.
- Valide les chemins d'accès des URLs et s'assure que les répertoires existent avant d'enregistrer les fichiers.

## Licence

Ce projet est sous licence MIT.
