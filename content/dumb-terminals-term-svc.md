Title: Dumb Terminals and Windows Remote Desktop
Slug: dumb-terminals-term-svc
Date: 2005-04-28 19:26
Category: Tech
Status: published

I'm spending a lot of time connected via [Windows Remote Desktop](https://web.archive.org/web/20080829002817/http://www.microsoft.com/windowsxp/using/mobility/getstarted/remoteintro.mspx) to an external network so that I can do work on their machines.

So here's a question: are there any IT departments out there that are using this to give their users old-style dumb terminals so as they can reduce the amount of maintenance they need to do, and their costs?

The setup would be simple enough. All you need a bunch of basic machines with decent graphics cards and a decent monitor. They needn't even have harddrives: all the software could be stored in ROMS. All you need is a machine fast enough to do any necessary compositing, to redraw the screen quickly, and to send any data from the keyboard and mouse down the line. You'd have totally silent machines that consume very little power.

The only software the client boxes need are a basic OS that can do sufficient networking to support the desktop client. The OS needn't even support the kind of sophisticated multitasking that a full system would need.

On the server side of things you could have a gateway that would receive initial connections, and farm them off to one of an array of identical boxes behind it, maintaining a balance across all of them. This would allow for a degree of redundancy, so if you were doing upgrades, you could do them without anybody noticing (more or less), and if one of the boxes died, the only people who'd need know would be IT staff.

Most users only use a fraction of their machine's processing power most of the time, so I really doubt they'd feel any slowdown as long as everything felt responsive to them.

Of course, such machine might not have the same kind of eye candy as standalone boxes, but that's not a consideration here.

History has a habit of repeating itself. Maybe with the availability of broadband and fast LANs, it's time for people to take a serious look at timeshare again.

**PS.** Don't bring [X](https://www.x.org/) up: (un)fortunately it's not used widely by ordinary users, and therefore not used widely by your average corporation.

**PPS.** The [X protocol](https://en.wikipedia.org/wiki/X_Window_System) sucks. There, I said it. [NeWS](https://en.wikipedia.org/wiki/NeWS) was much cooler, it's just a pity Sun didn't have the cop on to make it open. In some ways it's a bit of a pity that [Display PostScript](https://en.wikipedia.org/wiki/Display_PostScript) and [NeXTSTEP](https://en.wikipedia.org/wiki/NeXTSTEP) (which rocked even more) or something else open and in a similar vein didn't appear first.

**PPPS.** This is making me nostalgic about RISC OS again. The only difference between printing and redrawing the screen was the drawing context. So combined with the SpriteExtend, Draw, and FontManager modules, you'd virtually the whole package there. Sigh.
