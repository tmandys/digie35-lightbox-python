# digie35-lightbox-python
MicroPython firmware for controlling a Lightbox within the **digie35** system, powered by Raspberry Pi Pico (RP2040).

## Features
- Control of 6x LED channels using high-frequency PWM (90 kHz, 16-bit resolution).
- Rotary encoder input for adjusting brightness and settings.
- Push-button input with software time debouncing.
- 2x I2C buses (Master channel + OLED Display).
- Externalized pin configuration in `config.py` to prevent hardcoded IOs.

## Project Structure
- `main.py` – Entry point and main execution loop.
- `config.py` – GPIO pins, PWM frequencies, and timing settings.
- `lib/hardware.py` – Object-oriented hardware abstraction layer.

## Requirements & Setup
1. Install **MicroPython** on your Raspberry Pi Pico.
2. Upload all `.py` files to the Pico (using VS Code with the MicroPico extension, Thonny, or `mpremote`).
