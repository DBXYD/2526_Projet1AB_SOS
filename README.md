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

Table des matières

Introduction

Contexte et Problématique
Objectifs du Projet SOS
Solution mise en œuvre


Analyse des blocs fonctionnels

Bloc Alimentation
Bloc Port USB-C
Bloc STM32
Bloc Lecteur RFID
Bloc Connecteur SWD
Boutons et signaux utilisateur
Trous de fixation


Routage
Configuration des pins
Software
Question environnementale

# 2526_Projet1AB_SOS
## Introduction
### 1.1 Contexte et Problématique
Dans le cadre de la gestion logistique des laboratoires de l'ENSEA, le suivi précis et rigoureux des composants électroniques constitue un défi quotidien. Actuellement, l'inventaire repose sur un référencement manuel via un fichier Excel, et le stockage physique est réparti dans des boîtes de dimensions variables.
Ce mode de gestion présente plusieurs limites :

- Erreurs d'indexation : Risque élevé d'oublis ou de doubles saisies lors d'une mise à jour des stocks.
- Perte de traçabilité spatiale : Difficulté à localiser physiquement les boîtes suite à des déplacements ou réorganisations.
- Asynchronisme des données : Décalage temporel entre le mouvement réel d'un composant et sa mise à jour logicielle.

### 1.2 Objectifs du Projet SOS
Le projet SOS (Stock Organizer Scan) vise à concevoir un système embarqué de numérisation basé sur la technologie RFID (Radio Frequency Identification).
Chaque boîte de rangement se voit attribuer un tag RFID unique. Le dispositif SOS lit et écrit ces puces pour associer un contenant physique à ses données logistiques :
- Le MPN (Manufacturer Part Number) : référence exacte du constructeur
- SKU (Stock Keeping Unit) : code interne d'identification du stock
- LocalisationSalle précise au sein des différents tiroclasses de l'ENSEA
- Quantité exact d'exemplaires restants


### 1.3 Solution mise en œuvre
Le projet s'articule autour de deux parties :

1) [Hardware](./Hardware) : Une carte électronique sur mesure intégrant une carte électronique sur mesure intégrant un microcontrôleur basse
consommation STM32L4, un lecteur RFID communiquant via bus SPI matériel, et une interface USB-C assurant à la fois l’alimentation et l’échange de données haut débit.



3) [Software](./Software) : Une interface utilisateur développée en Python, permettant aux techniciens d'interagir avec la base de données.


## 2. Analyse détaillée des blocs fonctionnels
Le schématique du système SOS (Stock Organizer Scan) est structuré de manière ri-
goureuse en blocs fonctionnels distincts.

### 2.1 Bloc Alimentation (Power Supply)
Ce bloc assure la conversion et la régulation de l'énergie nécessaire aux différents composants.
- Composants identifiés :
ComposantValeur / RéférenceRôleRégulateur LDOBU33SD5WG-TRConversion 5 V → 3,3 VC1, C21 µFCondensateurs de découplageSW1SW_SPDTInterrupteur d'alimentationD1, D2LEDIndicateurs d'étatR3, R43,4 kΩ / 1,6 kΩRésistances de limitation
Justification des choix :

BU33SD5WG-TR — LDO compact, idéal pour abaisser le 5 V USB vers 3,3 V avec une capacité en courant suffisante pour alimenter simultanément le STM32 et le lecteur RFID.
C1 et C2 (1 µF) — Placés en découplage sur l'entrée et la sortie du LDO conformément aux spécifications constructeur, pour stabiliser la tension.
SW1 (SW_SPDT) — Permet de couper l'alimentation sans débrancher physiquement le câble USB.


### 2.2 Bloc Port USB (USB-C)
L'interface USB-C gère le transfert de données et l'apport d'énergie principal.
Composants identifiés :
ComposantRéférenceRôleConnecteur USB-CJ1 — 629722000214Connecteur principalProtection ESDU2 — USBLC6-2SC6Protection des lignes D+/D−R1, R25,4 kΩ / 5,1 kΩConfiguration CC1/CC2
Justification des choix :

