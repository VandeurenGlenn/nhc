class NHCAction:
    """A Niko Action."""

    def __init__(self, controller, action):
        """Init Niko Action."""
        self._state = action["value1"]
        self._action_id = action["id"]
        self._type = action["type"]
        self._name = action["name"]
        self._controller = controller
        self._suggested_area = controller.locations[action["location"]]

    @property
    def state(self):
        """A Niko Action state."""
        return self._state

    @property
    def suggested_area(self):
        """A Niko Action location."""
        return self._suggested_area

    @property
    def name(self):
        """A Niko Action state."""
        return self._name

    @property
    def action_id(self):
        """A Niko Action action_id."""
        return self._action_id

    @property
    def action_type(self):
        """The Niko Action type."""
        return self._type

    def is_light(self) -> bool:
        """Is a light."""
        return self.action_type == 1

    def is_dimmable(self) -> bool:
        """Is a dimmable light."""
        return self.action_type == 2

    def is_fan(self) -> bool:
        """Is a fan."""
        return self.action_type == 3

    def is_cover(self) -> bool:
        """Is a cover."""
        return self.action_type == 4

    def update_state(self, state):
        """Update state."""
        self._state = state
