# --- CATEGORY MASKS (Bits 24-31) ---
CAT_BUTTON  = 0x01_00_00_00
CAT_ENCODER = 0x02_00_00_00      # a/b
CAT_LED_PWM = 0x03_00_00_00
CAT_DIG_OUT = 0x04_00_00_00
CAT_DIG_IN  = 0x05_00_00_00
CAT_DISPLAY = 0x06_00_00_00
CAT_I2C_SLAVE = 0x07_00_00_00    # addr/sda/scl
CAT_SYSTEM  = 0xFF_00_00_00

# --- BIT MASKS ---
MASK_CATEGORY  = 0xFF_00_00_00
MASK_SUBTYPE   = 0x00_FF_00_00
MASK_RESERVED  = 0x00_00_FF_00
MASK_INDEX = 0x00_00_00_FF

# --- BUTTON & INPUT ACTIONS ---
ACTION_NONE         = 0x00
ACTION_PRESS        = 0x01  # button press (edge)
ACTION_RELEASE      = 0x02  # button release
ACTION_SHORT_CLICK  = 0x03  # short press
ACTION_LONG_PRESS   = 0x04  # long press 
ACTION_REPEAT       = 0x05  # repeat when pressed
ACTION_DOUBLE_CLICK = 0x06  # double click

# --- ROTARY & VALUE ACTIONS ---
ACTION_ROTATE       = 0x10
ACTION_SET_VALUE    = 0x11

def make_resource_id(category: int, index: int, subtype: int = 0, index2: int = 0) -> int:
    """Helper function to construct a 32-bit Resource ID."""
    return (category & MASK_CATEGORY) | ((subtype & 0xFF) << 16) | (index & 0xFF)

def get_category(resource_id: int) -> int:
    """Extract category mask from Resource ID."""
    return (resource_id & MASK_CATEGORY)

def get_subtype(resource_id: int) -> int:
    """Extract subtype from Resource ID."""
    return (resource_id & MASK_SUBTYPE) >> 16

def get_index(resource_id: int) -> int:
    """Extract pin or channel index from Resource ID."""
    return resource_id & MASK_INDEX

def get_index2(resource_id: int) -> tuple:
    """Extract two indexis from Resource ID."""
    return (resource_id & MASK_INDEX, (resource_id >> 8) & MASK_INDEX)

def decode_i2c_packet(packet: bytes):
    """Decodes a 6-byte I2C packet into (resource_id, action, param)."""
    if len(packet) < 6:
        return None, None, None
    res_id = (packet[0] << 24) | (packet[1] << 16) | (packet[2] << 8) | packet[3]
    action = packet[4]
    param = packet[5]
    return res_id, action, param