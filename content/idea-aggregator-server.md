Title: On Writing an Aggregator Server
Date: 2004-09-20 12:26
Category: Project Ideas
Slug: idea-aggregator-server
Status: published

Seeing as I'm flitting about the idea of finishing my two and a half year old RSS aggregator, _Mocha_, I've also had an idea that might help reduce the load that aggregators inevitably take on the web: an aggregator server.

Bloglines is a great idea, but it has one fatal flaw: it's a web application and web applications, no matter how great they are, inevitably suck. This is a sad fact of life. Even Gmail, though it doesn't suck nearly as much as most, still sucks because it still can't shake off that web application stink.

But Bloglines is a good idea: one server combines all the requests of all these users who are signed up to the same feed together into one, lessening the gross impact of the subscribers upon the subscribed, and it _always_ does it intelligently.

But web applications suck, and I can't just update my feeds while I'm at work and then read them later on when I'm back in my flat where I don't even have dial-up.

But often people in the same office, company, whatever, subscribe to many of the same feeds. For instance, I know that both myself and Peter subscribe to [The Daily WTF](http://thedailywtf.com/) and [Gavin's Blog](http://gavinsblog.com/). I makes no sense that we're both making seperate requests to the same feed when it would be better if those requests were combined and done together.

Mocha as it stands is written in VB: I almost started it in Java, but needed a good reason to write some VB at the time. C# and the rest of .NET was only beginning appear on the scene in any significant way at the time and it wasn't worth investing in it at the time, so I started it in VB.

Now, I'm thinking of ditching the VB codebase and taking what I can--mainly graphics, algorithms and ideas--and rewriting the core in C++, with the rest written in [Lua](http://www.lua.org/) and [wxWidgets](https://www.wxwidgets.org/) as the toolkit. This allows me to follow through with my fiendish plan:

Write the aforementioned aggregator server. This would provide a [REST](http://www.xfront.com/REST-Web-Services.html)-ful API (we don't need no steeking SOAP!) to which Mocha could talk. The server could make sure that it was fetching only when there was entries, and only once regardless of how many people were subscribed. This fact would be largely transparent to the person using Mocha. In fact they might even find it all works subtly better because they'll never miss an entry.

And the big pay offs? No matter where I am, if I can see the aggregator server I can access my feeds, and the central server will help keep track of what ones I haven't read. While this doesn't apply so much to me because I don't have a connection here in my flat, for people who do, it'll be invaluable. And there's the obvious: I'm lessening the load on the people whose writing I enjoy.

Hidden benefits are that the desktop aggregator can become format agnostic: those messy details are dealt with by the aggregator server. It'll no longer really matter what kind of feed it is just as long as the server can deal with it: good bye stupid format wars.

As long as the API is kept open, I see no reason why this kind of setup couldn't become widespread. As it stands, Bloglines could be the first to implement this thing on a wide scale. I want to do it, but they've got much of the infrastructure right there. All they need to do is expose an API, and all the aggregators need to do is support it.

While essential to minimise the impact on the syndicator's server, no amount of hacking with HTTP, no amount of optimal use of headers, nothing can compare to the gains that can be experienced by aggregating many requests into single ones. Considering the way mass feed syndication works, this is the best way to spread the load.

So, who's with me?
