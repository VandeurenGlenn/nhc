from .action import NHCBaseAction

class NHCThermostat(NHCBaseAction):
    def __init__(self, controller, data):
        super().__init__(controller, data)
        self._measured = data["measured"]
        self._setpoint = data["setpoint"]
        self._overrule = data["overrule"]
        self._overruletime = data["overruletime"]
        self._ecosave = data["ecosave"]
    
    @property
    def measured(self):
        return self._measured

    @property
    def setpoint(self):
        return self._setpoint
    
    @property
    def mode(self):
        return self._state
    
    @property
    def overrule(self):
        return self._overrule
    
    @property
    def overruletime(self):
        return self._overruletime
    
    @property
    def ecosave(self):
        return self._ecosave
    
    def set_mode(self, mode):
        self._controller.execute_thermostat(self.id, mode, self._overruletime, self._overrule, self._setpoint)

    def set_temperature(self, setpoint):
        self._controller.execute_thermostat(self.id, self._state, self._overruletime, self._overrule, setpoint)
    
    def update_state(self, data):
        super().update_state(data)
        self._setpoint = data["setpoint"]
        self._measured = data["measured"]
        self._overrule = data["overrule"]
        self._overruletime = data["overruletime"]
        self._ecosave = data["ecosave"]

