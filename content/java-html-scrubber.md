Title: A Java HTML Scrubber
Date: 2005-08-10 22:37
Slug: java-html-scrubber
Category: Coding
Status: published

In preparation for possibly adding a WYSIWYG editor to the site--mainly because people don't seem to read the formatting instructions--I've written the best part of a HTML scrubber to ensure that the HTML markup returned from the poster's browser doesn't contain anything dodgy and to attempt to ensure a minimal degree of validity and well-formedness to whatever gets posted up. It's written in Java, and I'll be wrapping it in a custom tag to make it easy for me to invoke from ColdFusion. It will, however, be usable from anything capable of instantiating a Java class.

It uses a simple [DSL](http://www.martinfowler.com/bliki/DomainSpecificLanguage.html) to describe which tags are allowed through, and which attributes are safe. It knows nothing about which tags can be nested within each other, or which are required. After all, it's a scrubber not a validator. The closest it comes is trying to balance tags which aren't.

As I said, it's mostly written. But what I'd like to know is if anybody else out there would find this useful, or if there's anything already out there like it. I've looked and I can't find anything like it, not written in Java anyway. But I don't see the point of writing it if somebody's already done all the work. Frankly, I'd rather contribute to what they've done than waste my time reinventing the square wheel.

So, thoughts people?

And on the topic of ColdFusion, I wrote replacements for all the ColdFusion mock objects for testing Java CFX tags. The existing ones are, ironically, buggy themselves, so having grown sick of them I replaced them.

Though I haven't released them to the wild, they work well enough for me, though I'm replacing some of the internals of [DebugQuery](https://web.archive.org/web/20080828064231/http://livedocs.macromedia.com/coldfusion/6.1/htmldocs/cfxrea33.htm) to make it a wrapper around a more general and faster implementation of the [Query](https://web.archive.org/web/20080828064231/http://livedocs.macromedia.com/coldfusion/6.1/htmldocs/cfxrefa6.htm) interface than how it's currently implemented.

I'm bringing this up because I've extended _DebugQuery_ and _DebugRequest_ to be able to return implementations of the Swing [javax.swing.table.TableModel](http://java.sun.com/j2se/1.5.0/docs/api/javax/swing/table/TableModel.html), and [javax.swing.MutableComboBoxModel](http://java.sun.com/j2se/1.5.0/docs/api/javax/swing/MutableComboBoxModel.html) respectively, allowing them to be edited in a UI as part of a test framework. This should suck rather less than doing all the fiddling in Java, especially when you want to be able to scroll back and forth through returned _Query_ objects. I'll post up the code once I'm finished reimplementing _DebugQuery_ and the code is solid.
