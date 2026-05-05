# Simulation d’un USV maritime sous Gazebo

## Description
Ce projet consiste à simuler un véhicule de surface autonome (USV) dans un environnement maritime en utilisant Gazebo et ROS2.  
L’objectif est de modéliser un bateau (WAM-V), de l’intégrer dans un environnement réaliste et de contrôler son déplacement à l’aide d’un script Python.

## Étapes du projet

### 1. Mise en place de l’environnement
- Téléchargement d’un workspace maritime depuis une ressource officielle Gazebo  
- Installation des dépendances ( colcon, etc.)
- Configuration du workspace
- Lancement de l’environnement maritime `sydney_regatta`

### 2. Création et configuration du monde
- Modification du fichier `.sdf`
- Ajout de plugins (physique, capteurs, interface)
- Intégration de l’environnement maritime (eau, vagues)
- Ajout de coordonnées géographiques et d’éléments du décor

### 3. Intégration du véhicule
- Ajout du modèle **WAM-V**
- Activation des effets hydrodynamiques
- Compilation et lancement de la simulation

### 4. Contrôle du bateau
- Développement d’un script Python
- Envoi de commandes de poussée aux hélices via les topics Gazebo
- Contrôle de l’orientation des propulseurs
- Déplacement du bateau d’un point A vers un point B
- Arrêt et stabilisation

## Résultat
La simulation permet de visualiser un USV évoluant dans un environnement maritime réaliste.  
Le bateau peut se déplacer, s’arrêter et se stabiliser à l’aide des commandes envoyées.

## Technologies utilisées
- Gazebo
- ROS2
- Python

## Auteur
Hanane
