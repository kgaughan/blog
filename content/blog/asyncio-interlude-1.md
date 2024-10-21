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

Here's the finished client:

```python
import asyncio

from server import ChatProtocol


class ChatClientProtocol(ChatProtocol):
    def write_line(self, line: str) -> None:
        # This relies on the transport to flush appropriately.
        self.transport.write(line.encode())
        self.transport.write(self.delimiter)

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        super().connection_made(transport)
        self.write_line(input())

    def line_received(self, line: bytes) -> None:
        print(line.decode())
        self.write_line(input())


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


if __name__ == "__main__":
    asyncio.run(main())
```

And the server:

```python
import asyncio
import typing as t


class ChatProtocol(asyncio.Protocol):
    __slots__ = ["transport", "delimiter", "buffer"]

    def __init__(
        self,
        delimiter: bytes = b"\r\n",
        on_exit: t.Optional[asyncio.Future] = None,
    ):
        self.buffer = bytearray()
        self.start = 0  # Where we'll start the delimiter search from
        self.delimiter = delimiter
        self.on_exit = on_exit

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport: asyncio.Transport = transport  # type: ignore

    def data_received(self, data: bytes) -> None:
        self.buffer.extend(data)
        # The data that's received may contain multiple delimiters, so we try
        # to find each.
        while True:
            pos = self.buffer.find(self.delimiter, self.start)
            if pos == -1:
                # The delimiter hasn't been found, so next time we start checking
                # from the end of the buffer, just far enough back to match the
                # delimiter if a single byte is added.
                self.start = max(0, len(self.buffer) - len(self.delimiter) + 1)
                break
            # Split the buffer on the delimiter
            line, self.buffer = (
                self.buffer[:pos],
                self.buffer[pos + len(self.delimiter) :],
            )
            self.start = 0
            self.line_received(bytes(line))

    def line_received(self, line: bytes) -> None:
        pass

    def connection_lost(self, exc: Exception) -> None:
        if self.on_exit is not None:
            self.on_exit.set_result(True)


class ChatEchoProtocol(ChatProtocol):
    def line_received(self, line: bytes) -> None:
        if line == b".":
            self.transport.close()
        else:
            self.transport.write(b"You sent: ")
            self.transport.write(line)
            self.transport.write(self.delimiter)


async def main():
    server = await asyncio.get_running_loop().create_server(
        protocol_factory=ChatEchoProtocol,
        host="localhost",
        port=8007,
        reuse_port=True,
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
```
