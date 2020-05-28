Getting a Dell Precision 5510 mobile workstation
================================================

:date: 2016-04-07 19:00
:category: Tech
:status: draft

Here's the executive summary: If you get a Dell Precision 5510 running Ubuntu
14.04 LTS, you will need to perform an update immediately if you want
functioning wireless. The firmware they ship with is essentially broken. Don't
bother trying to fix it yourself.

I have a few laptops still banging around the place, and it's getting time to
get rid of most of them.

.. Latitude E6300

My decision was to go with a Dell Precision 5510, which is essentially the big
brother of the XPS 13 laptops Dell has been putting out, and I quite liked my
original Project Sputnik XPS 13.

It's a really good looking machine, and I have zero complaints about the
hardware, or at least no direct complaints. Specs and the like don't matter
here. What I want to talk about is the software experience, which was a little
bit disappointing, particularly surrounding the wireless.

I'm not really so sure who deserves my ire, but I think I have to ultimately be
more annoyed with Dell than Canonical as ultimately they're the ones who
shipped me a machine with broken WiFi connectivity.

When it arrived yesterday, I booted the machine up, configured it, and tried to
connect to the company wireless network. While the machine could see all
in-range networks, it spun its wheels rather than actually connecting to it. I
tried setting up a wireless hotspot on my phone, but the effect was the same.
Checking ``/var/log/syslog`` revealed that the wireless had firmware issues.

Now, if this was some relatively obscure issue, I wouldn't be quite so annoyed.
If it had slipped with a piece of paper saying that I should do a software
update after starting the machine to solve the wireless issue, I wouldn't be
quite so annoyed, but no, there was nothing of the sort.

Dell shipped me a machine with broken wireless firmware but gave no indication
that this was the case.

How this happened is beyond me. I would expect that Dell would've tested the
particular version of Trusty on a machine before they created the image for
that would be shipped. Given that this machine doesn't even have built-in wired
ethernet, you would think this would be something that would pop out pretty
much immediately.
