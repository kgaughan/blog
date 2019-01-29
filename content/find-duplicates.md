Title: From my ~/bin: find-duplicates
Date: 2008-02-11 15:11
Category: Tools
Slug: find-duplicates
Status: published

!!! note
    This one was relatively populate for whatever reason. I'd recommend you use something like [duff](http://duff.dreda.org/) these days, though find-duplicates still works better in some circumstances.

	I'm still kind of happy with this code though. [Here](https://web.archive.org/web/20080907024912/http://talideon.com/weblog/2008/02/find-duplicates.cfm) is a cache of the original post.

This is is starting to become a bit of a series! I needed a small, sharp tool for finding what duplicate files I had sitting on my external harddrive. I've lot of stuff which, over time, has got inadvertently duplicated, or downloaded twice, such as photos, software archives, sound files, papers and articles, &c. It needed to be fast and small, capable of having several directories searched at once (e.g., my home directory and some directory on the external HDD), and grepable. Here's the result:

```python
#!/usr/bin/env python
#
# find-duplicates
# by Keith Gaughan <http://talideon.com/>
#
# Finds an lists any duplicate files in the given directories.
#
# Copyright (c) Keith Gaughan, 2008.
# All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# This license is subject to the laws and courts of the Republic of Ireland.
#

from __future__ import with_statement
import sys
import os
import hashlib
import getopt
import filecmp


USAGE = "Usage: %s [-h] [-m<crc|md5>] <dir>*"


class crc:
    """
    Wraps up zlib.crc32 to make it suitable for use as a faster but less
    accurate alternative to the hashlib.* classes.
    """
    def __init__(self, initial=None):
        self.crc = 0
        if initial is not None:
            self.update(initial)
    def update(self, block):
        import zlib
        self.crc = zlib.crc32(block, self.crc)
    def hexdigest(self):
        return "%X" % self.crc
    def digest(self):
        # Er...
        return self.crc


def all_files(*tops):
    """Lists all files in the given directories."""
    for top in tops:
        for dirname, _, filenames in os.walk(top):
            for f in filenames:
                path = os.path.join(dirname, f)
                if os.path.isfile(path):
                    yield path


def digest(file, method=hashlib.md5):
    with open(file) as f:
        h = method(f.read()).digest()
    return h


def true_duplicates(files):
    """
    Compare the given files, breaking them down into groups with identical
    content.
    """
    while len(files) > 1:
        next_set = []
        this_set = []
        master = files[0]
        this_set.append(master)
        for other in files[1:]:
            if filecmp.cmp(master, other, False):
                this_set.append(other)
            else:
                next_set.append(other)
        if len(this_set) > 1:
            yield this_set
        files = next_set


def group_by(groups, grouper, min_size=1):
    """Breaks each of the groups into smaller subgroups."""
    for group in groups:
        subgroups = {}
        for item in group:
            g = grouper(item)
            if not subgroups.has_key(g):
                subgroups[g] = []
            subgroups[g].append(item)
        for g in subgroups.itervalues():
            if len(g) >= min_size:
                yield g


def usage(message=None):
    global USAGE
    fh = sys.stdout
    exit_code = 0
    if message:
        fh = sys.stderr
        exit_code = 2
        print >>fh, str(message)
    name = os.path.basename(sys.argv[0])
    print >>fh, USAGE % (name,)
    sys.exit(exit_code)


def main():
    try:
        opts, paths = getopt.getopt(sys.argv[1:], "hm:")
    except getopt.GetoptError, err:
        usage(err)
    method = crc
    for o, a in opts:
        if o == "-m":
            if a == "crc":
                method = crc
            elif a == "md5":
                method = hashlib.md5
            else:
                usage("Unknown grouping method: %s" % (a,))
        elif o == "-h":
            usage()
        else:
            usage("Unknown option: %s%s" % (o, a))

    if len(paths) == 0:
        paths = ["."]

    first = True
    groups = [all_files(*paths)]
    for grouper in [os.path.getsize, lambda file: digest(file, method)]:
        groups = group_by(groups, grouper, 2)
    for group in groups:
        for files in sorted(true_duplicates(group)):
            if first:
                first = False
            else:
                print
            for file in files:
                print file


if __name__ == "__main__":
    main()
```

It's pretty simple, really. It walks the directories listed on the command line, sorting the files it finds into groups of files likely to be similar. The default criterion is to group them based on file size, which is quick and usually a good indicator that the files are the same. If it's not, such as if you're dealing with a bunch of [RAW images](https://en.wikipedia.org/wiki/Raw_image_format) or [TARGA](https://en.wikipedia.org/wiki/Truevision_TGA) files that are all the same size, other criteria can be used, such as the result of a [CRC](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) ([Adler-32](https://en.wikipedia.org/wiki/Adler-32), specifically) ran on the files, or their [MD5](https://en.wikipedia.org/wiki/MD5) hash. CRCs might be useless for hashing, but they're much quicker than a proper hash, and give a reasonable indication of whether the files are same. After that, each file in the group is explicitly compared for equality to ensure that they *really are* duplicates, and broken into subgroups. This ensures that you won't accidentally delete anything that might *appear* to be a duplicate, but really isn't.

When it's finds identical files, they're listed together, one per line, in groups separated by empty lines.

**Update (Feb 12th):** Got rid of some stupid inefficiencies. I'd forgotten that the `read()` method on filehandles will read everything if no argument's provided. This speeds it up somewhat when using the CRC or MD5 methods. For the size-based method, I think I'm going to introduce some extra grouping based on one of the other two methods to avoid needless file comparisons. Oh, and `whittle()` returns a generator now rather than a list.

**Update (Feb 14th):** Threat carried out! `whittle()` has been replaced by a more general method called `group_by()` which is similar but accepts an iterable of iterables instead of an iterable, and rather than returning a generator, it *is* a generator. Also, after the initial grouping by size, it groups by CRC, though this can be changed to use MD5 with a switch. Now the initial cheap grouping by size is always done, and the more expensive grouping methods (by hash/checksum, then direct comparison) are done after. This is *much* faster.
