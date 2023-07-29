Title: Building Python fat RPMs with nfpm and some magic
Date: 2023-07-01 22:57
Modified: 2023-07-29 18:36
Slug: python-rpm-nfpm-and-magic
Category: Python, Hacks, Tools, DevOps
Status: published

I'd an awkward problem to solve recently: how do you build a relatively cross-platform fat RPM for a Python application without having to build out a bunch of extra build infrastructure.

On the face of it, this is easy, and this is [something I've partially solved before]({filename}python-lambdas-with-dependencies.md). I've used the same trick umpteen times before, but I hit a problem recently that has to do with how clever [rpmbuild(8)] tries to be.

Normally, this cleverness--`AutoReq` and company--is a boon: it's clever enough to pick up some packages that you'd easily forget were actual dependencies and add them, as well as making sure that the right version of the runtime you're building the package against is also an automatic dependency. But it sometimes gets in the way.

Also, writing RPM spec files can be a tad annoying.

This is why I've been investigating [nfpm] to cover the simpler cases for building RPMs. Its functionality is built into [goreleaser], which I've been using recently to help automate release management for a bunch of project I have or maintain that are written in Go, but nfpm itself is useful as an alternative to rpmbuild for building RPMs. Fundamentally, it's a cut-down version of [fpm] written in Go. It supports fewer OS package types and doesn't do anything in the way of translation between language-specific packages and OS packages, but it's quick and clean, and gets out of the way. It's possible fpm might've had some tricks that would've solved my issues, but I wasn't really thinking about it at the time, and nfpm fit neatly into the existing pipeline I was dealing with.

The problem I ran into was twofold: binary dependencies and projects that _still_ don't release wheels.

If anything, the latter was the most awkward problem.

The particular project I was dealing with releases a `requirements.txt` file with a set of properly pinned dependencies. So, here's the first approximation of installing everything into a single target directory:

```sh
.venv/bin/python -m pip install \
	--platform manylinux2014_x86_64 \
	--only-binary :all: \
	--ignore-installed \
	--no-deps \
	--abi cp38 \
	--python-version 3.8 \
	--no-compile \
	--prefix="" \
	--requirement requirements.txt \
	--target "$target"
```

Yes, Python 3.8. I had constraints. Also, the value provided to `--platform` was found though several failures to find a value that'd work. I don't have a good way to figure that out besides looking as the wheels available on PyPI. Start with `manypython1` and edge throught its variants is the only advice I can give currently.

This _partially_ works, but bombs out as soon as you hit something that only has a source distribution and no wheels. Annoyingly, this included the project I was packaging.

I had a thought: I might not be able to automagically convince `pip` into making a best attempt to translate the source package distributions into wheels automatically when `--binary :all:` is set (which is necessary for binary wheels to work at all), but I can at least identify them and move them to their own file, which I called `special-requirements.txt`. I removed the problematic requirements from `requirements.txt` and added a reference to it with the `-r` flag in their stead.

I added an extra step and a few extra environment variables: the temporary directory I was using for building in grew some extra subdirectories, including somewhere to build wheels:

```sh
tmp="$(mktemp -d)"
build_root="$tmp/buildroot"
prefix="/opt/project"
target="${build_root}${prefix}"
wheels="${tmp}/wheels"

cleanup () {
	echo "cleaning..."
	rm -rf "$tmp"
}
trap cleanup EXIT

.venv/bin/python -m pip wheel --no-deps -r special-requirements.txt -m "$wheels"
```

This worked unreasonably well, and thankfully everything resulted in pure Python wheels, but adding another index with `--extra-index-url` proved awkward.

I did some investigating and found [piprepo]. Its boto3 dependency is a bit questionable, but it at least meant that I could take the directory of wheels I'd produced and turn it into something that `pip` would let me use with `--extra-index-url`:

```sh
.venv/bin/pip install piprepo
# ...
.venv/bin/piprepo build "$wheels"

.venv/bin/python -m pip install \
	--extra-index-url "file://$wheels/simple/" \
	--platform manylinux2014_x86_64 \
	--only-binary=:all: \
	--ignore-installed \
	--no-deps \
	--abi cp38 \
	--python-version 3.8 \
	--no-compile \
	--prefix="" \
	--requirement requirements.txt \
	--target "$target"
```

At this point, I was _really_ close to having something working, but the issue of shebangs remained. To fix this, I added the following small executable called `pyshim`:

```sh
#!/bin/sh
PYTHONPATH=/opt/project exec python3.8 "$@"
```

And to the build script, this:

```sh
sed -E -i -e "s,#!.*,#!$prefix/bin/pyshim,g" $target/bin/*
```

This way, the module search for these executables is remapped to the proper location.

Apologies for the GNU-isms, but we're dealing with RPMs.

I finally had something I could use to build the final package:

```sh
nfpm package --packager rpm --config "nfpm.yaml"
```

Obviously, the path was less obvious, but the result was a usable package. I'm hoping I can use this in a few other places, and if you're in a position where you have to do something similar with Python or another language it'll save you some time.

**Updated 2023-07-29 18:36:**: mergemanifest.py was unnecessary: I'd missed `type: tree` in the manifest documentation, which allowed me to graft the tree into the RPM.

[rpmbuild(8)]: https://linux.die.net/man/8/rpmbuild
[nfpm]: https://nfpm.goreleaser.com/
[goreleaser]: https://goreleaser.com/
[piprepo]: https://github.com/colinhoglund/piprepo
