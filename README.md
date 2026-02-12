# 2526_Projet1AB_SOS
## Introduction
### Projet SOS: Stock Organizer Scan
L'objectif de ce projet est de créer un scanner et programmeur RFID pour la gestion des inventaires de l'ENSEA.

Actuellement, les divers composants en stock à l'école sont inventoriés dans un fichier Excel et rangés dans des boîtes de taille variable. Le problème constaté est la difficulté de suivi de ces stocks (changement de localisation des boîtes, par exemple).
C'est pourquoi un système permettant l'accès à l'inventaire a été pensé.

Au fond de chaque boîte sera fixé une puce RFID l'identifiant. Le SOS assurera l'interaction entre la puce et l'utilisateur, qui pourra depuis un ordinateur accéder en lecture/écriture à son emplacement, son MPN, son SKU.

## Vue d'ensemble du projet
La partie hardware de SOS devra donc comprendre un moyen de scanner la puce RFID et un port USB pour la communication avec un PC sous Linux.
La partie software sera centrée sur une interface faite avec Python assurant les fonctions susmentionnées.

## Annexes
