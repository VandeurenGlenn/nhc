import __future__

from ..action import NHCAction
from ..event import NHCEvent
from ..const import PRESET_MODES

class NHCFan(NHCAction):
  def __init__(self, controller, action):
    super().__init__(controller, action)

  @property
  def mode(self) -> str:
    for mode, value in PRESET_MODES.items():
        if value == self._state:
            return mode

  def set_mode(self, speed: str) -> NHCEvent:
      return self._controller.execute(self.action_id, PRESET_MODES[speed])
