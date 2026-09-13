# lib/i2c_slave.py
from machine import mem32, Pin
import config

class RP2040I2CSlave:
    """I2C Target/Slave implementation for RP2040 using HW registers."""
    
    # Adresy registrů pro I2C1 na RP2040
    I2C1_BASE = 0x40048000
    IC_CON = I2C1_BASE + 0x00
    IC_TAR = I2C1_BASE + 0x04
    IC_SAR = I2C1_BASE + 0x08
    IC_DATA_CMD = I2C1_BASE + 0x10
    IC_RAW_INTR_STAT = I2C1_BASE + 0x34
    IC_CLR_RD_REQ = I2C1_BASE + 0x50
    IC_ENABLE = I2C1_BASE + 0x6C
    IC_STATUS = I2C1_BASE + 0x6E

    def __init__(self, addr: int, sda_pin: int, scl_pin: int):
        self.addr = addr
        
        # Nastavení pinů pro I2C1
        Pin(sda_pin, Pin.IN, Pin.PULL_UP)
        Pin(scl_pin, Pin.IN, Pin.PULL_UP)
        
        # Vypnutí I2C1 před konfigurací
        mem32[self.IC_ENABLE] = 0
        
        # Nastavení adresy zařízení (SAR - Slave Address Register)
        mem32[self.IC_SAR] = self.addr
        
        # Konfigurace: Slave mode, 7-bit adresování
        mem32[self.IC_CON] = 0x20
        
        # Zapnutí I2C1
        mem32[self.IC_ENABLE] = 1

    def read_byte(self) -> int:
        """Read one byte from master (if data available)."""
        if mem32[self.IC_STATUS] & 0x08:  # RX FIFO not empty
            return mem32[self.IC_DATA_CMD] & 0xFF
        return None

    def write_byte(self, data: int):
        """Send 1 byte to master when read reaquest"""
        mem32[self.IC_DATA_CMD] = data & 0xFF