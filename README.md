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
