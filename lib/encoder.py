from machine import Pin
import lib.resource as res

class RotaryEncoder:
    def __init__(self, resource_id: int, event_dispatcher):
        pins = red.get_index2(resource_id)
        self.clk = Pin(pin[0], Pin.IN, Pin.PULL_UP)
        self.dt = Pin(pin[1], Pin.IN, Pin.PULL_UP)

        self.resource_id = resource_id
        self.dispatch = event_dispatcher

        self.position = 0
        self.last_dispatched_position = 0

        # IRQ na sestupnou hranu CLK — extrémně rychlé a bezpečné
        self.clk.irq(trigger=Pin.IRQ_FALLING, handler=self._irq_handler)        
    
    def _irq_handler(self, pin):
        # When CLK goes to 0, get DT state rotation direction
        if self.dt.value() == 1:
            self.position += 1
        else:
            self.position -= 1
    
    def update(self):
        """Call from main loop"""
        diff = self.position - self.last_dispatched_position
        if diff != 0:
            self.last_dispatched_position = self.position
            # Odbavení události mimo IRQ kontext
            self.dispatch(self.resource_id, res.ACTION_ROTATE, diff)