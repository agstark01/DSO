#include <stdint.h>

// Simple STM32F103C8T6 test code for Wokwi addon in VS Code.
// Uses the popular STM32 "Blue Pill" board with a 72 MHz system clock.

#define RCC_APB2ENR   (*(volatile uint32_t *)0x40021018)
#define RCC_APB2ENR_IOPCEN (1 << 4)

#define GPIOC_CRH     (*(volatile uint32_t *)0x40011004)
#define GPIOC_ODR     (*(volatile uint32_t *)0x4001100C)

static void delay(volatile uint32_t count)
{
    while (count--) {
        __asm__("nop");
    }
}

int main(void)
{
    // Enable GPIOC peripheral clock
    RCC_APB2ENR |= RCC_APB2ENR_IOPCEN;

    // Configure PC13 as general purpose push-pull output, max speed 2 MHz.
    GPIOC_CRH &= ~(0xF << ((13 - 8) * 4));
    GPIOC_CRH |=  (0x2 << ((13 - 8) * 4));

    while (1) {
        // Toggle onboard LED on PC13
        GPIOC_ODR ^= (1 << 13);
        delay(3000000);
    }

    return 0;
}
