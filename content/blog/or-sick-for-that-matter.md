Title: Turns out I was sick rather than tired
Slug: or-sick-for-that-matter
Date: 2006-02-19 15:34
Category: Life
Status: published

I don't know whether it was that I picked up the 'flu that's been going around the office, or if I ate something bad while I was here, but I was in a complete mess Friday and Saturday. I was completely out of my head Saturday morning, but I seem to be ok now. I'm just a bit groggy and tired, and my stomach's a bit worse for wear, but I'll live.

I pity the poor chamber maids though: I would _not_ want want to be the person scrubbing the toilet. It's not blocked or anything, just a bit [mank](http://www.urbandictionary.com/define.php?term=mank).

## Ye Olde HTML Scrubber

On the plus side, though my weekend's pretty much screwed, I _did_ buckle down and start coding the HTML scrubber I've been [threatening to write]({filename}java-html-scrubber.md) for months now. I'm starting it with a cut-down SAX-style liberal SGML parser, which is currently about 10% of the way done. I have the parsed character data part of it done (and was more awkward to do properly for a liberal parser than I'd expected), and the next bit will be to do the tag parser (which I've done the background work for), and finally, I'll need to wire all that together and get it firing events.

Once the parser is done, I'll concentrate on the the scrubber itself. It'll use a stack to keep track of the tags and fire off events when it encounters start tags or unbalanced tags to some other bit of code which'll know which tags to keep, which ones to ditch, and how to resolve the unbalanced tags.

## Netbeans

Seeing as the I'm writing it in Java, I decided I'd take a look at [NetBeans](http://www.netbeans.org/) to see if it still sucked as much a I remembered. On the plus side, it's much snappier and feels better. On the minus side, it's still a big ugly, doesn't use my Windows anti-aliasing settings, it uses that awful anti-aliasing (smudging's more like it) system built into Java, doesn't have decent Subversion integration. It's intellisense is also just a little _too_ helpful at times. But overall, I'm quite happy with it.

I was able to solve at least some of the UI ugliness by installing [Kirill Grouchnikov](https://web.archive.org/web/20081015170420/http://weblogs.java.net/blog/kirillcool/)'s [Substance](https://web.archive.org/web/20081015170420/https://substance.dev.java.net/) look and feel and by changing the colour scheme to one that doesn't hurt my eyes.

## First impression of Silent Universe

I've just started listening to [Silent Universe](http://www.silentuniverse.com/) and my first impression is _awful, awful Irish/Scottish accent_! That woman _seriously_ needs lessons!

## Monday Update

Still feeling like crap. I'm better: no I just feel flushed, lethargic and queasy. I decided I'd head to the South Shore Plaza to try and pick some stuff up for whatever's making me feel ill, but after I was there for a short while, I was almost overcome with nausea. I _did_ manage to pick up some stuff from the pharmacy while I was there and pick up a present for Niamh's birthday, but after that I decided I'd catch a taxi back to the hotel. Not the best of weekends.

I'm heading into work now. I'd say I can hold up for the rest of the day.
