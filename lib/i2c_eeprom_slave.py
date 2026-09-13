from machine import mem32, Pin
import lib.resource as res
import config

class EEPROM24LC02Slave:
    """Emulates a 24LC02 (256-byte) EEPROM via RP2040 HW I2C registers."""

    # Registry pro I2C1
    I2C1_BASE = 0x40048000
    IC_CON = I2C1_BASE + 0x00
    IC_TAR = I2C1_BASE + 0x04
    IC_SAR = I2C1_BASE + 0x08
    IC_DATA_CMD = I2C1_BASE + 0x10
    IC_RAW_INTR_STAT = I2C1_BASE + 0x34
    IC_CLR_RD_REQ = I2C1_BASE + 0x50
    IC_ENABLE = I2C1_BASE + 0x6C
    IC_STATUS = I2C1_BASE + 0x6E

    def __init__(self, resource_id: int, event_dispatcher):
        scl_pin, sda_pin = res.get_index2(resource_id)
        self.addr = res.get_subtype(resource_id)
        self.resource_id = resource_id
        self.dispatch = event_dispatcher

        # 256 B buffer
        self.memory = bytearray(256)
        self.ptr = 0  # current address pointer
        self.first_byte_received = False

        # Načtení výchozích identifikačních dat desky
        self._load_board_identity()

        # HW Init
        Pin(sda_pin, Pin.IN, Pin.PULL_UP)
        Pin(scl_pin, Pin.IN, Pin.PULL_UP)
        
        mem32[self.IC_ENABLE] = 0
        mem32[self.IC_SAR] = self.addr
        mem32[self.IC_CON] = 0x20  # Target Mode, 7-bit addr
        mem32[self.IC_ENABLE] = 1

    def _load_board_identity(self):
        """Předvyplnění identifikační hlavičky desky v EEPROM."""
        # Příklad: Vlastní struktura nebo Linux Hat Spec / Vendor data
        header = b"digie35-lightbox-v1.0-SN2026001"
        self.memory[0:len(header)] = header

    def update(self):
        """I2C communication handling."""
        status = mem32[self.IC_STATUS]

        # 1. ČTENÍ (Pico posílá data do Mastera)
        if status & 0x20:  # RD_REQ (Read Request interrupt)
            # Pošleme bajt z aktuálního ukazatele a posuneme ho
            mem32[self.IC_DATA_CMD] = self.memory[self.ptr]
            mem32[self.IC_CLR_RD_REQ]  # Vyčištění přerušení
            self.ptr = (self.ptr + 1) & 0xFF  # Autoinkrement (0-255)

        # 2. ZÁPIS (Pico přijímá data od Mastera)
        elif status & 0x08:  # RX FIFO not empty
            val = mem32[self.IC_DATA_CMD] & 0xFF

            if not self.first_byte_received:
                # První bajt zápisu nastavuje pointer v EEPROM!
                self.ptr = val
                self.first_byte_received = True
            else:
                # Další bajty jsou samotná zapisovaná data
                self._write_byte(self.ptr, val)
                self.ptr = (self.ptr + 1) & 0xFF

        else:
            # Sběrnice je v klidu -> reset příznaku prvního bajtu
            self.first_byte_received = False

    def _write_byte(self, offset: int, value: int):
        """Zápis do emulované paměti a reakce na události."""
        # Ochraňujeme hlavičku (0x00 - 0x1F) jako READ-ONLY
        if offset < 0x20:
            return

        self.memory[offset] = value

        # Mapování: Zápis na adresy 0x20 až 0x25 přímé řízení LED 0 až 5!
        if 0x20 <= offset <= 0x25:
            led_index = offset - 0x20
            res_id = config.RES_PWM_LEDS[led_index]
            # Předáme událost změny jasu přes centrální handle_event
            self.dispatch(res_id, res.ACTION_SET_VALUE, value)