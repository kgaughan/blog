Title: Initial explorations of the Agon Light
Slug: agon-light-explorations
Category: Retrocomputing, Agon Light
Date: 2023-01-26 21:06:20
Status: published

The Agon Light doesn't have an equivalent of the "programmer's reference guides" of old, so I've been doing some poking around in different places to see what information I can gather together.

There's an [agon-light](https://github.com/topics/agon-light) tag on Github that lists a few interesting repositories. In particular, [Agon Forth](https://github.com/lennart-benschop/agon-forth) looks like a fun alternative to using BBC BASIC, giving it more of a [Jupiter Ace](https://en.wikipedia.org/wiki/Jupiter_Ace). The [agon-flash](https://github.com/envenomator/agon-flash) repo may be useful for firmware upgrades in future. The [agon-utilities](https://github.com/lennart-benschop/agon-utilities) repo has a few things I was thinking I'd have to write myself, such as a tool for loading fonts, a text editor, and a pager for reading files on mass storage.

The [Quark MOS](https://github.com/breakintoprogram/agon-mos) repo contains [an API manual](https://github.com/breakintoprogram/agon-mos/blob/main/API.md) and the README in the root of the repo clears up some issues I was having such as the star commands not always corresponding to what I expected from RISC OS (which borrowed heavily from the BBC Model B's MOS), and pointed at a solution to a minor issue I had, which is that my Agon Light 2 was set up to use a US keyboard by default, but we use a very similar layout to the UK here in Ireland (the input method for extended characters is the main difference), and it turns out all I need to do it edit `autoexec.txt` and change `SET KEYBOARD 1` to `SET KEYBOARD 0`. The [VDP firmware](https://github.com/breakintoprogram/agon-vdp) includes a [list of VDU driver command](https://github.com/breakintoprogram/agon-vdp/blob/main/MANUAL.md). It's a little rough and ready, as not all the limits are explained nor is there a description of the palette (though it supports 64 colours, IIRC), but I'm expecting those can be gleaned from reading the firmware, which is written in the Arduino dialect of C++. [This repo](https://github.com/envenomator/Agon) has a bit more information on the sprite VDU commands and some more information on the memory map, and some C libraries.

There's [a version of CP/M](https://bitbucket.org/cocoacrumbs/agon-light-cpm/src/master/) for the Agon Light, though it requires [a custom VDP firmware](https://bitbucket.org/cocoacrumbs/agon-vpd-cpm/src/master/) at present to run. I haven't looked at that as yet.

I found [a repo with some useful-looking sample programs in Z80 assembler](https://github.com/schur/Agon-Light-Assembly), including some include files and some information on the the [spasm-ng](https://github.com/alberthdev/spasm-ng) assembler as an alterative to using Zilog Developer Studio. It's apparently modelled off of [TASM](https://en.wikipedia.org/wiki/Turbo_Assembler), which I used ages ago, so it shouldn't be difficult to dig up documentation on the assembler's directives.

The [eZ80](https://en.wikipedia.org/wiki/Zilog_eZ80) processor seems to have to modes: classic Z80 mode, and "ADL mode", which allows a 24-bit address space (16MB) to be accessed. I found [an article describing the eZ80](https://www.chibiakumas.com/ez80/) and how it differs from the Z80, which may be useful for bigger programs, though the Agon Light has only 512KB of memory, not 16MB. [This issue in the MOS repo](https://github.com/breakintoprogram/agon-mos/issues/8) implies that this may not work exactly as expected, but it's worth experimenting with.

As far as games go, there's [a version of Sokoban](https://github.com/envenomator/agon-sokoban).

I'm on the lookout for a VGA to HDMI converter that might, which any luck, work well with one of my monitors. The HP LA2405x on my desk _really_ doesn't like the Agon Light's mode 2 VGA output, but I've an older Benq monitor that works with it just fine. If I can, I'd prefer to use the HP monitor, as the Benq is hooked up to the dock for my Steam Deck.
