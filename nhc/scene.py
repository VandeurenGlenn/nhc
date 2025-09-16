from .action import NHCAction

class NHCScene(NHCAction):

    async def activate(self) -> None:
        """Turn On."""
        await self._controller.execute(self.id, 255)