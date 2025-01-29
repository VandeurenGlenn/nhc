
class NHCBaseAction:
    """A Niko Base Action."""
    _name: str
    _id: int
    _suggested_area: str | None = None
    _state: str | int = None
    _type: int = None

    def __init__(self, controller, action):
        """Init Niko Base Action."""
        self._name = action["name"]
        self._controller = controller
        
        if ("channel" in action) and (action["channel"] is not None):
            self._id = f"energy-{action["channel"]}"
        elif ("mode" in action) and (action["mode"] is not None):
            self._id = f"thermostat-{action["id"]}"
        else:
            self._id = action["id"]

        if ("value1" in action):
            self._state = action["value1"]
        elif ("v" in action):
            """This is a energy action."""
            self._state = action["v"]
        elif ("mode" in action):
            """This is a thermostat action."""
            self._state = action["mode"]
        
        if ("type" in action):
            self._type = action["type"]

        if (
            "location" in action
            and action["location"] is not None
            and action["location"] != ""
        ):
            self._suggested_area = controller.locations[action["location"]]

    
    @property
    def state(self):
        """A Niko Action state."""
        return self._state
    
    @property
    def type(self):
        """The Niko Action type."""
        return self._type

    @property
    def suggested_area(self):
        """A Niko Action location."""
        return self._suggested_area

    @property
    def name(self):
        """A Niko Action state."""
        return self._name

    @property
    def id(self):
        """A Niko Action action_id."""
        return self._id
    
    def update_state(self, state):
        """Update state."""
        self._state = state

class NHCAction(NHCBaseAction):
    """A Niko Action."""

    @property
    def is_light(self) -> bool:
        """Is a light."""
        return self.type == 1

    @property
    def is_dimmable(self) -> bool:
        """Is a dimmable light."""
        return self.type == 2

    @property
    def is_fan(self) -> bool:
        """Is a fan."""
        return self.type == 3

    @property
    def is_cover(self) -> bool:
        """Is a cover."""
        return self.type == 4

class NHCEnergyAction(NHCBaseAction):
    """A Niko Energy Action."""
    
    @property
    def is_import(self) -> bool:
        """Is a import energy."""
        return self.type == 1 | self.type == 0
    
    @property
    def is_export(self) -> bool:
        """Is a export energy."""
        return self.type == 2