from .action import NHCAction

class NHCLight(NHCAction):

    @property
    def is_on(self) -> bool:
        """Is on."""
        return self._state > 0

    def turn_on(self, brightness=255) -> None:
        """Turn On."""
        self._controller.execute(self.id, brightness)

    def turn_off(self) -> None:
        """Turn off."""
        self._controller.execute(self.id, 0)

    def toggle(self) -> None:
        """Toggle on/off."""
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()
