How I use git
=============

:date: 2016-04-05 19:04
:category: Coding
:status: published

.. Oh, look! Yet another developer explaining their git workflow! Well, kind
   of. It's best to consider this a public record of what I do for my own
   reference and so I can throw a link in people's direction to explain my
   reasoning.

My git workflow for anything non-trivial is pretty straightforward, but a
little different from what I've seen others describe. I'm almost certainly not
the only person out there who uses this workflow, so I'm certainly not claiming
any originality.

There seem to be two camps, both based on how stuff gets into master, or
whatever the equivalent happens to be.

The rebase camp take their feature branches, rebase them off of master, and
then perform fast-forward merges, leaving them with a nice, clean, linear
history on their master branch.

The merge camp take their feature branches and do a non-fast-forward merge,
leaving them with a full history of development.

I think both these camps are wrong. Kind of.

There's real value to what both camps prize: a linear history makes it much
easier to reason about how the master branch got to the state it's currently
in, while merge commits, used well, give you a better idea of when particular
features entered the codebase.

My preferred way of working sits in between the two of these. When I'm ready to
merge in a branch, I rebase it off of master, run my test suite to make sure
everything still works, and then, most importantly, I do a non-ff merge with a
proper commit message.

So, I'm essentially both rebasing and merging.

What are the benefits of this?
------------------------------

Ultimately, you keep your history so that somebody can read it. You hope that
this is never *necessary*, but inevitably the point will come when you have to.

The big benefit of a merge-centric workflow is that you end up with a
*delimited* history: your history is broken up into chunks of changesets that
do something in particular to the codebase. This makes things like bisections__
to find regressions might have been introduced easier. The downside is that you
can end up with a spider's web of a history that's difficult for somebody to
follow.

.. __: https://git-scm.com/docs/git-bisect

A rebase-centric workflow doesn't have this latter problem as a linear history
is easy to follow from commit to commit, but you lose the the visibility on
when specific things were introduced into the codebase.

This history of when merges happened is actually *useful*, even if the rat's
nest they cause under a purely merge-centric workflow isn't quite so useful.

Are there downsides?
--------------------

None that I've been able to detect, though I have to say that git works against
it by not having an easy way to check if a fast-forward merge would work. For
this to work, you need to perform a non-fast-forward merge when a fast-forward
merge would work.  There are `ways of doing such a check`__ using `git
merge-base`_, `git merge-tree`_, and some other bits and bobs on the output but
I need to write up some supporting aliases.

.. __: http://stackoverflow.com/questions/501407/is-there-a-git-merge-dry-run-option/6283843#6283843
.. _git merge-base: https://git-scm.com/docs/git-merge-base
.. _git merge-tree: https://git-scm.com/docs/git-merge-tree
