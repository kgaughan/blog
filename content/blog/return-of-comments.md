Title: The Impending Return of Comments
Date: 2004-09-20 12:22
Category: Meta
Slug: return-of-comments
Status: published

I've been putting this off for long enough, and I think it's time to add comments back to my site.

The old system allowed comments on _every_ page of the site, not just the weblog. I think this is only right. The comments system is _still_ in there, but when I wrote my new blogging engine, I disabled it because it was file-based (though due to the magic of ColdFusion queries, the actual comments system doesn't know this: the logic for loading and posting comments looks as if it's talking to a database) as I didn't have a database for this site when I wrote it. No matter how clever this code might have been, it left people's email addresses open to download by spammers, and that's just now right. It also needed revision to clean up some of the logic: ColdFusion make it just a little too easy to intermingle logic and presentation.

To reenable the system, I need to create a new table in the database, and rewrite those two query files to use it rather than files.

But what I've been thinking of doing is using WikiComments, like on François Hoderne's [Znarf Weblog](https://web.archive.org/web/20081012083254/http://upian.net/znarf/). The idea's quite clever, and rather simple to implement, and it'd be fun and different.

But this is a maybe: I might do it, but then again I might now. One thing is certain though: this site will have comments again!
