Title: My C++ wrapper for the Expat XML parser
Date: 2005-05-24 15:52
Category: Coding
Slug: xmlparser
Status: published

Last year when I was writing Orpheus, I knocked out a C++ wrapper around [Expat](https://libexpat.github.io/) to make using it easier.

It consists of two classes. `XMLParser` is the Expat wrapper and sets up the event handlers and automates setup and teardown of the parser itself. `XMLEvtHandler` consists of a set of callback methods triggered when some parsing event occurs, such as encountering a block of text, a start tag, or an end tag. You just subclass it, overriding any methods you need, and Robert’s your father’s brother.

It’s small and dead simple, and there’s next to no overhead except for that involved in the dynamic dispatch of the virtual members on the event handler class. In the big scheme of things, this overhead is minimal, though it could be got rid of completely if it were to be reimplemented using templates.

Download XMLParser and XMLEvtHandler [here]({attach}attachments/xmlparser/XMLParser.zip).
