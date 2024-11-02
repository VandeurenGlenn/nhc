from .connection import NHCConnection
from .entities import NHCLight, NHCCover, NHCFan
import logging
import json
import asyncio

_LOGGER = logging.getLogger(__name__)

class NHCController:
    def __init__(self, host, port):
        self.host = host
        self.port = port | 8000
        self._connection = NHCConnection(host, self.port)
        self._entities: list[NHCLight | NHCCover | NHCFan] = []

        actions = self._send('{"cmd": "listactions"}')
        self._locations = self._send('{"cmd": "listlocations"}')
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
              self._entities.append(entity)

        _LOGGER.debug('Controller initialized')

    @property
    def locations(self):
        return self._locations

    @property
    def system_info(self):
        return self._system_info

    @property
    def entities(self):
        return self._entities

    def _event_handler(self, event):
        """Handle events."""
        _LOGGER.debug("Event: %s", event)
        if (self.event_handler) is not None:
            self.event_handler(event)

    def _send(self, data):
        response = json.loads(self._connection.send(data))
        if 'error' in response['data']:
            _LOGGER.warning(response['data']['error'])
            error = response['data']['error']
            if error:
                raise Exception(error['error'])

        return response['data']

    def execute(self, id, value):
        return self._send('{"cmd": %s, "id": %s, "value1": %s}' % ("executeactions", str(id), str(value)))

    def start_events(self):
        """Start events."""
        self._listen_task = asyncio.create_task(self.listen())

    async def listen(self):
        """Listen for events."""
        s = '{"cmd":"startevents"}'
        reader, writer = await asyncio.open_connection(self._host, self._port)

        writer.write(s.encode())
        await writer.drain()

        async for line in reader:
            try:
                message = json.loads(line.decode())
                _LOGGER.debug("Received: %s", message)
                if message != "b\r":
                    if "event" in message and message["event"] == "listactions":
                        for _action in message["data"]:
                            self._event_handler(_action)
            except any:
                _LOGGER.debug("exception")
                _LOGGER.debug(line)

