Title: Restarting Mocha
Date: 2005-02-16 23:52
Category: Project Ideas
Status: published

While [Sage](http://sagerss.com/) is the closest I've ever got to an RSS aggregator I actually liked, it's still not right. There are just too many things about it that irk me somewhat.

I've tried so many of the blasted things and a few things have been confirmed for me time after time after time:

*   RSS Aggregators are _not_ email programs: [RSS Bandit](http://www.rssbandit.org/), [FeedDemon](http://www.bradsoft.com/feeddemon/), [SharpReader](http://www.sharpreader.net/), [Thunderbird](https://www.thunderbird.net/), &c. all suck as aggregators. Ok, so FeedDemon's not too bad, but it still feels too much like a mail app.
*   [Live bookmarks](https://support.mozilla.org/en-US/kb/live-bookmarks) suck too.
*   It's nice to be able to search old entries, but Sage doesn't keep them.
*   The [Comments API](https://web.archive.org/web/20080829004451/http://wellformedweb.org/story/9) is nothing but a good idea.
*   [Bloglines](http://www.bloglines.com/) is pretty close to what I wanted Mocha to be, but it's a webapp, so it sucks.

I've been dithering, as I'm wont to do, about [finishing Mocha]({filename}always-finish-projects.md), but being a bit of an [Architecture Astronaut](http://www.joelonsoftware.com/articles/fog0000000018.html), I have a tendancy to get lots of [good ideas]({filename}idea-aggregator-server.md) that don't really go anywhere.

I started Mocha before all the desktop aggregators started coming out, but never finished it. Everybody has those projects that they start, but never get around to finishing, but this one really burns me. I know _what_ I want, but I keep putting off actually getting it.

So, this being Lent and all, I'm going to do something about it. I'm going to flip the concept about and rather than giving something up, I'm going to take something up. Starting this weekend, I'm putting [MinGW](http://www.mingw.org/), [wxWidgets](http://www.wxwidgets.org/) and [libxml2](http://xmlsoft.org/) on my laptop and I'm finishing it.

Just in case you're wondering how long this thing's been bouncing around in the background, then [here is me complaining about doing nothing about it two years ago](https://web.archive.org/web/20050405081930/http://hereticmessiah.buzzword.com/2003/01/20), and the [first mention I could find of it](https://web.archive.org/web/20050405081637/http://hereticmessiah.buzzword.com/2002/03/11) back ing March 2002. And I _know_ the idea was bouncing around long before that. Hmmm... reading back over some of that reminds me of how whiney I can be.

## What I wanted it to be like

My vision back in the day for Mocha was quite simple:

*   You have two panes.
*   In the left pane, you have your feeds arranged hierarchically.
*   In the right pane, you have a viewer.
*   When you click on a feed, all the unread entries in that feed are displayed in the viewer.
*   If you click on a folder, you get all the unread entries for the feed within that folder.
*   And, of course, if you click on the root folder, you get _all_ your unread entries.

Of course, this was it at its simplest level. There was more.

*   Along the bottom is the _filter_ toolbar.
*   You can filter by date.
*   From now to a time in the past, or...
*   ...between a date range, or...
*   ...with keywords, or...
*   ...a combination of the above.
*   And using this, you could browse your archives.

But wait, there's more!

*   At the bottom of the left sidebar you have a calendar. On this would be marked all the days with entries in the selected month, so you could page through your archives easily.

And that's it. That is what I intended for Mocha. And it's a damned sight better than any of the UIs I've seen for aggregators up till now.
