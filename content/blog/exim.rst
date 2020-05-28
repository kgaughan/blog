Progression of mail management on a Debian box
==============================================

:slug: exim-debian-progression
:date: 2016-05-26 16:31:00
:category: Tech
:status: published


1. Ah, I just need to deal with local mail, so I'll have Debian configure Exim
   for that. After all, it's already there.
2. Huh. Seems I need to send some mail from this box. I'll have Debian
   reconfigure Exim to use a smarthost for non-local mail.
3. Huh. Seems I need to listen for incoming mail. I'll just have Debian
   reconfigure Exim to recieve mail for a bunch of domains and have it deliver
   to local users.
4. Huh. Seems I need to set up some virtual hosting as I need to route email
   in non-trivial ways. I can't be that hard...

...three hours pass...

5. Aaarrgh! ``sudo apt install postfix``
