# Challenge Triple A - Dashboard de Monitoring

## Description
Le Challenge Triple A est un projet de monitoring léger et autonome permettant d’afficher en temps réel les statistiques d’une machine virtuelle Linux via un dashboard web.  
Il combine trois compétences vues ce semestre :
- Administration : gestion et configuration d’une VM Ubuntu.
- Algorithmique : collecte et traitement des données système avec Python.
- Affichage : création d’une interface web en HTML/CSS/JS.

## Prérequis
- Une machine virtuelle Ubuntu Desktop 22.04 LTS (ou version plus récente).
- 2 GB de RAM minimum.
- 15 GB de stockage.
- Un accès à Internet (carte reseau NAT recommandée)
- Un utilisateur administrateur avec droits sudo.
- Python 3 installé avec pip, venv et les bibliothèques citées plus bas
- Apache2 installé

## Bibliothèques python utilisés
- psutil: bibliothèques principale pour récuperer les informations système (CPU, mémoire, processus, utilisateurs, uptime)
- platform : fournit des informations générales sur le système (nom de la machine, OS, version)
- socket : permet de récupérer l'adresse IP principale.
- os : utilisé pour parcourir un dossier et analyser les fichiers
- time et datetime : pour calculer l'uptime et afficher l'heure de démarrage
- getpass : pour récupérer le nom de l'utilisateur courant.
- defaultdict : pour gérer les clés par valeurs par défaut.

## Installation

Sur un logiciel de virtualisation tel que VMWare Workstation, 
- créer une machine avec les spécifications ci-dessus
- installer Ubuntu par son ISO officiel https://www.ubuntu-fr.org/download/
- s'assurer d'avoir un utilisateur avec droits sudo

### 1. Mettre à jour le système
```
sudo apt update && sudo apt upgrade -y
```

### 2. Installer et parametrer apache2 ssl
```
sudo apt install apache2 -y
sudo apt install openssl -y
sudo a2enmod ssl
sudo mkdir /etc/apache2/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/apache2/ssl/apache.key \
  -out /etc/apache2/ssl/apache.crt
```
### 3. Configurer le localhost
```
sudo nano /etc/apache2/sites-available/dashboardtripleA.conf
```
Modifier le début du fichier : 
```
<VirtualHost *:443>
    ServerName votre.adresse.i.p
    DocumentRoot /var/www/html

    SSLEngine on
    SSLCertificateFile /etc/apache2/ssl/apache.crt
    SSLCertificateKeyFile /etc/apache2/ssl/apache.key
```
```
sudo a2ensite dashboardtripleA.conf
sudo systemctl reload apache2
```

### 4. Cloner le projet
```
git clone https://github.com/nelson-grac-aubert/tripleA.git
cd tripleA
```
### 5. Installer Python et les dépendances
Installation de python, création et activation de l'environnement
```
sudo apt install python3 python3-venv -y
python3 -m venv tripleA
source tripleA.venv/bin/activate
```
Installation des dépendances
```
sudo apt install python3-pip -y
pip install psutil jinja2
```
### 6. Donner les droits d'écriture dans var/www au fichier Python
```
sudo chown -R $NOMDUTILISATEUR:www-data /var/www/html
sudo chmod -R 775 /var/www/html
```

### 7. Sécurisation de la VM 
Pour fermer tous les ports sauf le 443 https
```
sudo ufw status
sudo ufw enable
sudo ufw default deny outgoing
sudo ufw default deny incoming
sudo ufw allow 443
sudo ufw reload
sudo ufw status numbered
```
Pour rétablir les paramètres par défaut : 
```
sudo ufw reset
sudo ufw reload
```

## Utilisation
S'assurer d'être dans le bon environnement virtuel 
```
source tripleA.venv/bin/activate
```
```
python3 monitor.py
```
Le dashboard est alors visible à https://adresseip.de.la.VM, sur les navigateurs de votre VM et de votre machine hôte, 
après acceptation de l'avertissement de sécurité du au certificat autosigné
Tant que vous n'interrompez pas monitor.py, les mesures seront actualisées toutes les 30 secondes

