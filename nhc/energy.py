class NHCEnergy():
    def __init__(self, channel, state):
        self._channel = channel
        self._state = state
        
    @property
    def state(self):
        return self._state
    
    def update_state(self, state):
        self._state = state
