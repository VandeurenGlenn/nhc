class NHCThermostat():
    def __init__(self, data):
        self._id = data["id"]
        self._state = data["measured"]
        self._wanted = data["setpoint"]
        self._mode = data["mode"]
        self._overrule = data["overrule"]
        self._overruletime = data["overruletime"]
        self._ecosave = data["ecosave"]
        
    @property
    def state(self):
        return self._state
    
    @property
    def wanted(self):
        return self._wanted
    
    @property
    def mode(self):
        return self._mode
    
    @property
    def overrule(self):
        return self._overrule
    
    @property
    def overruletime(self):
        return self._overruletime
    
    @property
    def ecosave(self):
        return self._ecosave
    
    def update_state(self, data):
        self._state = data["measured"]
        self._wanted = data["setpoint"]
        self._mode = data["mode"]
        self._overrule = data["overrule"]
        self._overruletime = data["overruletime"]
        self._ecosave = data["ecosave"]