### Fonctions python : 
get_cpu_info()
- But : Collecter les informations sur le processeur.
- Retourne : dictionnaire avec nombre de cœurs, fréquence actuelle (MHz), pourcentage d’utilisation CPU.

get_memory_info()
- But : Obtenir les informations sur la mémoire RAM.
- Retourne : dictionnaire avec RAM utilisée (GB), RAM totale (GB), pourcentage d’utilisation.

get_system_info()
- But : Récupérer les informations générales du système.
- Retourne : dictionnaire avec nom de la machine, OS, heure de démarrage, uptime, nombre d’utilisateurs connectés, adresse IP.

get_process_info()
- But : Lister les processus en cours et identifier les plus gourmands.
- Retourne : dictionnaire avec top 3 des processus les plus gourmands en utilisation de CPU et top 3 des processus les plus gourmands en utilisation de RAM

get_file_analysis(path)
- But : Analyser un dossier dont le chemin est donné en argument et compter les fichiers selon certaines extensions.
- Retourne : dictionnaire avec : nombre de fichiers par extension (.txt, .py, .pdf, .jpg), pourcentage de chaque type par rapport au total.

analize_files(root_dir, extensions)
- But : Parcourir récursivement tous les sous dossiers d'un répertoire choisi et faire la liste des 10 fichiers les plus volumineux.
- Retourne : dictionnaire avec : les dix fichiers les plus volumineux (extension et taille) et le nombre de fichier par extension et la taille de l'extension.

## Fonctionnalités
Informations sur le processeur :
- Nombre de cœurs du processeur
- Fréquence actuelle du CPU
- Pourcentage d'utilisation CPU
- Charge moyenne système : dernière minute, 5 dernières, 15 dernières

Informations sur la mémoire :
- RAM utilisée (en GB)
- RAM totale (en GB)
- Pourcentage d'utilisation de la RAM
- Stockage utilisé (en GB)
- Stockage total (en GB)
- Pourcentage d'utilisation du stockage

Informations système générales :
- Nom de la machine
- Système d'exploitation (distribution et version)
- Heure de démarrage du système
- Temps écoulé depuis le démarrage (uptime)
- Nombre d'utilisateurs connectés
- Adresse IP principale

Informations sur les processus :
- Top 3 des processus en cours avec leur consommation CPU (%)
- Top 3 des processus en cours avec leur consommation RAM (%)

Analyse de fichiers :
- Analyser un dossier au choix
- Compter le nombre de fichiers pour plus de 10 extensions
- Calculer le nombre total de fichiers pour chaque extension
- Calculer le pourcentage que représente chaque type de fichier par
rapport au total

## Captures d'écran
cf. Dossier Screenshots

## Difficultés rencontrées
- Quelles manières adoptés pour le remplacement des variables dans le fichier template.html (replace, Flask, Jinja2, Django)
Conditions par couleur : finalement plus simple avec Jinja2 ce qui a motivé notre choix pour cette option.
- Après modification du .cdd et du .script dans le dossier source d'apache2, le dashboard ne s'actualisait pas en conséquence : cela est du au cache du navigateur, on doit donc le rafrachir avec ctrl+F5 pour vider le cache.
## Améliorations possibles
- Python : récuperer plus de données système, comme le pourcentage d'utilisation de chaque coeur, le nombre de threads
- HTML / CSS / JS : ajouter des graphiques pour suivre l'évolution des variables au cours de l'uptime de la machine
- Rajouter un bouton "Print current state as PDF" dans le footer
- Ajouter l'API de virus total pour vérifier les fichiers important et/ou douteux (seulement 4 fichiers par jour pour la version gratuite / test difficile)
- 

## Auteur
Maxime Fourquié, Marius Gavini, Nelson Grac-Aubert
