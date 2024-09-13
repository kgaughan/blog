Title: Starting with asyncio
Date: 2024-09-12 23:14
Slug: starting-with-asyncio-1
Category: Coding, Projects, Python
Status: published
Series: Starting with asyncio

I have an old project called [uwhoisd](https://pypi.org/project/uwhoisd/) from a previous life. It's been about eight years since I last did anything significant with it. It's now largely obsolete owing to the ICANN policy changes partially forced by the GDPR, but I'd like to use it as a vehicle for learning Python's [asyncio](https://docs.python.org/3/library/asyncio.html) library.

This won't be a tutorial. This will be me feeling my way through things and later retrofitting uwhoisd to use asyncio rather than [Tornado](https://www.tornadoweb.org/en/stable/).

Here was my first try:

```python
import asyncio


async def daemon_task(name: str, delay: float = 1.0):
    while True:
        print(f"Hello from {name}")
        await asyncio.sleep(delay)


async def main():
    task1 = asyncio.create_task(daemon_task("first", delay=0.2))
    task2 = asyncio.create_task(daemon_task("second", delay=0.3))
    await asyncio.sleep(1)
    print("Waiting...")
    await asyncio.wait([task1, task2], timeout=None)


if __name__ == "__main__":
    asyncio.run(main())
```

Simple enough. The idea was that I wanted to see if I could spawn some background tasks. The one bit I spent longer than I should've on was that I didn't realise that the `main()` function needed to be coloured `async` for even `asyncio.create_task(daemon_task())` to work. Once I'd realised that, here's what it spat out:

```
Hello from first
Hello from second
Hello from first
Hello from second
Hello from first
Hello from second
Hello from first
Hello from first
Hello from second
Waiting...
Hello from first
Hello from first
Hello from second
Hello from first
Hello from second
Hello from first
...
```

About what I'd expected, given the sleeps.

As `uwhoisd` is a daemon, implementing [`asyncio.loop.create_server`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.create_server) seems like the next logical step. I misread the documentation and expected this to be a module, but it's not. Instead, you call [`asyncio.get_running_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_running_loop). A simple echo server makes sense to start with, but here's one with nothing filled in:

```python
import asyncio


class EchoProtocol(asyncio.Protocol):
    pass


async def main():
    server = asyncio.get_running_loop().create_server(
        protocol_factory=EchoProtocol,
        host="localhost",
        port=8007,
        reuse_port=True,
    )
    await asyncio.wait_for(task, timeout=None)


if __name__ == "__main__":
    asyncio.run(main())
```

That ran, but also exited immediately. I should've read the [example echo server](https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-server), which also demonstrates how [protocols](https://docs.python.org/3/library/asyncio-protocol.html#protocols) work.

What caught me by surprise most of all here is that you have to `await` the return value from `create_server`. The next version actually stayed running:

```python
import asyncio


class EchoProtocol(asyncio.Protocol):
    pass


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

(You might be wondering "Keith, why didn't you think to call `server.serve_forever()` in the first place?" Well, that's because I leaned on VS Code's intellisense a little too hard, and without the `await`, it gave nothing of use. And yes, I should've looked at the docs and noticed that the API works just the same as [`socketserver`](https://docs.python.org/3/library/socketserver.html)...)

While simply running `await server.serve_forever()` seems like it should be enough, [`Server`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.Server) objects are context managers and using them with `async with` means they'll be cleaned up properly.

Protocols seem pretty similar to the old asyncore `dispatcher` class, albeit somewhat more abstracted away from the underlying network I/O.

I updated `EchoProtocol` with something simple to show that it was receiving data:

```python
class EchoProtocol(asyncio.Protocol):
    def __init__(self):
        pass

    def data_received(self, data: bytes) -> None:
        print(f"received [{data}]")
```

After spinning up a telnet client, I typed in some nonsense and got this:

```console
$ python3 -m aiotest
received [b'fdasfdskl\r\n']
received [b'jklfdsa\r\n']
received [b'kflds\r\n']
received [b'ffdsafdsafdsafdsafdsafdsafsdafd...lafjkdalfjsda\r\n']
```

Which is enough to show that things are behaving how I'd expect.

Next up, I'll need to implement a parent class that supports 'chat'-style protocols, such as SMTP and WHOIS, but that can wait for tomorrow.
