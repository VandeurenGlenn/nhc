#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
nhcconnection.py

This is a tool to communicate with Niko Home Control.

You will have to provide an IP address and a port number.

License: MIT https://opensource.org/licenses/MIT
Source: https://github.com/NoUseFreak/niko-home-control
Author: Dries De Peuter
"""
import asyncio
import nclib
from .const import DEFAULT_PORT

NHC_TIMEOUT = 2000

class NHCConnection:
    """ A class to communicate with Niko Home Control. """
    def __init__(self, ip: str, port: int = DEFAULT_PORT):
        self._socket = None
        self._ip = ip
        self._port = port

    async def connect(self):
        """
        Connect to the Niko Home Control.
        """
        try:
            loop = asyncio.get_event_loop()
            self._socket = await loop.run_in_executor(None, nclib.Netcat, (self._ip, self._port), False)
            self._socket.settimeout(NHC_TIMEOUT)
        except Exception as e:
            self._socket = None
            raise ConnectionError(f"Failed to connect: {e}")

    async def disconnect(self):
        """
        Disconnect from the Niko Home Control.
        """
        if self._socket is not None:
            try:
                await asyncio.get_event_loop().run_in_executor(None, self._socket.shutdown, 1)
            except Exception as e:
                print(f"Failed to disconnect: {e}")
            finally:
                self._socket = None

    async def receive(self):
        """
        Receives information from the Netcat socket.
        """
        try:
            return await asyncio.get_event_loop().run_in_executor(None, self._socket.recv).decode()
        except Exception as e:
            print(f"Failed to receive data: {e}")
            return None

    async def read(self):
        return await self._receive_until(b'\r')

    async def _receive_until(self, s):
        """
        Receive data from the socket until the given substring is observed.
        Data in the same datagram as the substring, following the substring,
        will not be returned and will be cached for future receives.
        """
        try:
            data = b""
            while True:
                chunk = await asyncio.get_event_loop().run_in_executor(None, self._socket.recv)
                if s in chunk:
                    data += chunk[:chunk.find(s)]
                    break
                data += chunk
            return data.decode()
        except Exception as e:
            print(f"Failed to receive until {s}: {e}")
            return None

    def __del__(self):
        if self._socket is not None:
            asyncio.get_event_loop().run_until_complete(self.disconnect())
