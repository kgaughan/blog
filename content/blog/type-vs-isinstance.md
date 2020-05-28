Title: type() vs. isinstance() in Python
Slug: type-vs-isinstance
Date: 2010-08-31 17:47
Category: Coding
Status: published

One elementary error people make is using the `type()` function where `isinstance()` would be more appropriate[^caveat].

If you're checking to see if an object has a certain type, you want `isinstance()` as it checks to see if the object passed in the first argument is of the type of any of the type objects passed in the second argument. Thus, it works as expected with subclassing and old-style classes, all of which have the legacy type object `instance`.

`type()`, on the other hand, simply returns the type object of an object and comparing what it returns to another type object will only yield `True` when you use the _exact_ same type object on both sides.

By way of example, here's what happens when subclassing `dict`:

```text
>>> foo = {}

>>> type(foo)
<type 'dict'>

>>> class MyDict(dict):
...     pass

>>> bar = MyDict()

>>> type(bar)
<class '__main__.MyDict'>

>>> type(bar) == dict
False                     # Unexpected result

>>> isinstance(bar, dict)
True                      # Expected result
```

As you can see, `isinstance()` gives the result you're more likely to want.

[^caveat]: Though use of `isinstance()` is typically a marker of a flawed design and itself [ought to be avoided if possible](http://www.canonical.org/~kragen/isinstance/).
