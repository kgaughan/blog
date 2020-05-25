Title: RIP, spinning rust...
Slug: dell-mini-12-spinning-rust
Category: Hacks
Date: 2020-05-25 21:22
Series: Dell Mini 12
Status: published

[Last time]({filename}/notes-dell-mini-12.md), I got my old Dell Mini 12 up and running again. Well, the fates did not smile kindly on me, and through my own clumsiness, it ended up slipping off my lap, leaving it with some very, very unhappy spinning rust.

And yes, it contains a regular HDD, and not an SSD of some kind. That didn't bother me terribly up until now, but if that's not working, the machine is pretty much junk. Still, it turns out that the machine is has a pretty good service manual [here]({attach}/attachments/dell-mini-12/inspiron-1210_service manual_en-us.pdf), so fixing it is at least feasible.

I'm in two minds about doing this. Replacing the drive and battery will come to about €60 in total, and given machine is hardly particularly spectacular in terms of its place in computing history, it doesn't seem like a great use of my time and money to fix it up. However, being stuck inside means I don't exactly have a tonne of other things to do, so it's looking very tempting! It has the notorious [GMA 500](https://en.wikipedia.org/wiki/Intel_GMA#GMA_500) (Poulsbo) graphics code, and all the broken driver support that goes with it. This machine is never going to be anything other than something to run terminals on.

The machine takes a 1.8" [PATA](https://en.wikipedia.org/wiki/Parallel_ATA) drive, much like you'd find in iPod Classics and the like. PATA was on its way out when this machine was built, so I'm assuming the main reason for using it was cost, in spite of PATA being worse than SATA in every other way. It's slower, more power-hungry, and obsolete. Here's [a post on the Dell Mini 12](https://superuser.com/questions/975345/how-to-replace-hard-drive-and-switch-drive-cable-in-a-dell-mini-12) that gives some useful details. It looks like some kind of Compact Flash adaptor might be feasible, but I'd prefer to get a regular solid state drive if I can, though anything bigger than 32GB is basically going to be a waste of money.

I've found everything I need to get it running again. I guess writing this post has made the decision for me.
