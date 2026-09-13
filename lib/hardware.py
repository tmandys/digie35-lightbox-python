# lib/hardware.py
import time
from machine import Pin, PWM, I2C
import config as cfg
import lib.resource as res
import lib.button, lib.encoder
import lib.digital_input as din
import lib.i2c_memory_slave as mem

class LightboxHardware:
    """Hardware abstraction layer for the digie35 Lightbox controller."""

    def __init__(self):
        self.i2c_memory = mem.EEPROM24LC02Slave(cfg.I2C_MEMORY, event_handler=self.handle_event):
        
        #self.i2c_display = I2C(0, scl=Pin(config.I2C2_SCL_PIN), sda=Pin(config.I2C2_SDA_PIN), freq=config.I2C2_FREQ)


        # PWM LED Outputs
        self.pwms = {}
        for resource_id in cfg.PWM_LEDS:
            p = PWM(Pin(res.get_index(resource_id)))
            p.freq(config.PWM_FREQ)
            p.duty_u16(0)
            self.pwms{str(resource_id)} = p

        self.buttons = {}
        for resource_id in [cfg.KEY_LEFT, cfg.KEY_RIGHT, cfg.KEY_ESC, cfg.KEY_TRIGGER, cfg.KEY_ENTER]:
            self.puttons{string(resource_id)} = button.ButtonHandler(resource_id, event_handler=self.handle_event)

        self.rotary = encoder.RotaryEncoder(cfg.KEY_ROTARY, event_handler=self.handle_event)
        self.int_pin = Pin(cfg.DOUT_INT, Pin.OPEN_DRAIN, value=1)
        self.conn_detect = din.DigitalInput(cfg.DIN_CONN_DETECT, event_handler=self.handle_event)

    def handle_event(self, resource_id: int, action: int, *args, **kwargs):
        category = res.get_category(resource_id)
        print(f"ResourceID: 0x{resource_id:08X}, action: 0x{action:02X}, kwargs: {kwargs}, args: {args}")
        
    def set_led_brightness(self, resource_id: int, percent: float):
        """Set brightness for a specific LED channel (0.0 to 100.0%)."""
        duty = int((max(0.0, min(100.0, percent)) / 100.0) * 65535)
        self.pwms{string(resource_id}].duty_u16(duty)

    def set_int_signal(self, active: bool):
        """
        INT signalization control.
        :param active: True = pull to 0 (Active LOW), False = leave to Hi-Z
        """
        if active:
            self.int_pin.value(0)
        else:
            self.int_pin.value(1)

    def pulse_int_signal(self, duration_ms: int = 10):
        """Generate short pulse when pulling to 0."""
        self.int_pin.value(0)
        time.sleep_ms(duration_ms)
        self.int_pin.value(1)
        
    def update(self):
        for b in self.buttons:
            b.update()
        self.rotary.update()