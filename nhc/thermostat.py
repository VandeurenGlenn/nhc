from .action import NHCBaseAction

class NHCThermostat(NHCBaseAction):
    def __init__(self, controller, data):
        super().__init__(controller, data)
        self._measured = data["measured"]
        self._wanted = data["setpoint"]
        self._overrule = data["overrule"]
        self._overruletime = data["overruletime"]
        self._ecosave = data["ecosave"]
    
    @property
    def measured(self):
        return self._measured

    @property
    def wanted(self):
        return self._wanted
    
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
        self._controller.execute_thermostat(self.id, mode, self._overruletime, self._overrule, self._wanted)

    def set_temperature(self, wanted):
        self._controller.execute_thermostat(self.id, self._state, self._overruletime, self._overrule, wanted)
    
    def update_state(self, data):
        self._state = data["mode"]
        self._wanted = data["setpoint"]
        self._measured = data["measured"]
        self._overrule = data["overrule"]
        self._overruletime = data["overruletime"]
        self._ecosave = data["ecosave"]

