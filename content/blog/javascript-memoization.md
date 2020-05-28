Title: Memoization in JavaScript
Date: 2005-07-21 23:16
Slug: javascript-memoization
Category: Coding
Status: published

About a fortnight ago, I was poking around the copy of [Perl](http://www.perl.com/) sitting on my laptop. I came across [Memoize.pm](http://perl.plover.com/Memoize/). Having read [the article that inspired it](http://perl.plover.com/MiniMemoize/memoize.html) a few years back, I thought I'd take an attempt at implementing something to do the same in JavaScript.

[Memoization](http://en.wikipedia.org/wiki/Memoization) is a method of increasing the speed of slow [referentially transparent](http://en.wikipedia.org/wiki/Referential_transparency) functions by caching their arguments and results. This trades a marginal amount of memory space for a potentially huge gain in speed.

Take the canonical definition of the [Fibonacci sequence](http://en.wikipedia.org/wiki/Fibonacci_number), for instance:

```javascript
function Fib(n) {
    if (n < 2) {
        return n;
    }
    return Fib(n - 1) + Fib(n - 2);
}
```

As you can guess, this quickly becomes quite slow once you start using numbers greater than around 20. Once you're dealing with numbers in the mid-thirties range, it cripples the computer.

The solution is to memoize the function. You can either do it by hand:

```javascript
var IterMemoFib = function() {
    var cache = [1, 1];
    var fib = function(n) {
        if (n >= cache.length) {
            for (var i = cache.length; i <= n; i++) {
                cache[i] = cache[i - 2] + cache[i - 1];
            }
        }
        return cache[n];
    }

    return fib;
}();
```

Which is a wee bit of a pain and not exactly readable; or you can get the computer to do it for you:

```javascript
Fib = Fib.memoize();
```

Due to technical (browser security) constraints, the arguments for memoized functions can only be arrays or scalar values. No objects.

The code extends the Function object to add the memoization functionality. If the function is a method, then you can pass the object into `memoize()`.

```javascript
Function.prototype.memoize = function() {
    var pad  = {};
    var self = this;
    var obj  = arguments.length > 0 ? arguments[i] : null;

    var memoizedFn = function() {
        // Copy the arguments object into an array: allows it to be used as
        // a cache key.
        var args = [];
        for (var i = 0; i < arguments.length; i++) {
            args[i] = arguments[i];
        }

        // Evaluate the memoized function if it hasn't been evaluated with
        // these arguments before.
        if (!(args in pad)) {
            pad[args] = self.apply(obj, arguments);
        }

        return pad[args];
    }

    memoizedFn.unmemoize = function() {
        return self;
    }

    return memoizedFn;
}

Function.prototype.unmemoize = function() {
    alert("Attempt to unmemoize an unmemoized function.");
    return null;
}
```

## Elsewhere

* [One-Line JavaScript Memoization](http://osteele.com/archives/2006/04/javascript-memoization).
* [Timed Memoization](http://blog.stevenlevithan.com/archives/timed-memoization) - A trivial extension when you want the cached values to be garbage collected after a while. If JavaScript supported [weak references](http://en.wikipedia.org/wiki/Weak_reference), they'd also be useful in allowing the garbage collector to periodically collect memoized results.
