from .connection import NHCConnection
from .light import NHCLight
from .cover import NHCCover
from .fan import NHCFan
import json
import asyncio
import inspect

class NHCController:
    def __init__(self, host, port):
        self._host = host
        self._callback = []
        self._port = port | 8000
        self._connection = NHCConnection(host, self.port)
        self._actions: list[NHCLight | NHCCover | NHCFan] = []
        self._locations = {}

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

        self.start_events()

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def locations(self):
        return self._locations

    @property
    def system_info(self):
        return self._system_info

    @property
    def actions(self):
        return self._actions

    def add_callback(self, func):
        """Add callback function for events."""
        if inspect.isfunction(func):
            self._callback.append(func)
        else:
            raise Exception("Only use functions with 1 parameter as callback.")


    def _send(self, data):
        response = json.loads(self._connection.send(data))
        if 'error' in response['data']:
            error = response['data']['error']
            if error:
                raise Exception(error['error'])

        return response['data']

    def execute(self, id, value):
        return self._send('{"cmd": "%s", "id": "%s", "value1": "%s"}' % ("executeactions", str(id), str(value)))

    def start_events(self):
        """Start events."""
        self._listen_task = asyncio.create_task(self._listen())

    async def _listen(self):
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
                        for func in self._callback:
                            await func(data)
        finally:
            self._writer.close()
            await self._writer.wait_closed()
