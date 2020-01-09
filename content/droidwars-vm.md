Title: Old Ideas: My DroidWars VM
Date: 2008-06-04 19:25
Category: Project Ideas
Slug: droidwars-vm
Status: published

Years and years ago, I started work on a game I called “DroidWars”. It was based on some misunderstood third-hand information I got about [Core Wars](http://www.koth.org/), and rather than having program battle each other directly, each of the programs controlled a robot in a 2D virtual world.

It was written in [BBC BASIC V](http://en.wikipedia.org/wiki/BBC_BASIC#Acorn_Archimedes_(RISC_OS)), about the only BASIC dialect I've used that wasn't braindead. I hadn't got around to learning [ARM](http://en.wikipedia.org/wiki/ARM_architecture) assembly language just yet, though I did have a smattering from reading other people's code, and didn't have a C compiler that would run on my, at the time 1MB but later upgraded to a whopping 4MB, [A3010](https://web.archive.org/web/20081122001249/http://atterer.net/acorn.html), so the thing crawled like you wouldn't believe. Oh, if I'd only had a copy of the awesome [StrongHelp](https://web.archive.org/web/20081122001249/http://sudden.recoil.org/stronghelp/) sooner...

I got a reasonable amount of it done. The arena visualisation worked but was incredibly simplistic looking, and I developed a simple VM for the robots to have their code run in.

The reasons for the VM were twofold: I wanted the robots to be isolated from each other, and I wanted them isolated from my code. Aside from practicalities of namespace collisions, I wanted to make sure that competing robots couldn't reach into the game code or the code of another robot and interfere with it.

The project was abandoned when I got bogged down writing a compiler for the high-level DroidCode language. To imagine what it looked like, imagine the primitive bastard child of BBC BASIC, [Logo](http://en.wikipedia.org/wiki/Logo_(programming_language)), and [Lua](http://www.lua.org/). It never got very far because I didn't understand very much at the time about the subtleties of lexing, parsing or anything compiler-related. Oh, the naivety.

The one part I _did_ get done was the VM. It had one nifty idea I thought I'd share. I can't remember any specifics of the VM's workings, mind, so don't bother asking. If I manage to dig up the code for it from the floppy it was on and if entropy hasn't got it yet, I might post up more details.

The VM was a kind of a hybrid of a stack machine and a register machine. The stack started at the bottom of memory and grew upwards, and all the registers except the stack register itself, _including the program counter_ were mapped directly onto the stack. If this was implemented in silicon, the processor would probably have a small amount of on-board RAM that would shadow the top of the stack for fast access.

The layout of the stack, if I remember correctly, was as follows. The top-most element was a 32-bit process counter similar the ARM's R15\. It consisted of a number of flags, the counter itself, and the size of the current stack record. A subroutine jump consisted of pushing a new stack record containing the arguments and a new PC onto the top of the stack, and returning was a matter of removing the topmost record. I vaguely remember that the instruction to do this came in two forms, one of which preserved the current PC's flags and one of which ignored the current PC's flags.

After the PC came the other registers. There were fifteen, if I recall, including the PC. R1 was the topmost, continuing onto R14, the bottommost. R15 was the stack register, and, as mentioned previously, was an on-board register.

Because each stack frame was variable sized, this meant that it was possible for a routine to see its calling routine as the registers of the calling and called routines overlapped.

I'm not sure if there's any other machines, real or virtual, that use a similar design, but I thought it was interesting enough to share, and it might have some virtues over conventional register architectures and stack architectures, but I think I'll leave that to people more knowledgeable than myself.
