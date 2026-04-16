# 2526_Projet1AB_SOS
## Introduction
### Projet SOS: Stock Organizer Scan
L'objectif de ce projet est de créer un scanner et programmeur RFID pour la gestion des inventaires de l'ENSEA.

Actuellement, les divers composants en stock à l'école sont inventoriés dans un fichier Excel et rangés dans des boîtes de taille variable. Le problème constaté est la difficulté de suivi de ces stocks (changement de localisation des boîtes, mise à jour des stocks).
C'est pourquoi un système permettant l'accès à l'inventaire a été pensé. En effet, nous cherchons à réaliser un scan de composant grâce à un lecteur RFID permettant de pouvoir retrouver l'identité d'un composant scané ainsi que le rangement et le nombre d'exemplaire restant.

Au fond de chaque boîte sera fixé une puce RFID l'identifiant. Le SOS assurera l'interaction entre la puce et l'utilisateur, qui pourra depuis un ordinateur accéder en lecture/écriture à son emplacement, son MPN et son SKU.

## Vue d'ensemble du projet
La partie hardware de SOS devra donc comprendre un moyen de scanner la puce RFID et un port USB pour la communication avec un PC sous Linux.
La partie software sera centrée sur une interface faite avec Python assurant les fonctions susmentionnées.

## Annexes
### Justification des choix de composants
- Microcontrôleur : le microcontrôleur possède un écosystème connu à l'ENSEA avec des performances suffisantes pour gérer le SPI du RFID et l'USB simultanément.
- Connecteur USB-C : nous n'utilisons pas de Micro-USB en raison de la réversbilité, de la robustesse mécanique et des standards actuels des entreprises que l'USB-C confert.
- Protection USB-C : indispensable pour protéger le microcontôleur contre l'électricité statique lorsqu'un utiisateur touche le connecterur USB.

### Diagramme des Signaux
- RFID <-> STM32 : communication grâce au bus SPI (grande vitesse pour lire les identifiants SKU/MPN).
- STM32 <-> PC : communication via UART (converti en USB par le port série virtuel) pour l'interface Python.
- Feedback : les LEDs USR_LED_1 et USR_LED_2 permettent de confirmer visulement que la boîte à bien été scannée.

### Alimentaion
- Entrée : 5V provenant de l'USB
- Régulation : Utilisatin d'un régulateur LDO por abaisser la tension à 3.3V nécessaire pour le STM32 et le module RFID.
- Condensateurs de filtrage : permettent d'éviter la chute de tension des pics de consommations du lecteur RFID.

### Spécifications du Routage
- Largeur des pistes : plus large pour l'alimentaion pour limiter la résistance et plus fines pour les signaux de donées.
- Trous de fixation : Emplacements prévus pour visser la carte au fond d'un boîtier imprimé en 3D.
