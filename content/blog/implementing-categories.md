Title: Implementing Categories
Date: 2004-09-20 12:24
Category: Meta
Slug: implementing-categories
Status: published

One thing I'd like to add, but I've never came up with as satisfactory method of implementation for, is categories.

The best pure one that I've come up with is to use an unsigned integer column as a _bit array_, with each bit representing a category. The problem with this is that it puts a nasty limit on the number of categories that the blog can have, and means that I need to be open to the need to recycle bits later as categories are added and deleted. There's also the problem of indexing, but it's not an intractible one: more later.

Using _SET_ columns doesn't strike me as correct because I want to be able change the categories later on, and having to fiddle with the schema to do so seems rather messy. No indexing problem though, except when the set of categories needs to change. _shudder_

Including an extra _many-to-many table_ is at best messy. I've seen it in systems before, and used it, and it's always struck me as being little more than a nasty, if necessary, kludge. I might even use it if it didn't make fetching the categories so horrible when I'm listing multiple entries. This solution has no indexing problems.

My penultimate solution is to treat the categories as _keywords_. Here, I'd have a _VARCHAR_ column containing a list of the keywords associated with the entry. Selecting the entries in a category is nasty here because it can't be indexed, so the DBMS needs to do a linear search rather than a keyed one. While I doubt people will be listing categories all that much, I still don't like the idea that it'll take that long.

I can make the _bit array_ indexable by using a _SET_, with each element corresponding to a bit. This is probably the best way, but I'm still a bit uneasy with it.

Ah! Another idea's after coming to me: go with the _many-to-many_ table, but rather than querying the categories for each as they come along, do them in one chunk seperate from querying the entries (this'll need a pass over the query to get them), then add an extra column for the entries query, setting up the categories. The code can then iterate over it all safely and cleanly, and it allows me to go keyword-mad when I feel like it.

But are there any better ways of doing it? To be honest, I don't know, and I haven't found any. Any ideas?

Then again, with the ability to post up fine-grained entries, something I wasn't able to do with Manila back on weblogs.com, maybe I don't really need categories of this complexity and maybe all I need is a one-to-many relationship between categories and entries. Time will tell...
