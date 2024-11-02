from ..action import NHCAction
from ..const import COVER_OPEN, COVER_CLOSE, COVER_STOP
from ..event import NHCEvent

class NHCCover(NHCAction):
    def __init__(self, controller, action):
        super().__init__(controller, action)

    @property
    def is_open(self):
        return self._state > 0

    def open(self) -> NHCEvent:
        return self._controller.execute(self.action_id, COVER_OPEN)

    def close(self) -> NHCEvent:
        return self._controller.execute(self.action_id, COVER_CLOSE)

    def stop(self) -> NHCEvent:
        return self._controller.execute(self.action_id, COVER_STOP)
