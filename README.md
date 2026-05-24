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
- Quantité exacte d'exemplaires restants


### 1.3 Solution mise en œuvre
Le projet s'articule autour de deux parties :

1) [Hardware](./Hardware) : Une carte électronique sur mesure intégrant une carte électronique sur mesure intégrant un microcontrôleur basse
consommation STM32L4, un lecteur RFID communiquant via bus SPI matériel, et une interface USB-C assurant à la fois l’alimentation et l’échange de données haut débit.



3) [Software](./Software) : Une interface utilisateur développée en Python, permettant aux techniciens d'interagir avec la base de données.


## 2. Analyse détaillée des blocs fonctionnels
Le schématique du système SOS (Stock Organizer Scan) est structuré de manière ri-
goureuse en blocs fonctionnels distincts.



### 2.1 Bloc Alimentation (Power Supply)

<img width="585" height="357" alt="image" src="https://github.com/user-attachments/assets/e62d326b-0834-417b-bf93-7d223d7096c7" />

Ce bloc assure la conversion et la régulation de l'énergie nécessaire aux différents composants.

- Composants identifiés :
  - Régulateur LDO :  BU33SD5WG-TR (5 V → 3.3 V)
  - Condensateurs : C1 (1 μF) et C2 (1 μF)
  - Interrupteur : SW_SPDT (SW1)
  - LEDs indicatrices : D1 et D2 avec résistances associées R3 (3.4 kΩ) et R4 (1.6 kΩ)




- Justification des choix :
  - BU33SD5WG-TR : Ce régulateur (LDO) est particulièrement adapté pour abaisser le 5V issu de l’USB vers le rail 3.3 V. Son boîtier compact minimise l’empreinte au sol. De plus, sa capacité en courant ici est largement suffisante pour alimenter simultanément notre microcontrôleur STM32 et le lecteur RFID.

  - C1 et C2 (1 μF) : Placés en découplage direct sur l’entrée et la sortie du LDO conformément aux spécifications du constructeur. Ils stabilisent la tension ici.
  - SW1 (SW_SPDT) : Permet de couper l’alimentation de la carte sans avoir à débrancher physiquement le câble USB. Cela est plutôt intéressant d’un point de vue confort d’utilisation.


### 2.2 Bloc Port USB (USB-C)

<img width="808" height="500" alt="image" src="https://github.com/user-attachments/assets/f65551fc-c018-4f00-b9a4-c569cc49adb4" />

L'interface USB-C gère le transfert de données et l'apport d'énergie principal.

- Composants identifiés :
  - Connecteur USB-C : J1 (Référence commerciale : 629722000214)
  - Protection ESD : U2 (USBLC6-2SC6)
  - Résistances de configuration : R1 (5.4 kΩ), R2 (5.1 kΩ) sur les lignes CC1/CC2
  - 
- Justification des choix :
  - Connecteur Molex USB-C : Nous avons opter ici pour USB-C et non un Micro-USB car
le premier est réversible et largement plus robustesse.
  - USBLC6-2SC6 : Réseau de diodes TVS bidirectionnel ultra-faible capacité dédié à la
protection des lignes D+ et D−. Cette protection est indispensable contre les décharges
électrostatiques (ESD) induites lorsque’un humaine manipule le connecteur USB manuellement.





### 2.3 Bloc STM32 (Microcontrôleur principal)

<img width="611" height="877" alt="image" src="https://github.com/user-attachments/assets/0fe394a4-3ff7-4fe9-bc99-223fed6b7e5d" />

Le cœur logique du système repose sur le STM32L476RGTx (boîtier LQFP64) de STMicroelectronics. Composant central : STM32L476RGTx.

Ecosystème ENSEA : Il s’agit d’un composant sur lequel nous avons ulterieusrement eu a travaillé durant les séances de TD et TP surtout. SPI Matériel dispose de plusieurs bus SPI indépendants pour piloter à haute fréquence le lecteur RFID.

- Signaux notables :
  - SPI1_* → Liaison vers le lecteur RFID.
  - VCP_TX / VCP_RX → Interface UART pontée vers l’USB pour la communication avec le
