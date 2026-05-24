/*
 * rfid.c
 *
 *  Created on: Apr 9, 2026
 *      Author: julie
 */
#include "rfid.h"

RFID_HandleTypeDef hrfid1; // definition hrfid1: port du lecteur RFID

void RFID_init(RFID_HandleTypeDef* hrfid,
		SPI_HandleTypeDef* hspi,
		GPIO_TypeDef* hspi_nss_port,
		uint16_t hspi_nss_pin,
		GPIO_TypeDef* rst_port,
		uint16_t rst_pin){
	// initialise structure RFID_HandleTypeDef avec les infos en parametre
	hrfid->hspi = hspi;
	hrfid->hspi_nss_port = hspi_nss_port;
	hrfid->hspi_nss_pin = hspi_nss_pin;
	hrfid->rst_port = rst_port;
	hrfid->rst_pin = rst_pin;


}

void RFID_transmit(RFID_HandleTypeDef* hrfid, uint8_t* data, int size){
	// transmet size premieres donnees stockees sur le tag en les enregistrant dans le buffer data
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, RESET); // active communication avec le slave lecteur hrfid (SPI)
	HAL_SPI_Transmit(hrfid->hspi, data, size, 500);
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, SET); // desactive communication
}

void RFID_receive(RFID_HandleTypeDef* hrfid, uint8_t* data, int size){
	// ecrit donnees data de taille size sur le lecteur RFID
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, RESET); // active communication avec le slave lecteur hrfid (SPI)
	HAL_SPI_Receive(hrfid->hspi, data, size, 500);
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, SET); // desactive communication
}

void RFID_transmit_receive(RFID_HandleTypeDef* hrfid, uint8_t* pTxData, uint8_t* pRxData, int size){
	// ecrit TxData puis lit et met dans RxData les donnees du tag
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, RESET); // active communication
	HAL_SPI_TransmitReceive(hrfid->hspi, pTxData, pRxData, size, 100);
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, SET); // desactive communication
}
