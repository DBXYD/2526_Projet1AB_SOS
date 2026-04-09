/*
 * algo.c
 *
 *  Created on: Mar 13, 2026
 *      Author: julie
 */

#include "algo.h"

void setup (){
	RCC -> AHB2ENR |= 0x00000007 ; // activation GPIOA, GPIOB et GPIOC
	RCC->APB2ENR |= RCC_APB2ENR_SPI1EN;
	GPIOA->OSPEEDR |= (0x3F << 10);

	GPIOA-> MODER &= ~(0xFF << 8);// masque et pour PA4,PA5,PA6 et PA7
	GPIOA->MODER |= (0xA9 << 8); // masque ou pour PA4,PA5 et PA6 et PA7
	GPIOA-> MODER &= ~(0xFF << 22);// masque et pour PA11,PA12,PA13 et PA14
	GPIOA->MODER |= (0xAA << 22); // masque ou pour PA11,PA12,PA13 et PA14

	GPIOA->AFRH &= ~(0xFFF << 20);
	GPIOA->AFRH |= (0x555 << 20);
	GPIOA->AFRL &= ~(0xFFFF << 12);
	GPIOA->AFRL |= (0x00AA << 12);


	GPIOB -> MODER &= 0x01FFFFBF;// masque et
	GPIOB -> MODER |= 0x14000040; // masque ou

	GPIOC -> MODER &= 0xFFAEAAFF;// masque et
	GPIOC -> MODER |= 0x00515500; // masque ou


	SPI1->CR1 &= ~SPI_CR1_SPE;
	SPI1 -> CR1 &= ~(0x0003); // modification du bit dans CPHA en 0 modification du bit dans CPOL en 0

	SPI1 -> CR1 |= SPI_CR1_MSTR;


	SPI1-> CR1 |= (0x03 << 3); // modification des bits 5:3 pour f_clk/16

	SPI1 -> CR1 |= SPI_CR1_SSM;
	SPI1 -> CR1 |= SPI_CR1_SSI;

	SPI1 -> CR1 |= SPI_CR1_SPE;

	SPI1->CR2 |= (0x7 << 8);
	SPI1->CR2 |= SPI_CR2_FRXTH;


}

uint8_t SPI1_Transfer(uint8_t data) {
    while (!(SPI1->SR & SPI_SR_TXE));

    SPI1->DR = data;

    while (!(SPI1->SR & SPI_SR_RXNE));

    return SPI1->DR;


}

void loop(){
	HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_6);
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_7) //
}

