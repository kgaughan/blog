Title: Thoughts on Bugtracking
Date: 2008-05-29 15:48
Slug: bugtracking-thoughts
Status: published
Category: Projects

At [Blacknight](http://blacknight.com/), we use our own custom bugtracking software, [GrassSnake]({filename}grasssnake.md). It's something I wrote over the course of a few days on my own time and which I've been working on whenever I've had a free moment, which, in fairness, isn't all that often.

It's worked pretty well for us so far, but the design is beginning to hit a few limitations. Before I get to that, it's best if I explain its current design.

GrassSnake contains a list of _projects_, and each project has _issues_ contained within it, and there's a one-to-many relationship between projects and issues. Each issue has a series of _messages_ attached to it and a watch list. The _watch list_ is a list associating issues and users who wish to be informed when an issue is updated. How they get informed is the responsibility of whatever notification plugins are installed, with the current sole notification method being a simple mailer plugin. Privileged users are known as _developers_ and can be assigned as the _lead_ on a project or have issues assigned to them. The main purpose of a lead is that they're the person to whom issues for a particular project are assigned to initially and it's their responsibility to triage new issues for those projects and assign them to the appropriate developer.

This seems like a perfectly reasonable way of running things, and it was until a few months back, but it's becoming difficult to manage without resorting to adding a lot of administrative cruft to the application. For instance, there's reassigning issues from one project to another, merging issues together, marking issues as duplicates, and so on. These were being managed with command-line tools, but with the company network being locked down further, partly as a consequence of the [Debian OpenSSL debacle](http://www.links.org/?p=328) and a certain system administrator's intransigence ([*cough*](http://blog.moybella.net/)), that's not feasible any more.

So, what to do?

For a start, I want to get rid of projects. The basic idea is sound, but it doesn't really need to be explicit.

In its place, I want to add tagging or some other form of categorization. My thinking is that projects just need to be a specific class of category or tag. If I go down this route, the tag for, say, [BlogPing](http://blogping.sourceforge.net/)-related tickets would be `@blogping`, for AFK-related tickets, `@afk`, and so on: the `@` prefix marks the tag as a _project tag_. Issues too would become a special kind of tag, where the tag is a number prefixed by a hash symbol, so `#42` would be a tag for issue 42, whatever that might be. This would allow issues to be associated with one-another. A variant on issue tags would be duplicate issue tags, which would be used to mark an issue as a duplicate of another, so something like `dup:#42` would mark an issue as a duplicate of issue 42.

I also want to get rid of the idea of a developer. It should be sufficient for somebody to be watching an issue and optionally take responsibility for that issue.

To compensate for all the stuff being taken out, some more stuff's going to have to be put back in. The main thing to be added will be _autowatching_, where when an issue matches a set of criteria (that is, a specific set of tags), they're automagically put on the watchlist for that issue and possibly take responsibility for that issue.

The issue workflow GrassSnake currently has is _far_ too complex. The current states are:

*   Untriaged,
*   Open,
*   Suspended,
*   Resolved,
*   Works For Me,
*   Intended Behaviour,
*   Design Decision Needed,
*   Not Enough Information, and
*   Won't Fix.

Nine different states. This list grew organically over time and, I think, should never have reached the size if did. It's desperately in need of simplification.

Obviously, _Untriaged_ can be collapsed into _Open_ now that the idea of a lead developer gone. _Suspended_ was always a bit of a sop for the developer to be lazy and was a bad idea. The same goes for _Design Decision Needed_, which started life as a not-so-subtle way to get people to work on the design side of things properly, but never worked. _Works For Me_, _Intended Behaviour_, _Won't Fix_, and _Not Enough Information_ are really better off dealt with using messages. That leaves us with three issue states that are actually _useful_: _Open_, _Resolved_, and _Closed_. This simplified system would stay an issue property; there's no sense making it a tag. Moreover, I want to tie down the lifecycle more. From _Open_, the user should only be able to mark the issue as _Resolved_, and then, and _only_ then, _Closed_. It should be possible to make _Resolved_ or _Closed_ issues _Open_ again. The current system is rather fast-and-loose with the part of the lifecycle.

I'm tempted to make priorities issues, but, aside from some confusion and conflict between people on what the priorities mean, having them as distinct property of issues is useful.

Oh, and I finally have to implement [fulltext](http://dev.mysql.com/doc/refman/5.1/en/fulltext-search.html) search, which I'll probably make a plugin if I can, and a bunch of other bits and pieces such as tasks, a nag plugin for people who have taken responsibility for an issue, and paging. Then there's the need to finish the ticketing system I'd started writing to act as a customer frontend for GrassSnake.

Thoughts?
