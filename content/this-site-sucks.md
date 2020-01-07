Title: Things that suck about this site
Slug: this-site-sucks.cfm
Date: 2006-01-30 15:33
Category: Meta
Status: published

My vitriol isn't just reserved for others. No, I'm quite happy to lash out at myself when it's appropriate. There's a lot of things I really don't like about the code I wrote to drive this site. I thought it'd be good to get everything down.

### The software lacks a well-defined structure

Yup, it's just a bunch of files. The site has five applications running on it:

1.  the weblog;
2.  the comments app (which is separate from the weblog);
3.  the linklog;
4.  the mailer;
5.  the wiki.

The first four were written out on paper over the course of a bored evening and then typed into a computer and uploaded the next day. The wiki was written in two short bursts, once to get something functional for the C&C wiki, and again to slap on a passable change control system on top of it. I don't think I've spent more than ten hours in total on the code here. From that perspective, they're not bad. But since the day they were first written, all I've done is occasionally tweak them when I needed to. They're starting to smell a bit.

For some ridiculous reason, the **comments app** was written to be fully independent of everything else. I think I was inspired to do that by something I saw in [ACS](https://en.wikipedia.org/wiki/ArsDigita_Community_System), but I'm not sure. I wanted people to be able to comment on _any_ page, not just those in the weblog. In the end, I never took advantage of this. This design is the reason why the site currently doesn't display the number of comments in reply to a post: the join would be a pain as I idiotically store a _hash of the page path_ with each comment! To add insult to injury, it uses CLIENT variables rather than SESSION variables or cookies directly and I have to do comment moderation by hand in the DB! I have no idea what I was smoking when I came up with that system.

The **linklog** was another misguided idea, but for other reasons. What I ought to have done was have a form for queuing up items for the linklog, and whatever items were in the queue at midnight UTC posted to the weblog in a single post. _Or_ I could have had made them true weblog entries, something Keith Devens pointed out to me in the past. We live and learn. I'm edging towards the former option. But do you know what's _really_ dumb about it as it stands: I never bothered to make links editable after they'd been posted. I hasn't caused huge difficulties or anything, but there's been times when it might have been a wee bit useful.

The **mailer**'s just a little blob of intermixed markup and code with a bunch of hardwired settings. Not good enough!

The **weblog** is the best bit of code in it. Where it fails is that I didn't do enough to seperate everything out (action handers here, views there, &c) and too much of the site is fried rather than baked: everything, including the frontpage with that painfully expensive SQL statement to generate _x_ days' worth of posts rather than the posts for the past _x_ days or the past _x_ posts, is generated on the fly. Also, the interface for posting and editing's a bit more primitive than I'd like, and I _still_ haven't added tags, something I want for my own use more than as a readers' convenience. Then there's the lack of a comment count.

The **wikis** still both stick out like sore thumbs on the site. Not only is the code between them duplicated, but they don't integrate into the site in terms of look-and-feel. There's _no_ good reason why this should be so. [FusionWiki](http://fusionwiki.sourceforge.org/)'s also got a huge to-do list attached to it in other areas that I've been procrastinating on. Sigh.

Then there's the lack of any consistent administrative interface over the whole thing, and the partial hack of a reStructuredText mark-up converter I wrote for the weblog, comments app and wiki. I'm really considering replacing it with a WYSIWYG and server-side HTML scrubber combination (which is something else I really must upload and make public), but every WYSIWYG I've tried sucks even more than the mark-up converter. And I've tried them all. Or maybe I should just bite the bullet and convert [Markdown](http://daringfireball.net/projects/markdown/syntax) to ColdFusion.

And have I mentioned how mind-numbingly stupid the syndication code for the linklog and weblog is? Painfully, painfully so. All it does is generate an RSS 2.0 file if the weblog or linklog's been updated and leaves things at that. It doesn't check request headers to check how much it should be serving up--I could be sending 35kB down the line and only really need to send 5kB--or to support conditional GETs, nor does it use content negotiation to serve up the most appropriate syndication format. It works ok, but if this was a site that was regularly updated or had a reasonable amount of readers--say, if I was a Y-list rather than a Z-list blogger--it'd die a painful death.

### How to make my site suck less

My site has a lot of good ideas. Chief amongst them are the <cf_do> tag (my way of avoiding the scatter of duplicated code--particularly custom tags--that was a definite pain point before CFMX, and this site still runs on CF5, so I'm stuck with it) and the <cf_envelope> tag, which allows me to hook in behaviour to disparate pages quite easily.

If <cf_do> was modified _slightly_ to make it behave a little better and support applications in addition to tags, <cf_envelope> enhanced into the framework it _almost_ is, and the various apps mostly moved in under the `_lib` directory where a big chunk of the site code already lives, I'm pretty sure this site would suddenly start to feel a lot better.

The weblog should bake the various entry and index pages, _especially_ the frontpage. The linklog should be merged into the weblog, and the wikis should be made to fit into the site as a whole. The comments app, if it's going to stay independent of the weblog, needs use the full path of the page in question rather than a hash of it, and I need to get rid of those stupid CLIENT variables. The syndication code needs to be smartened up quite a bit and made part of the weblog software itself, with the HTML frontpage being just one representation along with everything else.

I need to, at the very least, make the markup filter suck an awful lot less.

I need to bring back editable page areas. I miss that.

Above all, I need to poach ideas from Syncope, the quasi-framework I use for PHP, and incorporate them into the site.

Any ideas? In what ways to _you_ think the site sucks? And how do you think it could be made better. If you want to take a look at the mess that drives this site, you can download it [here]({attach}/attachments/this-site-sucks/site.zip) (75kB). It's crap, but it's mine, so don't go passing any of it off as your own work (not that it's worth it) or using any of it anywhere without asking me first. Any incriminating details, such as DSNs, usernames, passwords, email addresses, &c. have been removed. As it stands, it probably won't work for you as it doesn't contain the DB schema, but it might be worth a read. Don't laugh too much, ok?
