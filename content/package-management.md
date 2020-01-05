Title: A method for doing package management using a union filesystem
Slug: package-management
Date: 2011-04-23 02:32
Category: Systems Administration
Status: published

It's long struck me as peculiar that package management isn't more commonly built on top of union filesystems. I'm sure there's probably somebody who's had roughly similar ideas to the ones I'm about to put forward, but I've never came across them being expressed anywhere.

Consider a package. It consists of a hierarchy of files, some metadata about those files (permissions, checksums, &c.), and a blob of metadata about the package itself such its version, a description, its dependencies, the services it provides, &c. The file hierarchy can be further subdivided into files that are meant to be immutable and those that are intended to be mutable (such as configuration file). Given all this information.

A package thus had two prongs: metadata and files, and files can be marked as either mutable or immutable in the metadata.

It stands to reason that, excepting dependency management, package installation should consist of simply dropping a package file into the filesystem hierarchy in a specific location.

The packages in this well-known location would thus be indexed by a special filesystem that for the purposes of this note, I'm going to call `packagefs`. `packagefs` simply keeps an index of the filesystem that the combined packages would expose the combined package hierarchies as a filesystem. This would be stacked with the root filesystem using a union filesystem, thus if a mutable file exposed by `packagefs` was edited and saved, the updated copy would appear in the same place in the hierarchy in a mutable filesystem, essentially performing a copy-on-write.

That much is obvious, but what I don't think is obvious is that such as system can solve or eliminate a lot of gnarly problems such package conflicts and others quite simply. They can do this using a **context**.[^1]

Contexts are the secret sauce of such as system, and can be tied to users, groups, specific packages, and so on.

Say, for instance, that you've two pieces of software written in Python, one that requires Python 2.\*, and another that requires Python 3.\* this means that it's difficult to get both pieces of software running on the same machine without a whole pile of awkward juggling, be it parallel hierarchies, executables with version numbers in their names, and so on.

Now say that these two pieces of software are packaged and state in their metadata that they depend on a the Python 3.\* and Python 2.\* packages respectively. When the OS does a context switch to executable A which depends on Python 3.\*, `packagefs` could notice this and expose the hierarchy of the Python 3.\* package instead, and similarly for executable B and Python 2.\*: the correct `/usr/local/bin/python` would be in place depending on the dependencies of the package the executable is from. Assuming that no packages depend on mutually incompatible pieces of software, this would provide a way for otherwise incompatible pieces of software to run on the on the same system.

That's package context, but what about users and groups? Well, if you'd a user or group and you wanted to restrict the package available to them, you could create a user/group context whitelisting certain installed packages for that user or group.

With this alone, you've got some of the positive aspects of chrooting.

Now let's go a bit further. As far as the user is concerned they only need see the contents of packages that have been explicitly marked as toplevel packages for them, so they might see some software that uses Perl, but might never see its interpreter or libraries unless their packages are marked as toplevel packages. It would be useful for users to temporarily enter a context in which certain packages appear as toplevel packages for them so they could develop against those packages. Pushing this idea a little further, and you essentially have a userland-based chroot environment.

So, that's that. If you think this is a good idea, feel free to go implement it. The difficult part in all this is, I think, contexts, but they're also the bit with the most potential benefits.

[^1]: When I wrote this, I didn't realise [Plan 9](http://plan9.bell-labs.com/plan9/) had a not-dissimilar concept in the form of [union mounts](http://en.wikipedia.org/wiki/Union_mount). However, the focus of contexts is wider as it's primarily concerned with package management.
