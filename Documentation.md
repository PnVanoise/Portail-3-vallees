## I Blibliographie
### Structure des données de capteurs

 - Capteurs PNV: structure des données, modalités de transmission, critères de validité
	 - Ornitela
	 - Biotrack
	 - Technosmart
	 - Iops
	 - Xerius
 - Interrogation PNx + recherche web pour autres types de capteurs à prendre en compte
### Audit des sites/applications existants
 - Followdem (Parc national des Ecrins)

## II Architecture du site
### Modèle Conceptuel de Données

 - Liste des tables
	 - Espèces
	 - Individus : espèce, sexe, année naissance, date capture
	 - Capteurs: fabricant, numero de série
	 - Table correspondance individus/capteurs: id individu, id capteur, date début, date fin
	 - Données GPS: id_capteur, date, heure, x, y, z, temperature, accel, hdop...
	 - Gestion des logins: usershub ??
### Modèle fonctionnel
- Inventaire des fonctionnalités attendues
- Test followdem + followdem-admin
- Présentation d'un prototype: à valider avec chargé de mission

## III Développement
 
## IV Tests

## II Déploiement
- Site Convention 3 vallées (grand public, accès libre)
- Site PNV (professionnel, accès avec login): Lizmap ??
