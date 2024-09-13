Title: Exploring asyncio protocols
Date: 2024-09-13 21:50
Slug: asyncio-protocols
Category: Coding, Projects, Python
Status: published
Series: Starting with asyncio

In [the last entry]({filename}starting-with-asyncio.md), I managed to get a very basic daemon running. Now I need to flesh out the initial `Protocol` implementation to first turn it into a proper echo server and then implement a simple parser for a 'chat'-style protocol.

The first bit is at least easy enough, but I need to get something I can write on, which means I need to implement `connection_made()`.

```python
import asyncio
import typing as t


class EchoProtocol(asyncio.Protocol):
    __slot__: t.ClassVar = ["transport"]

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport: asyncio.Transport = transport  # type: ignore

    def data_received(self, data: bytes) -> None:
        self.transport.write(data)
        self.transport.close()


async def main():
    server = await asyncio.get_running_loop().create_server(
        protocol_factory=EchoProtocol,
        host="localhost",
        port=8007,
        reuse_port=True,
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
```

(Type inference means I had some add some silly annotations to `connection_made`.)

This works as expected:

```console
$ telnet 127.0.0.1 8007
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
This should be repeated.
This should be repeated.
Connection closed by foreign host.
```

Next up, I'll need to implement some actual parsing of the data received. asyncio has a more high-level interface in the form of [`asyncio.start_server`](https://docs.python.org/3/library/asyncio-stream.html#asyncio.start_server) which has a more robust stream-based interface. I'll probably end up using that when I update _uwhoisd_, but right now I'm exploring the more low-level side of things specifically so I and understand what happens when something goes wrong.

'Chat'-style protocols are generally made up lines terminated by CRLFs. There's no guarantee that the client will flush its buffers right after every CRLF and may even perversely flush after each byte or a single line might not fit into the socket's buffer, so we need to maintain our own buffer so we can find where everything's delimited. In the interests of simplicity, I'm going to use a `bytearray` as the incoming buffer, though there may be faster mechanisms. Here's the result:

```python
import asyncio
import typing as t


class ChatProtocol(asyncio.Protocol):
    __slot__: t.ClassVar = ["transport", "delimiter", "buffer"]

    def __init__(self, delimiter: bytes = b"\r\n"):
        self.buffer = bytearray()
        self.start = 0  # Where we'll start the delimiter search from
        self.delimiter = delimiter

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
            line, self.buffer = self.buffer[:pos], self.buffer[pos + len(self.delimiter) :]
            self.start = 0
            self.line_received(bytes(line))

    def line_received(self, line: bytes) -> None:
        pass


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

This reads lines and echos them back until the client sends a line with a solitary fullstop, as which point the session is closed. Here's what a session looks like:

```console
$ telnet 127.0.0.1 8007
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
This is a line.
You sent: This is a line.
This is another line.
You sent: This is another line.
.
Connection closed by foreign host.
```

It mostly worked first time except for two things: I needed to clamp the lower bound of `self.start` with `max(0, ...)` as the delimiter can be more than one byte long, and the first time I wrote the code, I wrote `pos != -1` for some reason.

This should be enough for implementing the server. A more robust implementation might impose limits on how much data the buffer can consume, and the code for breaking the buffer in two can, no doubt, be made more efficient as it's likely doing a bunch of unnecessary copying.

Next up, I'll need some kind of a client that can interact with the server.
