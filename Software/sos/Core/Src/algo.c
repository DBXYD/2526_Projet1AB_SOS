/*
 * algo.c
 *
 *  Created on: Mar 13, 2026
 *      Author: julie
 */

#include "algo.h"

void setup (){
	RCC -> AHB2ENR |= 0x00000007 ; // activation GPIOA
	GPIOA -> MODER &= 0xF1BF99FF;// masque et
	GPIOA -> MODER |= 0x04405500; // masque ou
	GPIOB -> MODER &= 0x01FFFFBF;// masque et
	GPIOB -> MODER |= 0x14000040; // masque ou
	GPIOC -> MODER &= 0xFFAEAAFF;// masque et
	GPIOC -> MODER |= 0x00515500; // masque ou


	SPI1 -> CR1 &= ~(0x0003); // modification du bit dans CPHA en 0 modification du bit dans CPOL en 0

	SPI1 -> CR1 |= SPI_CR1_MSTR;


	SPI1-> CR1 |= (0x02 << 3); // modification des bits 5:3 pour f_clk/8

	SPI1 -> CR1 |= SPI_CR1_SSM;
	SPI1 -> CR1 |= SPI_CR1_SSI;

	SPI1 -> CR1 |= SPI_CR1_SPE;




}

void loop(){
	HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_6);
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_7) //
}

