Title: Picking up Lua again
Slug: picking-up-lua
Category: Coding
Date: 2020-05-17 21:44
Status: published

I recently resurrected my old original Raspberry Pi B+ and installed NetBSD on
it. Currently, it's acting as a bastion for my local network, but I've been
thinking of other projects I could do with it. One of those is to build
something like [Pi-Hole](https://pi-hole.net/) with it, as practically
everything needed is part of the the base system, as it come with both BIND 9
and Unbound, ISC dhcpd, sqlite3, bozohttpd, and Lua in the base system.

The first time I looked at Lua, was, I think, in the late '90s or early 2000s,
when I downloaded a pretty early version of the interpreter built for RISC OS.
It looked nice enough as a language, but I set it aside as it didn't really let
me do much with it out of the box. I'm not sure if I understood the point of
the language at the time, though I later grew to appreciate that aspect of it.
Not that I've ever had a huge need for embedding an interpreter in any of my
projects since then.

With this ad/DNS blackholing project, I figured I'd revisit it. What surprised
me is just how _little_ it seems to have changed over the years, at least on
the surface, and there are some very odd omissions from the the basic set of
libraries.

The first one that struck me is that there's no built-in way to print a table.
Best as I can tell, tables have no default implementation for the `__tostring`
metamethod, nor even a way to do so built into the debug library. If only to
help with debugging, it seems like an odd omission when the overhead would be
minimal.

Second is that there's a weird lack of policy where it would be convenient.
Particularly, it would be very nice if Lua supplied the few tens of lines of
code needed to implement classes consistently. It's one thing to favour
mechanism over policy, but when the policy would be cheap, easy, and
convenient, it seems silly not to provide it.

The lack of a basic test framework seems like an odd omission to me. It's the
kind of thing that's invaluable during development, but isn't going to add any
overhead in an embedded environment.

Alongside that is a lack of some basic application support functions, like an
implementation of something like `getopt`.

It would be nice to have built-in support for some very simple configuration
format like INI files, but that's not the end of the world.

I really miss not having an `in` operator for checking against a list of
values, the behaviour of `#` with tables is rather weird, as is how `nil`
interacts with them. I can see both of those biting me on the ass sooner or
later, and badly.

I think, though, that the oddest choice is `os.execute`, because it's
straight-up dangerous. Rather than taking a table of command-line arguments, it
takes a string, meaning that if you're shelling out to, say, execute `curl`,
you're performing a potentially risky operation.

I've found some ways to compensate for these issues, if need be. The
[Penlight](http://tieske.github.io/Penlight/) library looks like it'd help a
lot, and [luaposix](http://luaposix.github.io/luaposix/) looks like it should
cover most of my other needs, if need be.

Still, these odd omissions aside, it seems fine so far. Maybe this'll be the
thing that gets me to revisit using AwesomeWM on some low-powered device again.
After all, I've a Raspberry Pi 4 on the way.