script Python.
  - USB_DN / USB_DP → Lignes différentielles du bus USB physique.
  - SWDIO / SWCLK → Interface de programmation/débogage JTAG/SWD.
  - USR_LED_1 / USR_LED_2 → Indication d’état utilisateur (ex : scan réussi).
  - NRST / BOOT0 → Lignes de contrôle.
 
Remarque : Les condensateurs de découplage (C5 à C10, 100 nF) sont assignés individuellement à chaque broche d’alimentation VDD du STM32. Ils suppriment le bruit haute fréquence issu des commutations internes du coeur.



### 2.4 Bloc Lecteur RFID
<img width="608" height="293" alt="image" src="https://github.com/user-attachments/assets/06681ab6-ed1c-4f6f-b50f-fd46d644c5a4" />

Ce bloc gère l'acquisition des données des tags RFID attachés aux produits stockés.

- Interface SPI : Exploitation du bus à haute vitesse (jusqu’à 10 Mbit/s), réduisant la
latence lors de la lecture des identifiants.
- Compatibilité de tension : Fonctionnant sous 3.3 V, le composant fonctione directement
avec le STM32.
- Découplage local (C13,C14 - 1 μF) : Placés au plus près du circuit RFID pour pallier les
appels de courant violents générés par l’antenne lors de l’émission du champ magnétique
RF.







### 2.5 Bloc Connecteur SWD
<img width="500" height="391" alt="image" src="https://github.com/user-attachments/assets/5746ba05-d575-4bd6-9858-1699a89f63e5" />

Ce bloc offre un accès direct aux broches de débogage via une sonde externe de type ST-Link, pour le flashage et le débogage à chaud du microcontrôleur.

### 2.6 Boutons et signaux utilisateur


<img width="606" height="547" alt="image" src="https://github.com/user-attachments/assets/37c3baa9-7c05-40d9-a0b3-a22adbeae8fd" />


<img width="724" height="90" alt="image" src="https://github.com/user-attachments/assets/fbd93d9d-eef4-4d98-9e75-a6cbb7b068f7" />


### 2.7 Trous de fixation (Mounting Pads)

<img width="607" height="379" alt="image" src="https://github.com/user-attachments/assets/17e7d572-a427-4f82-a37f-08e2043f30c1" />

Les quatre perçages H1 à H4 (MountingHole_Pad) garantissent la rigidité de l’intégration au sein d’un boîtier personnalisé.

## 3. Routage
Le passage du schéma théorique du [PCB](./PCB) permettant le tracé des pistes physiques impose le respect de contraintes géométriques et électromagnétiques strictes.

 

<img width="616" height="575" alt="image" src="https://github.com/user-attachments/assets/a53242b7-c758-4e9f-b950-08e325036e92" />

### 3.1 Réalisation Matérielle et Placements des blocs

La conception du circuit imprimé a abouti à une modélisation tridimensionnelle permettant de valider l’intégration mécanique des composants, l’accessibilité des connecteurs.

Le microcontrôleur STM32L476RGTx (boîtier LQFP64) occupe une position parfaitement centrale. Cette disposition permet une distribution homogène des pistes de signaux vers les différents périphériques, minimisant ainsi la longueur moyenne des pistes.

- Implantation des diffférents blocs :
  - Connecteur USB-C et Protection ESD : Placés au plus près du bord de la carte. L’alignement direct du circuit de protection TVS en entrée du connecteur garantit que les décharges électrostatiques sont immédiatement dérivées vers la masse avant de pouvoir se propager vers l’intérieur du circuit.
  - Connecteur d’extension RFID : Disposé sur la périphérie supérieure sous forme d’un connecteur femelle barrette, offrant une liaison mécanique et électrique stable pour le module MFRC522 tout en évitant les superpositions de composants.
  - Connecteur SWD (J2) : Isolé à droite afin de permettre un raccordement aisé de la sonde ST-Link lors des phases de flashage sans gêner l’accès au port USB principal.
  - Mounting Pads : la présence de quatre trous de fixation métallisés (Mounting Pads) répartis de manière symétrique aux quatre angles de la carte valide l’aptitude du prototype à être intégré de manière rigide au sein d’un boîtier de protection. L’espacement laissé libre autour de ces trous garantit le passage des têtes de vis sans risque d’écrasement ou de court-circuit sur les pistes environnantes.

