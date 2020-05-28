Title: I've finally found an excuse to use reflection in Java
Category: Coding
Date: 2004-11-29 14:24
Slug: first-java-reflection-use
Status: published

I've a project here at work. I need to write a ColdFusion custom tag in Java to talk to a remote server. This tag needs to handle a bunch of different requests and responses, but putting all that code in the one class would be a bit messy, and then there's the problem of what happens when I need to add new handler code to it.

So I'm using this as an excuse to use the [Java Reflection API](http://java.sun.com/docs/books/tutorial/reflect/) for the first time. It's going to make the job of implementing all this much simpler, and I'm not just doing it just because I can.

The handlers simply register themselves with the tag class, which acts as a dispatcher, informing it of who it is (with a _Class_ object), and what message it can handle. Then when the tag gets a request or needs to handle a response, it simply looks up the message to get back the corresponding class, and creates and instance (though I might do pooling later if I find a good reason), and pushes all the hard work onto the handler class.

This will rock!
