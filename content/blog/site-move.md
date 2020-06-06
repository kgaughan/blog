Title: This site has moved
Date: 2020-06-05 01:45
Category: Meta
Status: published

I have to apologise to anybody who follows my feed as you have no doubt just been flooded with a hundred or so additional entries.

I'll explain.

I've moved this site to [keith.gaughan.ie](https://keith.gaughan.ie/). I intend for this to be its final location. I've added permanent redirects for _everything_. Unfortunately, not everything respects permanent redirects, so whatever software you use to subscribe to my feed will likely be hitting the old feed URL. You would be doing me a favour if you were to update the URL in your feed reader.

Additionally, [Pelican](https://getpelican.com/), which is what I use, does not give any way to give entries and feeds IDs, which makes it impossible for me to prevent old entries from showing up.

I intend this new location to be the final time I move my blog. I'm letting as many of my domains as possible expire. If I could whittle the list down to just talideon.com and gaughan.ie, I would, but I'll need to keep stereochro.me for email and canthack.it for redirects. I very much wish I'd never used those gimmicky domain hacks in the first place.

Also, if you're a relative of mine and would like a gaughan.ie subdomain, [ping me]({filename}../pages/about.md). If you're more technical, open a pull request against my [zones](https://github.com/kgaughan/zones) repo: you'll need to modify `group_vars/all/main.yml`, adding an entry to the `zone_cnames` mapping.
