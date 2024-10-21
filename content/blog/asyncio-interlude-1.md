Title: asyncio: an interlude
Date: 2024-09-15 16:00
Slug: asyncio-interlude-1
Category: Coding, Projects, Python
Status: published
Series: Starting with asyncio

[Yesterday's entry]({filename}asyncio-clients.md) contained some issues I didn't notice until later. The main one is that after the initial successful test, I'd notice that the client would start to disconnect. There's no explicit timeout on the connections, so this might be either some underlying socket timeout or there's something else going on.

Essentially, it was working partly by accident, as can be see by partly fixing the main function:

```python
async def main():
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_connection(
        protocol_factory=ChatClientProtocol,
        host="localhost",
        port=8007,
    )
    transport.close()
```

The transport closes immedately! Essentially, there was an implicit timeout in `asyncio.run()` cause by the function returning. Awaiting on a future will fix that. Here are the updates to the `ChatProtocol` class:

```python
import asyncio
import typing as t


class ChatProtocol(asyncio.Protocol):

    def __init__(
        self,
        delimiter: bytes = b"\r\n",
        on_exit: t.Optional[asyncio.Future] = None,
    ):
        self.buffer = bytearray()
        self.start = 0  # Where we'll start the delimiter search from
        self.delimiter = delimiter
        self.on_exit = on_exit

    ...

    def connection_lost(self, exc: Exception) -> None:
        if self.on_exit is not None:
            self.on_exit.set_result(True)
```

It can now optionally accept a future to wait on to signal when the server connection is lost. The existing `ChatClientProtocol` class requires no additional updates, but here's the new main function for the client:

```python
async def main():
    loop = asyncio.get_running_loop()
    on_exit = loop.create_future()
    transport, _ = await loop.create_connection(
        protocol_factory=lambda: ChatClientProtocol(on_exit=on_exit),
        host="localhost",
        port=8007,
    )
    try:
        await on_exit
    finally:
        transport.close()
```

This makes sure that the client doesn't exit until such time as it gets a signal that it should exit when the server closes the connection.
