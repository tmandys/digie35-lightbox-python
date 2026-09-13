import time
from machine import Pin
import lib.resource as res

class DigitalInput:
    """General debounced Digital Input (DIN)."""

    def __init__(self, resource_id: int, event_dispatcher, debounce_ms: int = 50, active_low: bool = True):
        # active_low=True means Log 0 on pin = active state (1)
        self.pin = Pin(res.get_index(resource_id), Pin.IN, Pin.PULL_UP if active_low else Pin.PULL_DOWN)
        self.resource_id = resource_id
        self.dispatch = event_dispatcher
        self.debounce_ms = debounce_ms
        self.active_low = active_low

        # Načtení výchozího stavu
        self.state = self._read_state()
        self.last_raw_state = self.state
        self.last_change_time = time.ticks_ms()

    def _read_state(self) -> int:
        val = self.pin.value()
        return 1 if (val == 0 if self.active_low else val == 1) else 0

    def update(self):
        current_raw = self._read_state()
        current_time = time.ticks_ms()

        if current_raw != self.last_raw_state:
            self.last_raw_state = current_raw
            self.last_change_time = current_time
        elif time.ticks_diff(current_time, self.last_change_time) >= self.debounce_ms:
            if current_raw != self.state:
                self.state = current_raw
                self.dispatch(self.resource_id, res.ACTION_SET_VALUE, state=self.state)