USB-C (vs Micro-USB) — Réversible, plus robuste mécaniquement.
USBLC6-2SC6 — Réseau de diodes TVS bidirectionnel ultra-faible capacité, indispensable contre les décharges électrostatiques (ESD) lors de la manipulation du connecteur.


### 2.3 Bloc STM32 (Microcontrôleur principal)
Le cœur logique du système repose sur le STM32L476RGTx (boîtier LQFP64) de STMicroelectronics.
Signaux routés notables :
SignalFonctionSPI1_*Liaison vers le lecteur RFIDVCP_TX / VCP_RXInterface UART → USB pour communication PythonUSB_DN / USB_DPLignes différentielles du bus USB physiqueSWDIO / SWCLKInterface de programmation/débogage JTAG/SWDUSR_LED_1 / USR_LED_2Indication d'état (ex : scan réussi)NRST / BOOT0Lignes de contrôle

Note : Les condensateurs de découplage C5 à C10 (100 nF) sont assignés individuellement à chaque broche VDD du STM32 pour supprimer le bruit haute fréquence issu des commutations internes.


### 2.4 Bloc Lecteur RFID
Ce bloc gère l'acquisition des données des tags RFID attachés aux produits stockés.

Interface SPI — Bus haute vitesse (jusqu'à 10 Mbit/s), réduisant la latence lors de la lecture des identifiants.
Compatibilité de tension — Fonctionnement natif en 3,3 V, compatible directement avec le STM32.
Découplage local (C13, C14 — 1 µF) — Placés au plus près du circuit RFID pour pallier les appels de courant générés par l'antenne lors de l'émission du champ magnétique RF.


### 2.5 Bloc Connecteur SWD
Ce bloc offre un accès direct aux broches de débogage via une sonde externe de type ST-Link, pour le flashage et le débogage à chaud du microcontrôleur.

### 2.6 Boutons et signaux utilisateur
SignalComposantRôle fonctionnelCondensateurValeurUSR_BTN_1/2SW2, SW3 (Push)Interaction — Scan / Validation manuelleC12, C13100 nFBOOT_DSW5 (Push)Raccordement BOOT0 à 1——NRSTSW4 (Push)Réinitialisation matérielle (Reset)C1510 nF

### 2.7 Trous de fixation (Mounting Pads)
Les quatre perçages H1 à H4 (MountingHole_Pad) garantissent la rigidité de l'intégration au sein d'un boîtier personnalisé.

## 3. Routage
Le passage du schéma théorique au tracé des pistes physiques impose le respect de contraintes géométriques et électromagnétiques strictes.
Placement des blocs
Le STM32L476RGTx (LQFP64) occupe une position centrale, permettant une distribution homogène des pistes vers les différents périphériques et minimisant la longueur moyenne des connexions.
BlocPlacementJustificationConnecteur USB-C + Protection ESDBord de carteLes décharges ESD sont dérivées à la masse avant de pénétrer dans le circuitConnecteur RFIDPériphérie supérieureConnecteur femelle barrette pour liaison stable avec le module MFRC522Connecteur SWD (J2)Côté droitAccès aisé à la sonde ST-Link sans gêner le port USBMounting Pads4 angles symétriquesPassage des vis sans risque de court-circuit

## 4. Configuration des pins
Le microcontrôleur STM32L476RGTx (LQFP64) est configuré avec les affectations suivantes :

Port A — SPI1 (NSS, SCK, MISO, MOSI), USB (DM, DP), VCP (TX, RX)
Port B — RFID IRQ, boutons utilisateur (BTN_1, BTN_2), SWD, LEDs utilisateur
Port C — OSC, LEDs, RFID RST
Signaux de contrôle — NRST, BOOT0


##5. Software
### 5.1 Firmware
(Section en cours de rédaction)
5.2 Interface Python
Une application Python assure l'interface entre l'utilisateur et la carte SOS. Elle s'appuie sur trois bibliothèques principales :
BibliothèqueRôleserialGestion de la liaison série — ouverture et écoute du port COM virtuel (VCP) créé via USB-CtkinterFramework IHM — génération de la fenêtre, boutons de contrôle, mise à jour dynamique des labelspandasManipulation de données — chargement et recherche indexée dans le fichier Excel d'inventaire
