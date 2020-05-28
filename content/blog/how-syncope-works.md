Title: How Syncope Works
Date: 2006-02-01 01:30
Category: Coding
Status: published

[Note from 2020: Syncope eventually ended up as [AFK](https://github.com/kgaughan/afk)]

Here's how Syncope, the kinda-but-not-really-a-framework I mentioned before, works. It's really just a library with a bunch of canned request lifecycles. Those are the only parts of it that vaguely resemble a framework. It's made to be as simple and unobtrusive as it possibly could be. If you don't like the way some part of it works, you can swap it out for something that suits you better.

It doesn't try to be like [Rails](http://www.rubyonrails.org/), [Django](http://www.djangoproject.com/), or anything like that. They're fine, but the way in which they work doesn't really fit well with PHP. I really don't understand the ongoing Rails envy PHP developers have [[1](http://phpontrax.com/), [2](https://web.archive.org/web/20060214234803/http://bennolan.com/biscuit/), [3](http://cakephp.org/)]. The whole point of Syncope is to play to PHP's strengths.

## Overview

The core of it is the _Pipeline_ class, which takes some bit of data (string, array, object, it doesn't care) and runs a bunch of filter objects on it. The only requirement for a class to be a filter is that it have a method called _execute()_, which takes the pipeline object and the data being passed along as argument and calls _do_next() _on the pipeline to execute the next filter on the pipeline._

## Web Lifecycle Outline

The filters starting with _Simple_ are just that: simple versions that work as simply as possible, almost moronically so. For example, the view code uses plain old PHP templates and the request filter just ensures that the action parameter is well-formed and implements an IE workaround to emulate a lot of the `<button>` tag's functionality with multiple regular `input>` buttons.

*   An instance of the `Pipeline` class is instantiated.
*   The filters below are registered with the `Pipeline` object, and the `$_REQUEST` array is passed to its `start()` method.
*   `SimpleRequestFilter` processes this to extract the action to run.
*   `ExecutionTimeFilter` benchmarks the rest of the pipeline.
*   `SimpleSessionFilter` starts the session (using PHP's default session handler).
*   `SimpleCommandDispatchFilter` works out which file in the site's `actions` directory to execute based on the value of the `action` element in the object passed along and the HTTP request verb. If it can't be serviced, it triggers either a _404 Not Found_ or a _405 Method Not Allowed_.
*   If the pipeline hasn't been stopped at this point, `DefaultViewFilter` runs. This pulls in some static content.

## Other Bits And Pieces

In addition to the above, it also has an `XmlBuilder` class I wrote a while back to make building feeds and other XML documents less painful for myself. Using templates for them doesn't make an awful lot of sense to me unless there's no better way to do it.

There's also a bunch of helper functions covering a bunch of things I keep on having to do in templates and elsewhere.

## Stuff To Do

While the stuff outlined above covers a lot of the annoying boilerplate I've ended up writing in the past, there's a few ancilliary things I'd like to add to the library.

*   A base class for making alternative session serialisation stratagies easier to write. I'll also write a filter class using this to implement database session serialisation. It's low priority.
*   [Formkey]({filename}formkeys.md) generation and validation. Formkeys make forms that have them one-shot, helping to avoid double submits, makes programmatic submission of forms a little more difficult, helps prevent spoofing of credentials, and can be used for throttling overactive posters. I have some ColdFusion code that does this already and though it's no panacea, it's _very_ useful. This is medium priority, but I'd really like this sometime.
*   Some simple authentification code. High priority, but only because I need it for something I'm doing right now. I'll probably use something from PEAR though.
*   Role-based authorisation. Also high priority, but I'll probably find something for doing this on PEAR too.
*   PHPUnit coverage. For my sins, there isn't any just yet, and there really should be.

Things that would be important if others wanted to use it would be:

*   Support for command modules might be a good idea. Where this would be useful is it would allow all the handlers in a group of action handlers to be held in one file rather than spreading them out over multiple ones.

What I'm _not_ going to do is write yet another ORM library. The fact I'm writing a library like Syncope _at all_ is bad enough.

**Update:** I forgot to mention that code for caching HTML fragments (or anything like it) is also something I'm intending on writing. I just have to figure out how exactly to handle the dependencies between the various fragments.
