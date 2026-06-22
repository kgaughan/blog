Title: Creating a signed RPM with nFPM and GnuPG
Date: 2026-06-21 22:53
Category: Systems Administration, DevOps, Security
Status: published

I have a need to be able to build a signed RPM, which isn't something I've done before.The RPM that I need is a simple one that's well-suited to [nFPM](https://nfpm.goreleaser.com/), which supports building signed RPMs. nFPM definitely isn't the hard part here: the hard part is using [GnuPG](https://gnupg.org/), a piece of software with a notoriously arcane interface. I haven't done anything with GnuPG in maybe two decades (outside of signing archives of stuff to be sent to Iron Mountain, and even that was almost twenty years ago), so I'm almost starting from scratch.

!!! note
    Obviously, I'm just a clueless software engineer, not a security professional, so take everything here with a grain of salt.

## Setup

Let's start by making sure I have a suitable directory for the configuration. Given GnuPG will (rightly) complain if the directory is world-readable, let's make sure it's only readable by my user while we're at it:

```sh
mkdir -m 700 ~/.gnupg
```

And to show that I'm starting from scratch, let's list the keys:

```console
$ gpg --list-keys
gpg: keybox '.../.gnupg/pubring.kbx' created
gpg: .../.gnupg/trustdb.gpg: trustdb created
```

Nothing's listed, and it's created the keybox and trustdb files as they don't already exist.

### Generating the master key

Let's create a key (with minor redactions):

```console
$ gpg --generate-key
Note: Use "gpg --full-generate-key" for a full featured key generation dialog.

GnuPG needs to construct a user ID to identify your key.

Real name: Keith Gaughan
Email address: ***@gaughan.ie
You selected this USER-ID:
    "Keith Gaughan <***@gaughan.ie>"

Change (N)ame, (E)mail, or (O)kay/(Q)uit? o
...
gpg: directory '.../.gnupg/openpgp-revocs.d' created
gpg: revocation certificate stored as '.../.gnupg/openpgp-revocs.d/1CA311670FDC16FD072CAAD91E2DC7275C63D2D5.rev'
public and secret key created and signed.

pub   ed25519 2026-06-21 [SC] [expires: 2029-06-20]
      1CA311670FDC16FD072CAAD91E2DC7275C63D2D5
uid                      Keith Gaughan <***@gaughan.ie>
sub   cv25519 2026-06-21 [E] [expires: 2029-06-20]
```

!!! note
    There's also a flag called `--quick-generate-key` that allows you to do all this without the prompts.

That's generated a key with the fingerprint `1CA311670FDC16FD072CAAD91E2DC7275C63D2D5`. It looks like `gpg` no longer prints the key ID, only the fingerprint, by default. My understanding is that the letters inside square brackets indicate what a particular key can be used for, where `S` means 'signing' (i.e., it can be used for signing things), `E` means 'encryption' (i.e., it can be used for encrypting files), and `C` means 'certification' (i.e., the key can have subkeys that are certified by this key), thus the master key can be used for signing and certification, while the subkey that was created at the same time can be used for encryption.

## Generating a subkey for signing

It's probably not a great idea to use your master key for signing, so a subkey specifically for signing that's been signed by the master key is probably a good idea, not least because it can have a much shorter lifetime than the master key.

For an explanation of why I'm specifying `ed25519`, [see this Stack Exchange post](https://crypto.stackexchange.com/questions/27866/why-curve25519-for-encryption-but-ed25519-for-signatures). The master key has a lifetime of three years, so I'll have this signing key expire after one year, hence `1y`:

```console
$ gpg --quick-add-key 1CA311670FDC16FD072CAAD91E2DC7275C63D2D5 ed25519 sign 1y
...
$ gpg --list-keys
gpg: checking the trustdb
gpg: marginals needed: 3  completes needed: 1  trust model: pgp
gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
gpg: next trustdb check due at 2029-06-20
.../.gnupg/pubring.kbx
----------------------
pub   ed25519 2026-06-21 [SC] [expires: 2029-06-20]
      1CA311670FDC16FD072CAAD91E2DC7275C63D2D5
uid           [ultimate] Keith Gaughan <***@gaughan.ie>
sub   cv25519 2026-06-21 [E] [expires: 2029-06-20]
sub   ed25519 2026-06-21 [S] [expires: 2027-06-21]
```

## Building an RPM and signing it: two approaches

I'll use a pretty simple project of mine for this: [socketmap-sql](https://github.com/kgaughan/socketmap-sql/), which I use for managing how my mailserver routes incoming mail. If you want to learn more about this, read [socketmap_table(5)](https://www.postfix.org/socketmap_table.5.html) in the Postfix documentation.

I'll start with dropping a small script for invoking nFPM into the root of the repo called `package.sh`:

```sh
#!/bin/sh

set -e

# Extract the most recent tag number; falls back to v0.0.0 is there's none
export VERSION=$(git describe --tags --abbrev=0 || echo "v0.0.0")

# Ensure the packaged files have a stable mtime based on the date of the
# most recent commit. See: https://reproducible-builds.org/docs/source-date-epoch/
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)

# Trigger the build
nfpm package --packager rpm
```

I'll also create a file called `nfpm.yaml` in repo containing the configuration for nFPM itself:

```yaml
---
name: socketmap-sql
arch: all
version: $VERSION
depends:
  - python3
maintainer: "Keith Gaughan <sendallyourspamhere@stereochro.me>"
description: |
   A socketmap script for interfacing with an SQL database.
homepage: "https://github.com/kgaughan/socketmap-sql/"
license: MIT

contents:
  - src: ./socketmapsql.py
    dst: /usr/libexec/socketmap-sql
    file_info:
      mode: 0755
```

And now I'll build it:

```console
$ ./package.sh 
using rpm packager...
created package: socketmap-sql-0.2.0-1.noarch.rpm
$ rpm --checksig -v socketmap-sql-0.2.0-1.noarch.rpm
socketmap-sql-0.2.0-1.noarch.rpm:
    Header SHA256 digest: OK
    Payload SHA256 digest: OK
```

So it's not signed, otherwise it'd mention a header and payload signature too.

### rpmsign

The RPM toolchain includes [`rpmsign`](https://rpm.org/docs/latest/man/rpmsign.1) for signing unsigned RPMs. Let's see what breaks if we run it to sign the RPM without any extra configuration:

```console
$ rpmsign --addsign socketmap-sql-0.2.0-1.noarch.rpm 
You must set "%_gpg_name" in your macro file
```

Predictably, it didn't work. It looks like I'll need to put some stuff in `~/.config/rpm/macros`:

```
%_gpg_name Keith Gaughan <***@gaughan.ie>
```

My assumption here is that `rpmsign` will use the subkey for signing, but I can't be sure, because the name associated with the key is a little ambiguous. There's a better way to specify the key in more recent versions of RPM than the version I'm using (4.20.1 as is packaged for Debian Trixie) by specifying it with the `%_openpgp_sign_id` macro.

Now let's try again:

```console
$ ./package.sh
using rpm packager...
created package: socketmap-sql-0.2.0-1.noarch.rpm
$ rpmsign --addsign socketmap-sql-0.2.0-1.noarch.rpm
socketmap-sql-0.2.0-1.noarch.rpm:
$ rpm --checksig -v socketmap-sql-0.2.0-1.noarch.rpm
socketmap-sql-0.2.0-1.noarch.rpm:
    Header V4 EdDSA/SHA256 Signature, key ID 1e64396b: NOKEY
    Header SHA256 digest: OK
    Payload SHA256 digest: OK
```

The `NOKEY` indicates that I haven't had RPM import the key, so it can't be verified. For our purposes, that's fine. We can check if my earlier assumption was correct by exporting the keys and searching for the key ID `1E64396B`:

```console
$ gpg -a --export | gpg --list-packets
...
# off=425 ctb=b8 tag=14 hlen=2 plen=51
:public sub key packet:
        version 4, algo 22, created 1782071536, expires 0
        pkey[0]: [80 bits] ed25519 (1.3.6.1.4.1.11591.15.1)
        pkey[1]: [263 bits]
        keyid: 16561EBD1E64396B
# off=478 ctb=88 tag=2 hlen=2 plen=245
:signature packet: algo 22, keyid 1E2DC7275C63D2D5
        version 4, created 1782071536, md5len 0, sigclass 0x18
        digest algo 8, begin of digest 8b 7a
        hashed subpkt 33 len 21 (issuer fpr v4 1CA311670FDC16FD072CAAD91E2DC7275C63D2D5)
        hashed subpkt 2 len 4 (sig created 2026-06-21)
        hashed subpkt 27 len 1 (key flags: 02)
        hashed subpkt 9 len 4 (key expires after 1y0d0h0m)
        subpkt 16 len 8 (issuer key ID 1E2DC7275C63D2D5)
        subpkt 32 len 117 (signature: v4, class 0x19, algo 22, digest algo 8)
        data: [255 bits]
        data: [255 bits]
```

It appears my assumption was correct! If it's not clear from this, even without looking up the meaning of any of the other fields, I can tell that this is the signing key because of `key expires after 1y0d0h0m`, which is a big clue that this is the signing subkey I created.

### with nFPM itself

With nFPM, we need to export the secret keys as it needs to be read by nFPM, which appears to not be able to talk to `gnupg-agent`:

```console
$ gpg --export-secret-keys --armor 1CA311670FDC16FD072CAAD91E2DC7275C63D2D5 > signing.gpg
```

Let's update `nfpm.yaml` to reference the exported keys:

```yaml
rpm:
  signature:
    key_file: signing.gpg
```

And now let's attempt to generate a signed RPM:

```console
$ ./package.sh
using rpm packager...
          
   ERROR  
          
  Failed to create signatures: call to signer failed: signing error: key is encrypted but no passphrase was provided.
```

This is because I'd added a passphrase to my master key. To allow this to be prompted, let's add something to the top of `package.sh`, just after `set -e`:

```sh
usage () {
    cat <<FIN
Usage:
    $0 [-P]
    $0 -h

Flags:
    -h  show this help
    -P  prompt for a passphrase; setting NFPM_PASSPHRASE makes this a no-op

FIN
}

while getopts "hP" opt; do
    case "$opt" in
        h)
            usage
            exit 0
            ;;
        P)
            prompt=1
            ;;
        *)
            usage 2>&1
            exit 1
            ;;
    esac
done

if test "${prompt:-}" = "1" -a -z "${NFPM_PASSPHRASE:-}"; then
    stty -echo
    read -p "passphrase> " NFPM_PASSPHRASE
    stty echo
    echo
    export NFPM_PASSPHRASE
fi
```

And now let's try it:

```console
$ ./package.sh -P
passphrase>
using rpm packager...
created package: socketmap-sql-0.2.0-1.noarch.rpm
$ rpm --checksig -v socketmap-sql-0.2.0-1.noarch.rpm
socketmap-sql-0.2.0-1.noarch.rpm:
    Header V4 EdDSA/SHA256 Signature, key ID 1e64396b: NOKEY
    Header SHA256 digest: OK
    Payload SHA256 digest: OK
    V4 EdDSA/SHA256 Signature, key ID 1e64396b: NOKEY
```

Bingo! It also seems that nFPM signs more parts of the file than `rpmsign` does. Whether this is useful (because I assume that the payload digest is in the header, and in that case the signed header ought to be enough) is another question, but it's certainly no harm. My assumption is that `rpmsign`'s `--signfiles` flag will trigger the same behaviour as nFPM, but I haven't checked this.

## Topics for followup

There are a few obvious topics to follow up upon at some point:

 * Backing up keys
 * Configuring a YUM repo and setting up GPG keys on it
