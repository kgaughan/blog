Title: GrassSnake, my bug tracker
Slug: grasssnake
Date: 2007-08-29 15:05
Status: published
Category: Projects

[Note: I haven't been able to recover the screenshots.]

I thought I'd post up a few screenshots of GrassSnake, the bug tracker I wrote for my own use, and which we also use with work after we got rid of [phpBugTracker](http://phpbt.sourceforge.net/), a piece of software nobody liked or wanted to use.

Most of the work on it was spent making its interface as bloody simple to use as possible: I wanted to get people keeping bugs in one place where everybody could see them rather than emailing them to me, and I wanted to keep the barrier to posting as low as possible.

The screenshots are a little bit old at this point, but they're still pretty representative of the application.

[![Console](https://web.archive.org/web/20080829004706im_/http://talideon.com/images/blog/gs/gs1.png)](https://web.archive.org/web/20080829004706/http://talideon.com/images/blog/gs/gs1-big.png "Console")

This is the console, which displays the bugs pending the user's attention, be they ones assigned to them (above) or ones they're interested in (below).

[![Project Page](https://web.archive.org/web/20080829004706im_/http://talideon.com/images/blog/gs/gs2.png)](https://web.archive.org/web/20080829004706/http://talideon.com/images/blog/gs/gs2-big.png "Project Page")

Here's a sample project page. It lists the issues that are part of this project and lets you post up new ones. You see the stars? If they're blue, the issue is assigned to you. If they're yellow, you're watching them, and if they're gray, you're not. You can toggle an issue between watched and unwatched by clicking the gray and yellow stars.

[![Issue Page](https://web.archive.org/web/20080829004706im_/http://talideon.com/images/blog/gs/gs3.png)](https://web.archive.org/web/20080829004706/http://talideon.com/images/blog/gs/gs3-big.png "Issue Page")

A sample issue. You can post up new comments, reassign it to other people, and change its status and priority.

There's a few other screens, but they're the principle ones. Once I've a public source repository (most likely a [Mercurial](https://www.mercurial-scm.org/) one, it's beginning to seem), I'll make it openly available.

Update: More likely, I'll be using [Bazaar-NG](http://bazaar-vcs.org/), but only because it can publish repositories using FTP, which I'm stuck with until I eventually get my own server. Sigh. I'd prefer not to, because hg's faster than bzr, but I've no choice, it seems.

**Update:** I'm writing a ticketing plugin for it right now, which should be useful.
