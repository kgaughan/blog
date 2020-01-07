Title: Listening for file updates on Windows
Slug: windows-listen-file-changes
Date: 2004-10-06 22:15
Category: Coding
Status: published

I'd really like to know if there's a way to set up a callback of some kind that would allow a program to be informed of when a certain file is updated. Not just _any_ file, but a particular file.

I've taken a look through [MSDN](http://msdn.microsoft.com/), disorganised heap that it is, without the slightest bit of luck. If anybody out there knows how, I'd love if somebody'd contact me and tell me. I don't want to have to run a thread that would cycle through a list of files, checking to see if their datestamps have changed, which is the alternative.

I know this is possible on Linux and a few other \*nixen, but I need this on Windows.

I'm going to hack my comments system back into working tonight, along with a few other changes to the system, and I hope to have it back running tomorrow morning (UTC).

**Update**: I found [this article](https://www.desaware.com/tech/filemonitoring.aspx) and [this one](https://web.archive.org/web/20081015170702/http://www.relisoft.com/win32/watcher.html) that mention [FindFirstChangeNotification](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-findfirstchangenotificationa). Now _there_'s an system call that could do with a more obvous name, maybe _CreateFileChangeNotificationEvent_ or something.
