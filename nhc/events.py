class NHCActionEvent:
    @property
    def value1(self) -> str:
        return self._value1
    
    @property
    def id(self) -> str:
        return self._id
    
    def __init__(self, event: str):
        self._id = event["id"]
        self._value1 = event["value1"]

class NHCEnergyEvent():
    @property
    def channel(self) -> str:
        return self._channel
    
    @property
    def v(self) -> str:
        return self._v
    
    def __init__(self, event: str):
        self._channel = event["channel"]
        self._v = event["v"]

class NHCThermostatEvent: 
    @property
    def mode(self) -> str:
        return self._mode
    
    @property
    def setpoint(self) -> str:
        return self._setpoint
    
    @property
    def measured(self) -> str:
        return self._measured
    
    @property
    def overrule(self) -> str:
        return self._overrule
    
    @property
    def overruletime(self) -> str:
        return self._overruletime
    
    @property
    def ecosave(self) -> str:
        return self._ecosave
    
    def __init__(self, event: str):
        self._mode = event["mode"]
        self._setpoint = event["setpoint"]
        self._measured = event["measured"]
        self._overrule = event["overrule"]
        self._overruletime = event["overruletime"]
        self._ecosave = event["ecosave"]