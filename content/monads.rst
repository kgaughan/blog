What monads are
===============

:date: 2016-05-06 03:00
:category: Coding
:status: published

It's almost like a rite of passage for a developer to write a monad tutorial.

Well, this isn't a monad tutorial. This is simply an effort to put an end to
some of the nonsense that leads to monad tutorials being written in the first
place and all the magical woo surrounding what is actually a very mundane topic
every developer in the world understands, but simply doesn't realise they do.

And let's not use silly metaphors for any of this. Analogies, yes, but no
metaphors.

Say I have the following expression::

    1 + 2

Because the type of the values on each side of the ``+`` operators is an
integer, we know that the ``+`` refers to integer addition, and thus the answer
will be '3'.

Now, let's say that our language allows operators to be overloaded, and one of
the meanings of ``+`` is concatenation. Thus in the following expression, ``+``
means list concatenation::

    [1, 2, 3] + [4, 5, 6]

With me so far? Now's the bit where I blow your minds. Look at this::

    ;

That's a semicolon, which in many languages is used as a statement separator.
If you tilt your head a bit, you'll see that it can also be thought of as an
operator, thus in the following::

    3 + 4; 5 + 6

The semicolon is acting as an operator that joins two expressions together and
evaluates them in a particular order. It's really no different from ``+`` in
that regard.

So, what determines the behaviour of ``;`` when though of as an operator?
Nothing really, except that the languages we use assume that it behaves a
particular way. However, if we can vary the behaviour of ``+`` depending on the
type of the expressions on either side, why can't we do the same with ``;``?
This is what a monad does: it's a type that lets you determine the behaviour of
the semicolons---or your language's equivalent---as you need to.

If you've got this far and understand everything, then you understand what's
most essential about monads. Congratulations!

Now, stop reading and writing monad tutorials.

There's a bit more to it, and I may cover those details in a future post, but
suffice it to say that if you're looking for the closest useful equivalent of
the semicolon as an operator in a monad type/typeclass, you're looking for
what's referred to as `bind`, or `>>=`. The related `join` or `>>`
operator/method is a more direct equivalent, but `join` can be implemented in
terms of `bind`: `join` is just `bind`, but you're throwing away the result of
the expression.
