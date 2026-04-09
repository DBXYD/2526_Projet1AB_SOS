/*
 * algo.c
 *
 *  Created on: Apr 9, 2026
 *      Author: julie
 */
#include "algo.h"


uint8_t SPI1_WriteRead(uint8_t data,SPI_HandleTypeDef hspi1) {
    uint8_t stock;
    HAL_SPI_TransmitReceive(&hspi1, &data, &stock, 1, HAL_MAX_DELAY);
    return stock;
}

