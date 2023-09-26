# Portail GPS 3 Vallées
Portail de suivi de la faune équipée de balises GPS dans le cadre de la Convention 3 Vallées

## Technologies

Machine virtuelle :
- Système d’exploitation Linux : Debian v10
- Système de gestion de base de données relationnelles : PostgreSQL v15.2 et PostGIS v3.3.2
- Logiciel de gestion de version décentralisé : Git v2.20.1
- Gestionnaire de paquets : npm v9.8.1
- Logiciel d’exécution JavaScript : Node.js v16.13.0

Machine physique :
- Logiciel de terminal pour Windows : MobaXterm v23.0
- Logiciel d’échange de fichiers entre serveur local et distant : WinSCP v5.21.7
- Logiciel de base de données : DBeaver v23.0.1
- Logiciel d’édition de code : Visual Studio Code
- Extensions VSCode : Python v2023.14.0, Pylance v2023.8.30, Vue Language Features (Volar) v1.8.8
- Navigateur web : Google Chrome.

Application :
- Front-end : Vue js v3, Bootstrap v5.3.0, Leaflet v1.9.4, Leaflet-polylinedecorator v1.6.0
- Back-end : Back-end de FollowDem-Admin https://github.com/PnVanoise/FollowDem-admin/tree/FDadmin-tests-stage 

## Fonctionnalités 

- Liste des espèces de la convention
- Liste des individus équipés 
- Affichage des traces GPS selon l'individu et la période sélectionnés 
- Onglets pour contextualiser l'application

## Installation 

Prérequis :
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install postgresql-15
sudo apt-get install postgis postgresql-15-postgis-3
sudo apt-get install python3
sudo apt-get install python3-venv
sudo apt-get instamm python3-pip
sudo apt-get install apache2
sudo apt-get install nodejs
sudo apt-get install npm
sudo apt-get install git

sudo pip3 install gunicorn
```
### Installation de FollowDem-Admin 

Clonez le dépôt (dans /home/user):
```
sudo wget https://github.com/PnVanoise/FollowDem-admin/archive/refs/heads/main.zip
unzip main.zip
```
Le projet ayant été élaboré sur une branche, il est possible qu'elle ne soit pas encore appliquée au main, si c'est le cas (dans /home/user) :
```
sudo wget https://github.com/PnVanoise/FollowDem-admin/archive/refs/heads/FDadmin-tests-stage.zip
unzip FDadmin-tests-stage.zip 
```
Suivez la doc d’installation (ignorez la partie "Import des données") : https://github.com/PnEcrins/FollowDem-admin/blob/master/docs/installation.rst

Déploiement Gunicorn :
- Copiez et éditez le fichier de settings : `cp ./settings.ini.sample ./settings.ini`
- Copiez le fichiez de service : `cp ./GPS3V-admin.service.template /etc/systemd/system/GPS3V-admin.service`
- Rendre exécutable le fichier sh : `chmod +x /home/user/GPS3vallees-admin/gunicorn_start.sh`
- Démarrez le service : 
```
sudo systemctl start GPS3V-admin
sudo systemctl enable GPS3V-admin
```
- Pour vérifier l’état du service : `sudo systemctl status GPS3V-admin`
- Pour arrêter le service si besoin : `sudo systemctl stop GPS3V-admin`
- Pour relancer le service si besoin : `sudo systemctl restart GPS3V-admin`

Le serveur est ouvert sur l’IP et le port que vous avez configuré, exemple : http://localhost:5000/ 

### Installation de GPS 3 Vallées

Clonez le dépôt (dans /home/user):
```
sudo wget https://github.com/PnVanoise/Portail-3-vallees/archive/refs/heads/main.zip

unzip main.zip 
```
Mettez à jour les packages (pour les librairies Leaflet, Bootstrap notamment) :
```
cd Portail-3-vallees/app 
npm update --save
```
Personnalisation de l'application :
- Copiez et éditez le fichier de config situé dans /public : `cp ./config.json.sample ./config.json`
- Développement de l’application : `npm run dev`
- Compil de l’application pour la production (création d’un répertoire dist) : `npm run build` 

Déploiement Apache :
- Copiez la configuration située dans /app : `cp ./conf_apache.template  /etc/apache2/sites-available/GPS3vallees.conf`  
- Editez : `sudo nano /etc/apache2/sites-available/GPS3vallees.conf`
- Activez le service : `sudo a2ensite GPS3vallees.conf`
- Redémarrez Apache2 : `sudo systemctl restart apache2`

## Copyright
Auteur·ices :

Parc National de la Vanoise

- Alix Cornu-Lachamp
- Claire Lagaye
- Christophe Chillet 

Licence :

- OpenSource
- (c) GPS 3 Vallées 2023 Parc National de la Vanoise

