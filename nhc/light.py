from typing import Optional
from .action import NHCAction

class NHCLight(NHCAction):

    @property
    def is_on(self) -> bool:
        """Is on."""
        return self._state > 0

    async def turn_on(self, brightness: Optional[int] = None) -> None:
        """Turn On."""
        if (brightness is None):
            if self.is_dimmable:
                brightness = 254
            else:
                brightness = self._state if self._state > 0 else 100
        else:
            brightness = round(brightness / 2.55)
        await self._controller.execute(self.id, brightness)

    async def turn_off(self) -> None:
        """Turn off."""
        value = 0
        if self.is_dimmable:
            value = 255
        await self._controller.execute(self.id, value)

    async def toggle(self) -> None:
        """Toggle on/off."""
        if self.is_on:
            await self.turn_off()
        else:
            await self.turn_on()
