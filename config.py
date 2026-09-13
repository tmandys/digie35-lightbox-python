
import lib.resources as res
from machine import Pin

KEY_LEFT = res.make_resource_id(res.CAT_BUTTON, 16)
KEY_RIGHT = res.make_resource_id(res.CAT_BUTTON, 20)
KEY_ESC = res.make_resource_id(res.CAT_BUTTON, 2)
KEY_TRIGGER = res.make_resource_id(res.CAT_BUTTON, 18)
KEY_ENTER = res.make_resource_id(res.CAT_BUTTON, 3)
KEY_ROTARY = res.make_resource_id(res.CAT_ENCODER, 15, index2: 17)

LED_WHITE_WARM = res.make_resource_id(res.CAT_LED_PWM, 19)
LED_WHITE_COLD = res.make_resource_id(res.CAT_LED_PWM, 7)
LED_RED = res.make_resource_id(res.CAT_LED_PWM, 4)
LED_GREEN = res.make_resource_id(res.CAT_LED_PWM, 5)
LED_BLUE = res.make_resource_id(res.CAT_LED_PWM, 6)
LED_IR = res.make_resource_id(res.CAT_LED_PWM, 21)

PWM_LEDS = [cfg.LED_WHITE_WARM, cfg.LED_WHITE_COLD, cfg.LED_RED, cfg.LED_GREEN, cfg.LED_BLUE, cfg.LED_IR]

# detect when external connector inserted
DIN_CONN_DETECT = res.make_resource_id(res.CAT_DIG_IN, 22)

# trigger action on external interface
DOUT_INT = res.make_resource_id(res.CAT_DIG_OUT, 19)

BUTTON_PINS = [KEY_LEFT, KEY_RIGHT, KEY_ESC, KEY_TRIGGER, KEY_ENTER)

# RP2040 PWM: 16-bit resolution (0-65535).
# 90 kHz frequency provides smooth dimming without audible noise or visible flicker.
PWM_FREQ = 90_000  # Hz
PWM_LED_PINS = [LED_WHITE_WARM, LED_WHITE_COLD, LED_RED, LED_GREEN, LED_BLUE, LED_IR]

I2C_MEMORY = res.make_resource_id(res.CAT_I2C_SLAVE, index=1, index2=0, subtype=0x57)


I2C2_SCL_PIN = 19
I2C2_SDA_PIN = 18
I2C2_FREQ = 400_000
DISP_WIDTH = 128
DISP_HEIGHT = 64

# --- INPUTS ---

BUTTON_DEBOUNCE_MS = 50
