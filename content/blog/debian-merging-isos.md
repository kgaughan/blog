Title: Merging .iso files on Debian, Ubuntu, and most likely Linux in general
Date: 2008-01-25 23:52
Slug: debian-merging-isos
Category: Systems Administration
Status: published

I hardly ever have to do this, so I can never remember precisely how to do it. Hopefully by noting it here, I won't forget again.

Specifically, I want to do this so that I can create a single DVD image from the FreeBSD 6.3 CD images I have. Here's more-or-less how it goes:

```sh
mount -t iso9660 -o loop disc1-mountpoint
mount -t iso9660 -o loop disc2-mountpoint
mkisofs -l -J -R -o dvd.iso disc1-mountpoint disc2-mountpoint
```

Don't forget to unmount those mountpoints afterwards.

Here's a shell script to do the work. It assumes it's in a directory with a subdirectory called isos, which contains the source .iso images. It has no error handling, so the usual caveats apply:

```sh
#!/bin/sh

rm -rf mnt contents
mkdir mnt contents
for i in isos/*.iso; do
    mount -t iso9660 -o loop $i mnt
    cp -av mnt/* contents
    umount mnt
done

# This bit is specific to merging FreeBSD .isos.
sed -i -e 's/^CD_VOLUME = .$/CD_VOLUME = 1/' contents/cdrom.inf
sed -i -e 's/|.$/|1/' contents/packages/INDEX

mkisofs -l -J -R -o dvd.iso contents
rm -rf mnt contents
```

And here's how you [merge several .iso files into a single one on FreeBSD](https://web.archive.org/web/20100110041833/http://mexinetica.com/~lanjoe9/freebsd/bsd_dvd_howto.html), and [how to do it for FreeBSD .iso images](https://web.pa.msu.edu/people/tigner/bsddvd.html).
