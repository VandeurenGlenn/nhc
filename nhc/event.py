class NHCEvent:
  def __init__(self, action):
    self._id = action["id"]
    self._value1 = action["value1"]
    self._value2 = action["value2"]

  @property
  def id(self):
    return self._id

  @property
  def value1(self):
    return self._value1

  @property
  def value2(self):
    return self._value2
