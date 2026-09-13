import time
from machine import Pin
import lib.resource as res

class ButtonHandler:
    """Button controller supporting Short Click, Long Press, and Auto-Repeat."""

    def __init__(self, resource_id: int, event_dispatcher, 
                 debounce_ms: int = 50, long_press_ms: int = 800, repeat_ms: int = 200):
        self.pin = Pin(res.get_index(resource_id), Pin.IN, Pin.PULL_UP)
        self.resource_id = resource_id
        self.dispatch = event_dispatcher

        self.debounce_ms = debounce_ms
        self.long_press_ms = long_press_ms
        self.repeat_ms = repeat_ms

        self.is_pressed = False
        self.press_time = 0
        self.last_repeat_time = 0
        self.long_press_triggered = False

    def update(self):
        """Call this method periodically in the main loop or via hardware timer."""
        current_time = time.ticks_ms()
        state = self.pin.value() == 0  # True when pressed (Active LOW / Pull-Up)

        # 1. Button Press Edge
        if state and not self.is_pressed:
            self.is_pressed = True
            self.press_time = current_time
            self.long_press_triggered = False
            self.dispatch(self.resource_id, res.ACTION_PRESS)

        # 2. Button Hold (Long Press & Repeat)
        elif state and self.is_pressed:
            duration = time.ticks_diff(current_time, self.press_time)

            # Check for Long Press trigger
            if duration >= self.long_press_ms and not self.long_press_triggered:
                self.long_press_triggered = True
                self.last_repeat_time = current_time
                self.dispatch(self.resource_id, res.ACTION_LONG_PRESS)

            # Check for Auto-Repeat while holding
            elif self.long_press_triggered:
                if time.ticks_diff(current_time, self.last_repeat_time) >= self.repeat_ms:
                    self.last_repeat_time = current_time
                    self.dispatch(self.resource_id, res.ACTION_REPEAT)

        # 3. Button Release Edge
        elif not state and self.is_pressed:
            duration = time.ticks_diff(current_time, self.press_time)
            self.is_pressed = False
            
            # Send RELEASE event
            self.dispatch(self.resource_id, res.ACTION_RELEASE)

            # If released before Long Press limit and after debounce, it's a Short Click
            if duration >= self.debounce_ms and not self.long_press_triggered:
                self.dispatch(self.resource_id, res.ACTION_SHORT_CLICK)