## 4. Configuration des pins
<img width="611" height="877" alt="image" src="https://github.com/user-attachments/assets/d9d7188c-23e8-41e3-bce7-823d32ae9f4e" />

Le microcontrôleur STM32L476RGTx (LQFP64) est configuré avec les affectations suivantes :

<img width="544" height="449" alt="image" src="https://github.com/user-attachments/assets/1269685d-3aa4-4d53-9e83-b443684b7623" />


- Port A — SPI1 (NSS, SCK, MISO, MOSI), USB (DM, DP), VCP (TX, RX)
- Port B — RFID IRQ, boutons utilisateur (BTN_1, BTN_2), SWD, LEDs utilisateur
- Port C — OSC, LEDs, RFID RST
- Signaux de contrôle — NRST, BOOT0


## 5. Software
### 5.1 Firmware
La liaison entre le PC et le tag RFID à travers le PCB est gérée par du code en C, où on retrouve une séparation par composants. Le projet est construit de manière à pouvoir réutiliser des morceaux du code pour d’autres projets faisant intervenir des composants de celui-ci.\
Par la suite on détaillera seulement les fichiers contenant des fonctions écrites par nous, et non des fichiers générés par STM32CubeIDE lors de l'affectation des pins sur le .ioc (gpio, spi, usart,...).\

Dans le main.c se trouvent des appels aux fonctions d'initialisation et une boucle infinie où l'appel à test() de algo.c permet de tester des fonctionnalités en mode debuggeur.\
\
Le fichier rfid.c contient des fonctions ayant trait à la liaison SPI entre la STM32 et le lecteur RFID, et une structure permettant de définir les broches associées à un lecteur RFID. Cette dernière est initialisée grâce à la fonction RFID_init(hrfid, hspi, hspi_nss_port, hspi_nss_pin, rst_port, rst_pin). 

- void RFID_transmit(RFID_HandleTypeDef* hrfid, uint8_t* data, int size) transmet les données de data au tag et les y écrit;
- void RFID_receive(RFID_HandleTypeDef* hrfid, uint8_t* data, int size) lit les données du tag et les envoie au master en les stockant dans un buffer data.
- void RFID_transmit_receive(RFID_HandleTypeDef* hrfid, uint8_t* pTxData, uint8_t* pRxData, int size) fait les deux, l’un après l’autre.


Le fichier algo.c contient des fonctions rassemblant celles des autres fichiers, mettant ainsi bout à bout les différents éléments du PCB. Les fonctions read et write font alors intervenir le lecteur RFID et la liaison USART avec le PC. 

- void test() est utile pour la phase développement: elle aide à vérifier le fonctionnement de read(huart, hrfid, pdata, size) et write(huart, hrfid, pdata, size). On commence par lire le tag RFID, puis on y enregistre des données qu’on cherche enfin à retrouver en refaisant appel à read. 

- uint8_t SPI1_WriteRead(uint8_t data, SPI_HandleTypeDef hspi1) fait appel à RRFID_transmit_receive(hrfid, pTxData, pRxData, size). Elle est particulièrement utile dans les cas où ces deux actions doivent être effectuées l’une après l’autre. RFID_transmit_receive gère le délai de transmission. 

### 5.2 Interface Python
Pour assurer l’interface entre l’utilisateur et la carte électronique SOS, une application logicielle a été développée en Python qui était une condition nécéssaire dans notre projet. 
L’application s’appuie sur trois bibliothèques clés, assurant chacune un rôle pilier dans le traitement des données :
Le script Python s’appuie sur trois bibliothèques principales pour articuler ses différentes tâches. Elles sont structurées de la manière suivante :

- serial :
  - Rôle : Gestion de la couche de liaison série.
  - Utilité : Permet l’ouverture, la configuration et l’écoute du port COM virtuel (VCP) créé par le branchement USB-C du STM32. C’est elle qui intercepte le flux binaire.
    
- tkinter :
  - Rôle : Framework de construction d’Interface Homme-Machine (IHM).
  - Utilité : Bibliothèque standard de Python permettant de générer la fenêtre principale de l’application SOS, de positionner les boutons de contrôle et de mettre à jour dynamiquement les étiquettes de texte lors d’un scan.

