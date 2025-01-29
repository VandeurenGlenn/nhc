from .errors import UnknownError, ToManyRequestsError
from .connection import NHCConnection
from .light import NHCLight
from .cover import NHCCover
from .fan import NHCFan
from .energy import NHCEnergy
from .thermostat import NHCThermostat
import json
import asyncio
from collections.abc import Awaitable, Callable
from typing import Any
from .events import NHCActionEvent, NHCEnergyEvent, NHCThermostatEvent
import logging

_LOGGER = logging.getLogger('nikohomecontrol')

class NHCController:
    def __init__(self, host, port=8000) -> None:
        self._host: str = host
        self._port: int = port
        self._actions: list[NHCLight | NHCCover | NHCFan] = []
        self._locations: dict[str, str] = {}
        self._energy: dict[str, NHCEnergy] = {}
        self._thermostats: dict[str, NHCThermostat] = {}
        self._system_info: dict[str, Any] = {}
        self._connection = NHCConnection(host, port)
        self._callbacks: dict[str, list[Callable[[int], Awaitable[None]]]] = {}
        self.jobs = []
        self.jobRunning = False

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def locations(self) -> dict[str, str]:
        return self._locations

    @property
    def system_info(self) -> dict[str, Any]:
        return self._system_info

    @property
    def actions(self) -> list[NHCLight | NHCCover | NHCFan]:
        return self._actions
    
    @property
    def lights(self) -> list[NHCLight]:
        lights: list[NHCLight] = []
        for action in self._actions:
            if action.is_light is True or action.is_dimmable is True:
                lights.append(action)
        return lights
    
    @property
    def covers(self) -> list[NHCCover]:
        covers: list[NHCCover] = []
        for action in self._actions:
            if action.is_cover is True:
                covers.append(action)
        return covers
    
    @property
    def fans(self) -> list[NHCFan]:
        fans: list[NHCFan] = []
        for action in self._actions:
            if action.is_fan is True:
                fans.append(action)
        return fans
    
    @property
    def thermostats(self) -> dict[str, Any]:
        return self._thermostats
    
    @property
    def energy(self) -> dict[str, Any]:
        return self._energy
    
    def jobHandler(self):
        '''Handle the job queue'''
        if len(self.jobs) > 0 and not self.jobRunning:
            self.jobRunning = True
            _LOGGER.debug(f"jobRunning: {self.jobRunning}")
            job = self.jobs.pop(0)
            job()
            self.jobRunning = False
            _LOGGER.debug(f"jobRunning: {self.jobRunning}")
            self.jobHandler()

    async def connect(self) -> None:
        await self._connection.connect()

        actions = self._send('{"cmd": "listactions"}')
        locations = self._send('{"cmd": "listlocations"}')

        for location in locations:
            self._locations[location["id"]] = location["name"]

        for thermostat in self._send('{"cmd": "listthermostat"}'):
            entity =  NHCThermostat(self, thermostat)
            self._thermostats[entity.id] = entity

        for energy in self._send('{"cmd": "listenergy"}'):
            entity = NHCEnergy(self, energy)
            self._energy[entity.id] = entity

        self._system_info = self._send('{"cmd": "systeminfo"}')

        for (_action) in actions:
            entity = None
            if (_action["type"] == 1 or _action["type"] == 2):
                entity = NHCLight(self, _action)
            elif (_action["type"] == 3):
                entity = NHCFan(self, _action)
            elif (_action["type"] == 4):
                entity = NHCCover(self, _action)
            if (entity is not None):
                self._actions.append(entity)

        self._listen_task = asyncio.create_task(self._listen())
        
    def _send(self, data) -> dict[str, Any] | None:
        response = json.loads(self._connection.send(data))
        if 'error' in response['data']:
            error = response['data']['error']
            if error:
                if error == 100:
                    raise Exception("NOT_FOUND")
                if error == 200:
                    raise ToManyRequestsError(error)
                if error == 300:
                    raise Exception("ERROR")
                raise UnknownError(error)
        return response['data']

    def execute(self, id: str, value: int) -> None:
        """Add an action to jobs to make sure only one command happens at a time."""
        _LOGGER.debug(f"execute: {id} {value}")
        def job():
            self._send('{"cmd": "%s", "id": "%s", "value1": "%s"}' % ("executeactions", str(id), str(value)))
        
        self.jobs.append(job)
        _LOGGER.debug(f"jobs: {self.jobs}")
        _LOGGER.debug(f"jobRunning: {self.jobRunning}")
        if not self.jobRunning:
            self.jobHandler()

    def execute_thermostat(self, id: int, mode: int, overruletime: str, overrule: int, setpoint: int) -> None:
        """Add an action to jobs to make sure only one command happens at a time."""
        def job():
            self._send('{"cmd": "%s", "id": %s, "mode": "%s", "overruletime": "%s", "overrule": %s, setpoint: %s}' % ("executethermostat", id, mode, str(overruletime), overrule, setpoint))
        
        self.jobs.append(job)

        if not self.jobRunning:
            self.jobHandler()

    def register_callback(
        self, action_id: str, callback: Callable[[int], Awaitable[None]]
    ) -> Callable[[], None]:
        """Register a callback for entity updates."""
        self._callbacks.setdefault(action_id, []).append(callback)

        def remove_callback() -> None:
            self._callbacks[action_id].remove(callback)
            if not self._callbacks[action_id]:
                del self._callbacks[action_id]

        return remove_callback

    async def async_dispatch_update(self, action_id: str, value: int) -> None:
        """Dispatch an update to all registered callbacks."""
        for callback in self._callbacks.get(action_id, []):
            await callback(value)

    async def handle_event(self, event: NHCActionEvent) -> None:
        """Handle an event."""
        for action in self._actions:
            if action.id == event["id"]:
                _LOGGER.debug(f"update_state for: {action}")
                action.update_state(event["value1"])
      
        await self.async_dispatch_update(event["id"], event["value1"])

    async def handle_energy_event(self, event: NHCEnergyEvent) -> None:
        """Handle an energy event."""
        _LOGGER.debug(f"energy: {self._energy}")
        _LOGGER.debug(f"handle_energy_event: {event}")
        id = f"energy-{event['channel']}"
        self._energy[id].update_state(event["v"])
        await self.async_dispatch_update(id, event["v"])

    async def handle_thermostat_event(self, event: NHCThermostatEvent) -> None:
        """Handle an energy event."""
        _LOGGER.debug(f"thermostat: {self._thermostats}")
        _LOGGER.debug(f"handle_thermostat_event: {event}")
        id = f"thermostat-{event['id']}"
        self._thermostats[id].update_state(event)
        await self.async_dispatch_update(id, event)

    async def _listen(self) -> None:
        """
        Listen for events. When an event is received, call callback functions.
        """
        s = '{"cmd":"startevents"}'

        try:
            self._reader, self._writer = \
                await asyncio.open_connection(self._host, self._port)

            self._writer.write(s.encode())
            await self._writer.drain()

            async for line in self._reader:
                message = json.loads(line.decode())
                _LOGGER.debug(f"message: {message}")
                if "event" in message and message["event"] != "startevents":
                    # The controller also sends energy and thermostat events, so we make sure we handle those separately
                    _LOGGER.debug(f"message: {message}")
                    # The controller also sends energy and thermostat events, so we make sure we handle those separately
                    if message["event"] == "getlive":
                        _LOGGER.debug(f"getlive: {message}")
                        await self.handle_energy_event(message["data"])
                    elif message["event"] == "listthermostat":
                        _LOGGER.debug(f"listthermostat: {message}")
                        for data in message["data"]:
                            await self.handle_thermostat_event(data)
                    else:
                        for data in message["data"]:
                            await self.handle_event(data)
        finally:
            self._writer.close()
            await self._writer.wait_closed()
