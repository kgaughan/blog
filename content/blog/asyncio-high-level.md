Title: A high-level asyncio server and client
Date: 2024-10-21 23:42
Slug: asyncio-high-level
Category: Coding, Projects, Python, Asyncio
Status: published
Series: Starting with asyncio

Life got in the way of me publishing anything for the last month, but I was able to [convert uwhoisd to use asyncio](https://github.com/kgaughan/uwhoisd/pull/45). That PR has a lot more in it aside form the code to switch from Tornado to asyncio. Here, I'll just cover how the echo server and client would be converted to use the [high-level API](https://docs.python.org/3/library/asyncio-api-index.html).

Here's the server:

```python
import asyncio


async def handle_request(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while True:
        line = await reader.readuntil(b"\r\n")
        if line == b".\r\n":
            break
        writer.write(line)
        await writer.drain()
    writer.close()


async def main():
    svr = await asyncio.start_server(handle_request, host="localhost", port=8007)
    async with svr:
        await svr.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
```

Quite a bit simpler! `StreamReader` and `StreamWriter` are doing all the heavy lifting the protocol classes in the low-level versions were doing. `StreamReader` has a `readline` method, but I'm explicitly expecting a CRLF. Arguably, there should be a timeout on the read, and if we wanted to (and should in anything even remotely production-worthy), we'd do this:

```python
        try:
            line = await asyncio.wait_for(reader.readuntil(b"\r\n"), timeout=30)
        except asyncio.TimeoutError:
            break
```

That'll cause the server to disconnect from a client after 30 seconds of inactivity.

Here's the client:

```python
import asyncio


async def echo_client():
    reader, writer = await asyncio.open_connection(host="localhost", port=8007)
    while True:
        writer.write(input().encode())
        writer.write(b"\r\n")
        await writer.drain()

        try:
            line = await reader.readuntil(b"\r\n")
        except asyncio.IncompleteReadError:
            break
        print(line.decode().rstrip())
    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(echo_client())
```

The `await writer.drain()` waits until everything in the `StreamWriter` is flushed and sent to the client. The `asyncio.IncompleteReadError` is raised if the server timed out while we were waiting on `input()` or explicitly closed the connection.