- pandas :
  - Rôle : Manipulation et analyse de structures de données.
  - Utilité : Charge en mémoire le fichier tableur Excel faisant office de base de données d’inventaire de l’ENSEA. Elle permet d’effectuer des recherches indexées ultrarapides à partir d’un emplacement donné pour en extraire le MPN et le SKU.


Dans notre progremme Python, on retrouve les fonctions suivantes : 
- scan() :
  - Entrée : void
  - Rôle : Ouvre le canal de communication série USB-C avec le STM32.
  - Sortie : serial.Serial ou None : ser (instance de connexion)
- decode(data) :
  - Entrée : bytes : data
  - Rôle : Convertit les données en hexadécimal reçues en une listee de caractères utilisable.
  -Sortie : list[str,str,int,int,int] : location
- search_info(location) :
  - Entrée : list : location
  - Rôle : Requête de recherche au sein du fichier d’inventaire Excel 
  - Sortie : int : mpn, int : sku
- display_info(mpn, sku, location) :
  - Entrée : int : mpn, int : sku, list : location
  - Rôle : Met à jour dynamiquement l’interface graphique.
  - Sortie : NoneType : None
- read_data():
  - Entrée : void
  - Rôle : Suite à l'appui sur le bouton read, appelle les fonction scan, decode, search_info et display_info pour afficher SKU, MPN et localisation sur l'interface
  - Sortie : Nonetype : None
- write_loc():
  - Entrée : void
  - Rôle : demande à l'utilisateur la localisation à attribuer à la puce scannée 
  - Sortie : Nonetype : None
- display_value():
  - Entrée : void
  - Rôle : Suite à l'appui sur le bouton "done" (lorque l'utilisateur a entré la localisation et a terminé), convertit cette localisation en identifiant (locbytes) puis appelle la fonction assign_tag(loc_bytes)
  - Sortie : Nonetype : None
- assign_tag(loc_bytes):
  - Entrée : bytes loc_bytes
  - Rôle : Ouvre le canal de communication série USB-C avec le STM32 et envoie à la STM32 l'identifiant à attribuer à la puce.
  - Sortie : Nonetype : None
  
## 6. Question environnementale

A l'issue de notre projet nous avons finalement choisis la question : Votre projet recherche-t-il la rentabilité dans une perspective de viabilité financière ?

A cette question, nous y repondons *oui* et ce pour plusieurs raisons :
- **Gain de temps et d'organisation** : le système SOS permet aux techniciens de localiser instantanément les composants, réduisant les pertes de temps liées à la recherche manuelle en tiroir.
- **Économie d'argent important** : avec une actualisation automatique du système, nous pouvons éviter de recommander des composants déjà présents au sein de l'école.
- **Facilité de commande** : grâce au suivi précis des stocks (quantité, SKU, MPN), les réapprovisionnements sont déclenchés au bon moment, évitant les ruptures comme les sur-stocks inutiles.
- **"Le temps c'est de l'argent"** : chaque minute gagnée en gestion de stock est une minute réinvestie dans des tâches à plus forte valeur ajoutée.

En ce sens, le projet SOS s'inscrit pleinement dans une logique de rentabilité opérationnelle et de viabilité financière à long terme.

## Conslusion
Le projet SOS (Stock Organizer Scan) est, à ce stade, un projet en cours de développement dont on a malheuresement pas pu venir à bout. Cependant, nous avons pu faire une belle avancée : une carte électronique sur mesure intégrant un microcontrôleur STM32L4 et un lecteur RFID, couplée à une interface logicielle en Python, constitue une solution cohérente et pensée pour répondre à un besoin concret au sein de l'ENSEA.

Même inachevé, le projet démontre une réelle utilité : automatiser le suivi des composants électroniques, réduire les erreurs de gestion de stock et faciliter les commandes sont des apports directs pour les techniciens et les étudiants qui utilisent les tiroclasses au quotidien.

Ce projet nous a également permis de monter en compétences sur des technologies variées : conception PCB, communication SPI, développement logiciel et gestion de projet en équipe. Il constitue une base que d'autres promotions pourraient reprendre et faire évoluer vers un système pleinement opérationnel.

   
