Title: Introducing Planet Mercury
Category: Planet Mercury, Projects, Go, Slow Web
Date: 2020-06-22 21:27
Status: published

Planet Mercury is a [Planet](https://en.wikipedia.org/wiki/Planet_(software))-style feed aggregator I've been writing in Go over the past few days.

It's now at the Minimal Viable Product stage, so I figure there's no harm in announcing its existence to the world. If you want to poke around the currenty quite messy codebase, [it's on Github](https://github.com/kgaughan/mercury/).

## What's a planet?

A planet is a kind of simple feed aggregator that takes a set of newsfeeds, splices them together in reverse chronological order, and spits them out as pages.

## Quickstart

If you have Go installed, you can check out the repo and build it:

```console
$ git clone https://github.com/kgaughan/mercury.git
$ make
```

It'll produce an 8MB binary called _mercury_.

By default, _mercury_ will look for a file called _mercury.toml_ in the current directory. If you check out the repo and run it, you'll get a very basic site written to the _output_ directory. The contents of _mercury.toml_ should be self-explanatory. As far as templating goes, it expects the theme directory contains at least a file called _index.html_, which contains the template to use when generating each page of the aggregator. This needs proper documentation, but under the hood it uses Go's [html/template](https://golang.org/pkg/html/template/) engine. If you're familiar with that, then you should be able to work out what's going on from _main.go_ and _entry.go_.

## Why?

First and foremost, I'd previously used [Sam Ruby](http://intertwingly.net/blog/)'s [Planet Venus](https://github.com/rubys/venus/), but that codebase is now moribund, and not even the people who took over development on it after Sam stopped maintaining it are doing any work on it now. I'd tried to get some patches in to fix some issues, and get it ported to Python 3, but my efforts were for nothing.

Second of all, I needed projects to keep me occupied during the COVID 19 lockdown, and this seemed like a good one: it's a chance to practice coding in Go, and gives me a chance to prototype some ideas for another feed aggregator project I'm planning on reviving.

Thirdly, I wanted to see if I could get the MVP written in under 500 lines of code, which I did!

```console
$ wc -l *.go
  89 cacheitem.go
  42 config.go
  13 duration.go
  77 entry.go
  59 feedqueue.go
 131 main.go
  52 manifest.go
 463 total
```

Finally, after [abandoning Twitter]({filename}leaving-twitter.md), I'm looking to re-embrace [The Slow Web](https://jackcheng.com/the-slow-web/).

## What's left to do?

Currently, it doesn't have good support for paging. It doesn't do any HTML sanitisation, but I'm looking at [bluemonday](https://github.com/microcosm-cc/bluemonday) for that. I'd like to introduce [hackergotchi](https://fedoraproject.org/wiki/Hackergotchi) support, and give the option for it to produce an [Atom](https://tools.ietf.org/html/rfc4287) feed of whatever's been generated. The code for fetching feeds is currently entirely serial, but could easily be updated to process feeds concurrently.

Above all, it needs a proper theme, some documentation, and a lot of cleanup.

[Update: there was an annoying bug in the feed splicing code, where it ended up not maintaining the heap property as it spliced the feeds together. That's been fixed, and it now has a passable basic theme.] 
## Alternatives

There are a few other Planet-style aggregators I know of under active maintenance: [Planet Pluto](https://github.com/feedreader/), which is written in Ruby, and [moonmoon](https://moonmoon.org/)
