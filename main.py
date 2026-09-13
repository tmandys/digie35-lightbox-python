import time
from lib.hardware import LightboxHardware

def main():
    hw = LightboxHardware()
    print("Lightbox Pico initialized.")

    while True:
        # Main application execution loop
        time.sleep_ms(10)
        hw.update()

if __name__ == "__main__":
    main()