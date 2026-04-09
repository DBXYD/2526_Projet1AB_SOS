/*
 * rfid.c
 *
 *  Created on: Apr 9, 2026
 *      Author: julie
 */
#include "rfid.h"

RFID_HandleTypeDef hrfid1;

void RFID_init(RFID_HandleTypeDef* hrfid,
		SPI_HandleTypeDef* hspi,
		GPIO_TypeDef* hspi_nss_port,
		uint16_t hspi_nss_pin,
		GPIO_TypeDef* rst_port,
		uint16_t rst_pin){

	hrfid->hspi = hspi;
	hrfid->hspi_nss_port = hspi_nss_port;
	hrfid->hspi_nss_pin = hspi_nss_pin;
	hrfid->rst_port = rst_port;
	hrfid->rst_pin = rst_pin;


}

void RFID_transmit(RFID_HandleTypeDef* hrfid, uint8_t* data, int size){
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, RESET);
	HAL_SPI_Transmit(hrfid->hspi, data, size, 100);
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, SET);
}

void RFID_receive(RFID_HandleTypeDef* hrfid, uint8_t* data, int size){
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, RESET);
	HAL_SPI_Receive(hrfid->hspi, data, size, 100);
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, SET);
}

void RFID_transmit_receive(RFID_HandleTypeDef* hrfid, uint8_t* pTxData, uint8_t* pRxData, int size){
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, RESET);
	HAL_SPI_TransmitReceive(hrfid->hspi, pTxData, pRxData, size, 100);
	HAL_GPIO_WritePin(hrfid->hspi_nss_port, hrfid->hspi_nss_pin, SET);
}
