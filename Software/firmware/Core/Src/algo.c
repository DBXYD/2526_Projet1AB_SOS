/*
 * algo.c
 *
 *  Created on: Apr 9, 2026
 *      Author: julie
 */
#include "algo.h"

void test(){
	// read/write
	int size= 8;
	uint8_t data[size];
	int sizeLog= 8;
	uint8_t log[sizeLog];
	log[0]= 0x03;
	log[1]= 0x05;
	log[4]= 0x07;
	read(&hrfid1, data, size);
	printf("Received data at Ox%x.\r\n", data);
	write(&hrfid1, log, sizeLog);
	printf("Wrote data at Ox%x.\r\n", log);

	uint8_t readData[size*2];
	read(&hrfid1, readData, size);
	printf("Read 'written' data stored at Ox%x.\r\n", readData);
	printf("%u, %u, %u, %u\r\n", readData[0], readData[4], readData[8], readData[12]);
}

void read(UART_HandleTypeDef* huart, RFID_HandleTypeDef* hrfid, uint8_t* pdata, int size){
	// reads hrfid card, puts size Bytes in data buffer pdata and sends it to PC via USB huart
	RFID_receive(hrfid, pdata, size);
	HAL_UART_Transmit(huart, pdata, size, 500); //envoi USART (USB)
}

void write(UART_HandleTypeDef* huart, RFID_HandleTypeDef* hrfid, uint8_t* pdata, int size){
	HAL_UART_Receive(huart, pdata, size, 500); //avec données reçues de l'USB
	RFID_transmit(hrfid, pdata, size);
}

uint8_t SPI1_WriteRead(uint8_t data,SPI_HandleTypeDef hspi1) {
    uint8_t stock;
    HAL_SPI_TransmitReceive(&hspi1, &data, &stock, 1, HAL_MAX_DELAY);
    return stock;
}
