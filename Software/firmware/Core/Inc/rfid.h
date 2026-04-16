/*
 * rfid.h
 *
 *  Created on: Apr 9, 2026
 *      Author: julie
 */

#ifndef INC_RFID_H_
#define INC_RFID_H_

#include "spi.h"
#include "gpio.h"

typedef struct {
	SPI_HandleTypeDef* hspi;
	GPIO_TypeDef* hspi_nss_port;
	uint16_t hspi_nss_pin;
	GPIO_TypeDef* rst_port;
	uint16_t rst_pin;
} RFID_HandleTypeDef;

extern RFID_HandleTypeDef hrfid1;


void RFID_init(RFID_HandleTypeDef* hrfid,
		SPI_HandleTypeDef* hspi,
		GPIO_TypeDef* hspi_nss_port,
		uint16_t hspi_nss_pin,
		GPIO_TypeDef* rst_port,
		uint16_t rst_pin);
void RFID_transmit(RFID_HandleTypeDef* hrfid, uint8_t* data, int size);
void RFID_receive(RFID_HandleTypeDef* hrfid, uint8_t* data, int size);
void RFID_transmit_receive(RFID_HandleTypeDef* hrfid, uint8_t* pTxData, uint8_t* pRxData, int size);

#endif /* INC_RFID_H_ */
