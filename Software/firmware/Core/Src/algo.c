/*
 * algo.c
 *
 *  Created on: Apr 9, 2026
 *      Author: julie
 */
#include "algo.h"

void test(){
	// teste fonctionnalites read/write
	// data buffer pour size infos lues du tag
	int size= 8;
	uint8_t data[size];
	// tableau log de taille sizeLog a ecrire dans le tag
	int sizeLog= 8;
	uint8_t log[sizeLog];
	log[0]= 0x03;
	log[1]= 0x05;
	log[4]= 0x07;
	
	// lecture tag, affichage de l'adresse de data
	read(&huart1, &hrfid1, data, size);
	printf("Received data at Ox%x.\r\n", data);
	// ecriture de log sur le tag, affichage de l'adresse du tableau log (pour verifier si modifie)
	write(&huart1, &hrfid1, log, sizeLog);
	printf("Wrote data at Ox%x.\r\n", log);
	
	// lecture du tag pour observer les modifications post-ecriture
	uint8_t readData[size];
	read(&huart1, &hrfid1, readData, size);
	// affichage adresse buffer readData et du premier hexa d'1 octet sur 2 en memoire depuis cette adresse
	printf("Read 'written' data stored at Ox%x.\r\n", readData);
	printf("%u, %u, %u, %u\r\n", readData[0], readData[4], readData[8], readData[12]);
}

void read(UART_HandleTypeDef* huart, RFID_HandleTypeDef* hrfid, uint8_t* pdata, int size){
	// lit tag hrfid, met size Bytes ds pdata buffer et envoie au PC via USB huart
	RFID_receive(hrfid, pdata, size); // recupere donnees stockees sur le tag
	HAL_UART_Transmit(huart, pdata, size, 500); // envoi via USART (USB)
}

void write(UART_HandleTypeDef* huart, RFID_HandleTypeDef* hrfid, uint8_t* pdata, int size){
	// ecrit infos recues du PC sur le tag
	HAL_UART_Receive(huart, pdata, size, 500); // recupere donnees recues de l'USB dans le buffer pdata
	RFID_transmit(hrfid, pdata, size); // enregistre pdata sur le tag 
}

uint8_t SPI1_WriteRead(uint8_t data, SPI_HandleTypeDef hspi1) {
    // ecrit data puis lit (en renvoie avec stock) les donnees sur le tag
    // n'inclut pas la liaison USART
    uint8_t stock;
    RFID_transmit_receive(&hspi1, &data, &stock, 1, HAL_MAX_DELAY);
    return stock;
}
