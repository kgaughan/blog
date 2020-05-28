Title: Minesweeper Kata
Date: 2009-01-03 10:19
Category: Coding
Status: published

I did the [minesweeper kata](http://codingdojo.org/kata/Minesweeper/) a few days back. It was a bit _too_ easy, though it's quite possible that this is more an artifact of how I approached it. Given that it's a simple one, it might be an idea to see if I can take it in smaller steps, _much_ smaller steps.

There's not really much to say, so here's the code:

```python
#!/usr/bin/env python

import doctest
import sys


def unpack_line(s):
    """
    >>> unpack_line('.....')
    [0, 0, 0, 0, 0]
    >>> unpack_line('')
    []
    >>> unpack_line('.*.')
    [0, '*', 0]
    """
    line = []
    for c in s:
        if c == '*':
            line.append('*')
        else:
            line.append(0)
    return line


def mark_adjacents(lines):
    """
    >>> mark_adjacents([[0, 0], [0, 0]])
    [[0, 0], [0, 0]]
    >>> mark_adjacents([['*', 0], [0, 0]])
    [['*', 1], [1, 1]]
    >>> mark_adjacents([['*', 0], [0, '*']])
    [['*', 2], [2, '*']]
    >>> mark_adjacents([[0, 0, 0], [0, '*', 0], [0, 0, 0]])
    [[1, 1, 1], [1, '*', 1], [1, 1, 1]]
    >>> mark_adjacents([['*', 0, 0], [0, 0, 0], [0, 0, '*']])
    [['*', 1, 0], [1, 2, 1], [0, 1, '*']]
    """
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '*':
                for oy in [y - 1, y, y + 1]:
                    if oy < 0 or oy == len(lines):
                        continue
                    for ox in [x - 1, x, x + 1]:
                        if ox < 0 or ox == len(lines[y]):
                            continue
                        if lines[oy][ox] != '*':
                            lines[oy][ox] += 1
    return lines


def process_fields(iterable):
    start = True
    for line in iterable:
        line = line.rstrip()
        if start:
            start = False
            lines = []
            height, width = [int(x) for x in line.split(' ')]
            if width == 0 and height == 0:
                break
        else:
            lines.append(unpack_line(line))
            height -= 1
            if height == 0:
                start = True
                yield mark_adjacents(lines)


def main():
    field = 0
    for f in process_fields(sys.stdin):
        field += 1
        if field > 1:
            print
        print "Field #%d:" % field
        for l in f:
            print ''.join([str(x) for x in l])


def _test():
    doctest.testmod()


if __name__ == '__main__':
    main()
```

I should really buckle down and finish the code that's meant to replace the crappy one-evening hack the this blog runs on.
