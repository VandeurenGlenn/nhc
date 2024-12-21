from .connection import NHCConnection
from .light import NHCLight
from .cover import NHCCover
from .fan import NHCFan
import json
import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

class NHCController:
    def __init__(self, host, port=8000) -> None:
        self._host: str = host
        self._port: int = port
        self._actions: list[NHCLight | NHCCover | NHCFan] = []
        self._locations: dict[str, str] = {}
        self._connection = NHCConnection(host, port)
        self._callbacks: dict[str, list[Callable[[int], Awaitable[None]]]] = {}

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
    
    async def connect(self) -> None:
        await self._connection.connect()

        actions = self._send('{"cmd": "listactions"}')
        locations = self._send('{"cmd": "listlocations"}')

        for location in locations:
            self._locations[location["id"]] = location["name"]

        # self._thermostats = self._send('{"cmd": "listthermostats"}')
        # self._energy = self._send('{"cmd": "listenergy"}')µ

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
                raise Exception(error['error'])
        return response['data']

    def execute(self, id: str, value: int) -> None:
        self._send('{"cmd": "%s", "id": "%s", "value1": "%s"}' % ("executeactions", str(id), str(value)))

    def update_state(self, id: str, value: int) -> None:
        """Update the state of an action."""
        for action in self._actions:
            if action.id == id:
                action.update_state(value)

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

    async def handle_event(self, event: dict[str, Any]) -> None:
        """Handle an event."""
        self.update_state(event["id"], event["value1"])
        await self.async_dispatch_update(event["id"], event["value1"])

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
                if "event" in message \
                        and message["event"] != "startevents":
                    for data in message["data"]:
                        await self.handle_event(data)
        finally:
            self._writer.close()
            await self._writer.wait_closed()
