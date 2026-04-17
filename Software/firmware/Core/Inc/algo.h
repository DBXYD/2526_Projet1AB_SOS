/*
 * algo.h
 *
 *  Created on: Apr 9, 2026
 *      Author: julie
 */

#ifndef INC_ALGO_H_
#define INC_ALGO_H_

#include "main.h"
#include "rfid.h"

void test();
void read(RFID_HandleTypeDef* hrfid, uint8_t* pdata, int size);
void write(RFID_HandleTypeDef* hrfid, uint8_t* pdata, int size);
uint8_t SPI1_WriteRead(uint8_t data, SPI_HandleTypeDef hspi1);

#endif /* INC_ALGO_H_ */
