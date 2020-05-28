Title: Building an RPM package: a guide for the unwilling
Date: 2008-01-16 22:31
Category: Systems Administration
Status: published
Slug: rpm-for-the-unwilling

Some day, if you're a software developer and develop software than runs on Linux, you will end up, whether you like it or not, having to build an [RPM](http://www.rpm.org/) file.

I've just spent an absolutely inordinate amount of time working out how to do this. It wasn't fun, and I don't think I'd like to ever have to do it again, so to save myself or some other poor [sod](http://www.urbandictionary.com/define.php?term=sod) similar pain, I thought I'd write up what I did here.

First, a few assumptions. Unlike most explanations of how to do this, I'm not going to be building from an tarball, so I'm not going to be covering `%prep` and all that just yet. Also, I'm building the RPM from a [tag in a subversion repository](http://svnbook.red-bean.com/en/1.1/ch04s06.html).

Before we do anything else, we need to set up our system so we can build the RPM without being root. To do that, open the file _~/.rpmmacros_ in your editor of choice and enter the following:

    %_topdir %(echo ~/rpmbuild)

This tells RPM to use _~/rpmbuild_ as its working directory. RPM requires its working directory to have a certain format, so type the following to build it:

    $ cd rpmbuild; mkdir -p BUILD RPMS/i386 SOURCES SPECS SRPMS

_BUILD_ is where the work is done, _RPMS_ is where the finished RPM is dumped, _SOURCES_  is where you drop tarballs if you're building from one, _SPECS_ is where you put your spec files, and _SRPMS_ is where finished source RPMs are dumped.

Let's get to writing the spec file, which I'm going to call _libexample.spec_. The first section of the RPM contains [metadata](http://www.rpm.org/RPM-HOWTO/build.html#HEADER), so let's write up some:

    Summary: My example library.
    Name: libexample
    Version: 0.1
    Release: 1
    Group: Development/Libraries
    Packager: J.R. Hacker <me@example.com>
    License: BSD
    BuildRoot: %{_tmppath}/%{name}-root

Most of these should be pretty self-explanatory: _Summary_ is a short human-readable summary of what the package is for; _Name_ is its actual name; _Version_ is the version of the library you're building; _Release_ is the release number of that version; _Group_ specifies the kind of package it is, _Packager_ is your name and contact details, and _License_ specifies the licensing details for the package.

The last one, _BuildRoot_ needs a little more explanation. When you're building an RPM, you're building a directory tree that will be extracted to the filesystem root of your machine when the package is installed. You don't want to pollute the directory of your machine with crap, so you need somewhere you can cleanly build it. In the case above, let's say that the value of the `%\{_tmppath}` macro is _/tmp_. This would mean that _BuildRoot_ would have the value _/tmp/libexample-root_. Similarly to how the _Name_ header is referenced here as `%{name}`, we'll be referencing _BuildRoot_ as `%{buildroot}`.

Next comes the `%description` section, which contains a longer description of the package than given in the summary. Following this is normally the `%prep` section, which we're going to ignore here and not use because we're not fiddling with tarballs. Then we have the `%build` section. This is where the first bit of real work happens, but first a quick note on the directory structure we're building.

We're exporting a single directory from SVN called _src_. This contains a makefile that build a library using [GNU libtool](http://www.gnu.org/software/libtool/) into a folder within it called _src/.libs_. The project doesn't use the [autotools](http://sources.redhat.com/autobook/), so the spec file does all the installation work after it's built. I'm using this structure because I want to demonstrate explicitly how the contents of `%{buildroot}` is built.

Here's what our `%build` section looks like:

    %build
    rm -rf src %{buildroot}
    svn export https://svn.example.com/projects/libexample/tags/0.1/src/
    (cd src; make)

When this section is being executed, RPM automatically changed to the `%{_topdir}/BUILD` directory. It's here that we do our work. The second line cleans up our environment so that we can build it. The third exports the project's _src_ directory to a directory of the same name. The third then switches to this within a subshell and executes the makefile within it. Now it's time to for the `%install` section, which is where we build the directory tree that's going to end up in the RPM.

    %install
    # Create the directory hierarchy for building our RPM.
    mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_includedir}
    # Copy whichever files that RPM will contain into it.
    install --strip --mode=0755 src/.libs/%{name}.so.0 src/.libs/%{name}.a %{buildroot}%{_libdir}
    install --mode=0755 src/%{name}.la %{buildroot}%{_libdir}
    sed -i -e s/^installed=no$/installed=yes/ %{buildroot}%{_libdir}/*.la
    install --mode=0644 src/*.h %{buildroot}%{_includedir}
    (cd %{buildroot}%{_libdir}; ln -sf %{name}.so.0 %{name}.so)
    # Build a manifest of the RPM's directory hierarchy.
    echo "%%defattr(-, root, root)" >MANIFEST
    (cd %{buildroot}; find . -type f -or -type l | sed -e s/^.// -e /^$/d) >>MANIFEST

The `%{_libdir}` and `%{_includedir}` macros specify the directories where your system installs libraries and header files. On a typical Red Hat derived system, these are going to have the values _/usr/lib_ and _/usr/include_, though this isn't necessarily what they're going to be.

Within `%{buildroot}` we need to create the directory tree that's going to end up in the RPM. We then need to copy anything that will end up in `%{_libdir}` after installation into the correct place under `%{buildroot}`, and to the same with any headers too. We use [`install`](http://unixhelp.ed.ac.uk/CGI/man-cgi?install) to make sure that permissions and ownership for all the files are correct. The fourth last line makes a symbolic link pointing whatever linkers end up linking to our library to the version of it we're installing. The second last and last lines build a manifest of the files within `%{buildroot}`. We'll be using that later to save ourselves some work. Now that our root directory hierarchy's been built, we can get on with the odds and ends.

Your RPM might need to have commands executed before or after installation and deinstallation. There are hooks for these, but I'm only going to cover two of them: `%post`, which is ran post-installation, and `%postun`, which is ran post-deinstallation. We're installing libraries, which means that after they're added and after they're removed, we need to call [`ldconfig`](http://unixhelp.ed.ac.uk/CGI/man-cgi?ldconfig) so that the dynamic linker knows about them.

    %post
    /sbin/ldconfig
    
    %postun
    /sbin/ldconfig

After the RPM is built, we need to clean up our environment again. That's what the `%clean` section is for:

    %clean
    rm -rf src %{buildroot} MANIFEST

The last section is the file manifest, which is contained within the `%files` section. Here you specify what files the RPM will contain and where they reside in the filesystem. Normally, it'd look something like this:

    %files
    %defattr(-, root, root)
    %{_libdir}/%{name}.so*
    %{_libdir}/%{name}.la
    %{_libdir}/%{name}.a
    %{_includedir}/example.h

The `%defattr` macro specifies the permissions and ownership of the files that follow it and takes three arguments: the permissions, the owner, and the group. If any of these don't matter, use a hyphen. This way, the attributes already specified on the files will be used instead.

However, we were clever earlier on and built a manifest of the contents of `%{buildroot}`, so we can just tell RPM to use that, which means the `%files` section is reduced to this:

    %files -f MANIFEST

And that's it! You should now have an RPM. Here's our finished spec file:

    Summary: My example library.
    Name: libexample
    Version: 0.1
    Release: 1
    Group: Development/Libraries
    Packager: J.R. Hacker <me@example.com>
    License: BSD
    BuildRoot: %{_tmppath}/%{name}-root
    
    %description
    A library that acts as an example of how to build an RPM.
    
    %build
    rm -rf src %{buildroot}
    svn export https://svn.example.com/projects/libexample/tags/0.1/src/
    (cd src; make)
    
    %install
    # Create the directory hierarchy for building our RPM.
    mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_includedir}
    # Copy whichever files that RPM will contain into it.
    install --strip --mode=0755 src/.libs/%{name}.so.0 src/.libs/%{name}.a %{buildroot}%{_libdir}
    install --mode=0755 src/%{name}.la %{buildroot}%{_libdir}
    sed -i -e s/^installed=no$/installed=yes/ %{buildroot}%{_libdir}/*.la
    install --mode=0644 src/*.h %{buildroot}%{_includedir}
    (cd %{buildroot}%{_libdir}; ln -sf %{name}.so.0 %{name}.so)
    # Build a manifest of the RPM's directory hierarchy.
    echo "%%defattr(-, root, root)" >MANIFEST
    (cd %{buildroot}; find . -type f -or -type l | sed -e s/^.// -e /^$/d) >>MANIFEST
    
    %post
    /sbin/ldconfig
    
    %postun
    /sbin/ldconfig
    
    %clean
    rm -rf src %{buildroot} MANIFEST
    
    %files -f MANIFEST

There's much more to creating RPMs to what I've detailed here, but this should at least give you a good start.

*Nota bene:* This was all written pretty much trail-of-though, so there may be errors and typos. If you find any before I do, post up a comment.

## References

I didn't really find anything particularly clear and informative online about building RPMs, except the [Fedora Project's RPM Guide](http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/), the [HOW-TO linked to above](http://www.rpm.org/RPM-HOWTO/), and [this oldish tutorial](http://genetikayos.com/code/repos/rpm-tutorial/trunk/rpm-tutorial.html). I also found [this one](http://www.brandonhutchinson.com/Building_an_RPM.html) after the fact, and it looks pretty decent, if terse.
