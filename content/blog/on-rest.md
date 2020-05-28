Title: On REST
Date: 2008-08-20 15:10
Category: Tech
Status: published

Tim Bray posted up a good piece called '[REST Questions](http://www.tbray.org/ongoing/When/200x/2008/08/18/On-REST)', and one of the commentators [asked several questions](http://www.tbray.org/ongoing/When/200x/2008/08/18/On-REST#c1219096506.232478) I felt I should respond to. This was [my response](http://www.tbray.org/ongoing/When/200x/2008/08/18/On-REST#c1219167217.122048) with some light editing and additional links:

> Mainly because there is still a little confusion on what exactly REST is?

[REST](http://en.wikipedia.org/wiki/Representational_State_Transfer) is an architectural style. I think the confusion is that people confuse '[architectural style](http://www.ics.uci.edu/~fielding/pubs/dissertation/net_arch_styles.htm)' with '[architecture](http://en.wikipedia.org/wiki/Technical_architecture)' and '[protocol](http://en.wikipedia.org/wiki/Protocol_(computing))', neither of which an architectural style is.

> As a technology person, I sure wish REST had some very, very distinct features.

It does, only the thing to remember is that it is neither an architecture nor a protocol, but describes a set of useful and interrelated properties an architecture or protocol fitting it would have as well as the benefits and demerits resulting.

The confusion here is that people are committing a [reification fallacy](http://en.wikipedia.org/wiki/Reification_fallacy): they're taking something abstract and treating it as if it's more concrete than it is.

> Even with AJAX...

That's apples and amoebas. [AJAX](http://en.wikipedia.org/wiki/Ajax_(programming)) is quite a concrete thing: making HTTP requests in Javascript within a browser.

> Let me ask this question, is there a REST RFC?

No, but there could be, and [it'd be informational](http://www.rfc-editor.org/rfc/rfc3117.txt).

> Could one be implemented?

Based on REST, you could 'implement' it, after a fashion, by designing a protocol based on REST.

Let me put it this way: a protocol or architecture is a [reification](http://en.wiktionary.org/wiki/Reification) or 'implementation' of one or many architectural styles. Similarly, an application or system is a reification/implementation of one or more protocols and/or architectures.

> What if a server or client library fails to implement the features properly, is it still REST?

Clients and servers don't implement REST, they implement RESTful protocols. What they're doing is implementing or using the protocol incorrectly by going against its grain.

> Lets say I don't get HTTP right. I don't use PUT, I don't use DELETE. I use a heavy RPC oriented XML messaging format in POST requests. Heavy requests. Am I building a REST application?

PUT and DELETE have nothing to do with REST. You're confusing REST's [uniform interface constraint](http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1_5) with how HTTP implements it. [RPC](http://en.wikipedia.org/wiki/Remote_procedure_call) as an architectural style (yep, it is: it's initial reification from style to protocol was probably [RFC1050](http://www.rfc-editor.org/rfc/rfc1050.txt), though I'm sure something predates that) is diametrically opposed in most regards to REST, so no, it wouldn't be RESTful. The [Flickr API](http://www.flickr.com/services/api/) is RPC, plain and simple. The same goes for the ['RESTful' Twitter API](https://web.archive.org/web/20081122004221/http://groups.google.com/group/twitter-development-talk/web/api-documentation) and the ['RESTful' Last.fm API](http://www.last.fm/api/rest), both of which are RPC and definitely not RESTful.

> Can you use custom XML RPC formats with REST?

I'm not quite sure what you mean, but if you mean using [XML-RPC](http://xmlrpc.com/spec.md) as an object serialisation format similar to [JSON](http://www.json.org/), sure, but that's as far as it goes.

> If REST is essentially getting HTTP right?

Yes and no. Using HTTP in a RESTful manner is getting HTTP right, but HTTP is not REST, it's protocol that adheres to the REST architectural style.
