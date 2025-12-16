Title: A simple asyncio client
Date: 2024-09-14 22:16
Slug: asyncio-client
Category: Coding, Projects, Python, Asyncio
Status: published
Series: Starting with asyncio

In [the last entry]({filename}asyncio-protocols.md), I implemented a 'chat'-style protocol. Using [`loop.create_connection()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.create_connection), I can reuse `ChatProtocol`, but with a different client implementation to allow some interactivity. I'm assuming the server is in the same directory as this file so `ChatProtocol` can be imported from it.

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
    await asyncio.get_running_loop().create_connection(
        protocol_factory=ChatClientProtocol,
        host="localhost",
        port=8007,
    )


if __name__ == "__main__":
    asyncio.run(main())
```

!!! note
    There's a silly bug here, and the fix is covered in [the next entry]({filename}asyncio-interlude-1.md).

This is far from perfect--it contains blocking code in the form of `input()`--but it's enough to get things working. If this were a real-life situation, the synchronous code would need to be [run in an executor](https://docs.python.org/3/library/asyncio-eventloop.html#executing-code-in-thread-or-process-pools), and that won't necessarily work for something like `input()`.

Here's the output:

```console
$ python3 client.py
Hello!
You sent: Hello!
This is a line.
You sent: This is a line.
This is another.
You sent: This is another.
.
```
The behaviour of the client is as expected.

I'm discarding the return value of `create_connection()`. It will yield a tuple consisting of the transport and protocol object that was instantiated, and you can potentially use these instead of doing everything in the protocol.

Next up, I'll rewrite everything to use the high-level APIs.
