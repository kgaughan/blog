Title: Moving from SVK to Bazaar-NG
Date: 2007-10-08 10:17
Slug: svk-to-bzr
Status: published

I exported my projects from [SVK](https://web.archive.org/web/20080828070002/http://svk.bestpractical.com/)'s hidden Subeversion repository on Saturday using [tailor](https://web.archive.org/web/20080828070002/http://progetti.arstecnica.it/tailor). I was expecting it to be simple, but it was anything but! Mind you, this is probably my fault.

I just wanted to get it working, so I read the documentation accompanying tailor to figure out what I was supposed to do. However, none of it seemed to work, not least of which was that it was saying [Bazaar](http://bazaar-vcs.org/) wasn't a supported VCS! After a bit of investigating, I came to the conclusion that between the time that `tailor-0.9.29` was released and `bazaar-ng-0.91` was released, there were some minor, but important changes within [bzrlib](http://bazaar-vcs.org/BzrLib). The one that bit me was that in [`vcpx/repository/bzr.py`](https://web.archive.org/web/20080828070002/http://progetti.arstecnica.it/tailor/browser/vcpx/repository/bzr.py?rev=1369), it was importing `compare_trees` from `bzrlib.deltas` (line 25), but the name of that particular function has changed to `_compare_trees`, as I discoved with a quick `dir(bzrlib.deltas)`. It doesn't seem to be used in the end, so I think that import line can probably be deleted.

After reinstalling it with my patch, I tried generating the configuration file again, but to no avail. Maybe I'm just dumb--not entirely unlikely--but the configuration options don't seem to make any sense. Some end up being ignored, and others don't seem to do exactly what you'd expect. I gave up and started bludgeoning the config file directly. To export AFK from my old SVK repository, here's what I used:

```ini
[DEFAULT]
verbose = True

[project]
target = bzr:target
start-revision = INITIAL
root-directory = /usr/home/keith/branches/dev/personal/afk
state-file = tailor.state
source = svn:source
subdir = .

[bzr:target]
repository = .

[svn:source]
module = /afk/trunk
repository = file:///usr/home/keith/.svk/local
```

The key bits here are `root-directory`, which specifies where the repository you're importing into is, `module`, which specifies the path in the SVK/SVN repository of the project, and the second `repository` line, which specifies the location of the subversion repository itself. I dropped this file in `~/branches/dev/personal`, and then, in that directory, did the following:

```text
% mkdir afk
% cd afk
% bzr init
% bzr whoami "Keith Gaughan <myemailaddress@example.com>"
% cd ~-
% tailor --configfile afk.tailor
```

Tailor should start moving the revisions from the old repository to the new one. After it's finished, it leaves some crud behind, so do the following:

```text
% cd ~-
% rm project.log tailor.state*
% find . -name .svn -exec rm -rf {} +
```

That'll clear out the `.svn` directories it created in the process of checking out the individual versions, and the logs it leaves behind.

Bingo! You've now turned a Subversion/SVK project into a BZR one! Now, I just have to contact the person maintaining tailor in the ports and the original author and get them to fix that problem...

I'll see if I can find a less hacky way to do this, but for now this works.

**Update:** Submitted the bug report. Tailor's 'new ticket' appears to be disabled, even if you've created an account. It appears you have to be explicitly given permission to post up new bugs. Hrumph. I emailed the maintainer the report directly.

**Update (later that same day):** [Fixed!](https://web.archive.org/web/20080828070002/http://progetti.arstecnica.it/tailor/browser/vcpx/repository/bzr.py?rev=1442) That was fast! Gotta love open source.
