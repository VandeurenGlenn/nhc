from .action import NHCAction
from .event import NHCEvent

class NHCLight(NHCAction):
    def __init__(self, controller, action):
        super().__init__(controller, action)

    @property
    def is_on(self):
        """Is on."""
        return self._state > 0

    def turn_on(self, brightness=255) -> NHCEvent:
        """Turn On."""
        return self._controller.execute(self.action_id, brightness)

    def turn_off(self) -> NHCEvent:
        """Turn off."""
        return self._controller.execute(self.action_id, 0)

    def toggle(self) -> NHCEvent:
        """Toggle on/off."""
        if self.is_on:
            return self.turn_off()

        return self.turn_on()
