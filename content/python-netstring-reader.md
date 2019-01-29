Title: Quick hacks: Python netstring reader
Date: 2008-05-15 13:34
Category: Coding
Slug: python-netstring-reader
Status: published

I'm writing a proof-of-concept server for a less jokey version of the [SRGP]({filename}/srgp.md). The protocol is more or less SRGP, but it doesn't use MIME-style headers each request is made up of a series of [netstrings](http://cr.yp.to/proto/netstrings.txt). The header and body sections are terminated with empty netstrings, i.e., `0:,`.

The proof-of-concept server is being written in Python. Here's the netstring reader generator function, in case it might be of use to somebody else out there:

```python
class MalformedNetstringError:
    pass


def netstring_reader(f):
    while True:
        n = ""
        while True:
            c = f.read(1)
            if c == '':
                return
            if c == ':':
                break
            if len(n) > 10:
                raise MalformedNetstringError
            if c == '0' and n == '':
                # We can't allow leading zeros.
                if f.read(1) != ':':
                    raise MalformedNetstringError
                n = c
                break
            n += c
        n = int(n, 10)
        payload = f.read(n)
        if len(payload) < n:
            return
        if f.read(1) != ',':
            raise MalformedNetstringError
        yield payload
```

`netstring_reader()` takes a [file object](https://docs.python.org/2.4/lib/bltin-file-objects.html) and returns a generator that returns each netstring extracted from the file object. If the stream is malformed, a `MalformedNetstringError` is raised.

Currently the diagnostics are far from as good as they ought to be. It should state whether it's a malformed length or a missing terminating comma, and the offset into the stream where the error occurred. There's a few places where it can be made more robust, but expect that in later releases.

Here's an example of it in use.

```python
f = open("sample.dat", "r")
try:
    for i in netstring_reader(f):
        print i
finally:
    f.close()
```
