A slightly deeper dive into monads
==================================

:date: 2016-05-06 02:29
:category: Coding
:status: draft

If you look at the interface definition for a monad, the most important
operation is called 'bind'. This is, more or less, the equivalent of the
semicolon, albeit with some minor caveat, which I'm going to explain here.

I'll borrow some syntax from Haskell to help with this. In the following,
when I write ``\x -> 2 * x``, I'm defining an anonymous function that takes
a single argument, `x`, doubles it, and returns that as a result.
