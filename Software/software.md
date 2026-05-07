## Infos RFID
ID = emplacement sur RFID
MPN et SKU à partir du fichier excel

boîte et RFID indissociables + on part du principe qu'à une boîte=RFID correspond un emplacement: si on veut changer un composant de place on le change de boîte et on doit pouvoir modifier son emplacement sur le fichier excel

| format emplacement | salle | meuble | tiroir | colonne | ligne |
|--------:|-------  -|-----------|---------|-------|-------|
| max (entier/bits) taille | Patricia+D265/4 | tiro-class/4 | 9?/8 pour être sûrs | 12/4 | 8/4 |


## Fonctions à coder
### Fonctionnement PCB
rfid_init
rfid_reset
rfid_write
rfid_read
rfid_receive
rfid_transmit
rfid_transceive


Lecture infos:
- lecture tag RFID et transmission données à la STM
- décodage
- préparation données à transmettre en fonction de celles lues sur le tag
- transmission via USB au PC

Ecriture infos:
- transmission PC -> USB
- ...
- écriture sur le tag RFID

Enregistrement tag RFID (si nouveau par exemple) ...

### USB
AN 2.1.3 gestion Vusb après reset.

### Interface PC

## Pins à configurer
### Liste pins interconnectés
| Pin | Fonction | Composants connectés | Pins connectés | Source 1 | Commentaire 1 |Source 2 | Commentaire 2 |
|----:|----------|----------------------|-----------|----------|--------------|----------|--------------|
| PA5 | SPI1_SCK | STM32, RFID | SCLK: serial clock input | DS RFID | Schmitt-Trigger input | | |
| PA6 | SPI1_MISO | STM32, RFID | DIN: data input | DS RFID | Schmitt-Trigger input | RM STM| mode TI, CPOL= 0 ?, CPHA=1 |
| PA7 | SPI1_MOSI | STM32, RFID | DOUT: data output | DS RFID | open drain output with internal pull-up resistor | | |
| PA11 | USBDM | STM32, USB via protection diode | D- (A7, B7) | | | | |
| PA12 | USBDP | STM32, USB via protection diode | D+ (A6, B6) | | | | |
| PA13 | SWDIO | STM32, SWD conn | 4 | | | | |
| PA14 | SWCLK | STM32, SWD conn | 6 | | | | |
| PA15 | TDI | STM32, SWD conn | 10 | | | | |
| PB3 | TDO | STM32, SWD conn | 8 | | | | |
| NRST | NRST | STM32, SWD conn | 12 | | | | |
| PB4 | TRST | STM32, SWD conn | 3 | | | | |
| ? | VCP_IN | STM32, SWD conn | 13 | | | | |
| ? | VCP_OUT | STM32, SWD conn | 14 | | | | |

SPI1 in APB2 see 6.4.21 RM\
SPI -> 42 RM;
SPIx registers in 42.6 RM

### Liste pins autres
| Pin | Fonction | Composant connecté | Pins liés | Source 1 | Commentaire 1 |Source 2 | Commentaire 2 |
|----:|----------|----------------------|-----------|----------|--------------|----------|--------------|
| BOOT0 | BOOT0 | STM32 | | | | | |
| PH0 | OSC_IN | STM32 | | | | | |
| PH1 | OSC_OUT | STM32 | | | | | |


### Infos complémentaires
#### Lecture/Ecriture RFID
Incluant échange données avec PC.


Liste commandes dans DS_RFID 10:
- READ_TAG: recieved data at DOUT, to be decoded by uC
- WRITE_TAG(-N)
