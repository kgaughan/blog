Title: Notes from Real World OCaml, first edition
Slug: rwocaml-1
Category: Coding
Date: 2023-01-14 23:10
Modified: 2023-01-20 23:07
Series: Real World OCaml
Status: published

Because it's been so long since I've done anything in OCaml, I'm going through [Real World OCaml](https://realworldocaml.org). I have the first edition, and though [the second edition](https://www.cambridge.org/core/books/real-world-ocaml-functional-programming-for-the-masses/052E4BCCB09D56A0FE875DD81B1ED571) came out earlier this month, it's the original that I'm going through. I'm hoping this is useful for anyone who has the original but hits issues with it, because it makes some assumptions as it depends on things like [utop](https://opam.ocaml.org/packages/utop/) and an alternative standard library, [base](https://opam.ocaml.org/packages/base/), from Jane Street.

I'll be checking everything on both MacOS 12.6 (Monterey) and Ubuntu 22.10 (Kinetic Kudu), and documenting anything odd I ran into.

I'll just be going over chapter 1 ("A guided tour") in this entry.

## MacOS

On MacOS, install `opam`, which will also install `ocaml` itself from Homebrew:

```console
$ brew install opam
$ opam init
No configuration file found, using built-in defaults.
Checking for available remotes: rsync and local, git.
  - you won't be able to use mercurial repositories unless you install the hg command on your system.
  - you won't be able to use darcs repositories unless you install the darcs command on your system.


<><> Fetching repository information ><><><><><><><><><><><><><><><><><><><>  🐫
[default] Initialised

<><> Required setup - please read <><><><><><><><><><><><><><><><><><><><><>  🐫

  In normal operation, opam only alters files within ~/.opam.

  However, to best integrate with your system, some environment variables
  should be set. If you allow it to, this initialisation step will update
  your fish configuration by adding the following line to ~/.config/fish/config.fish:

    source $HOME/.opam/opam-init/init.fish > /dev/null 2> /dev/null; or true

  Otherwise, every time you want to access your opam installation, you will
  need to run:

    eval (opam env)

  You can always re-run this setup with 'opam init' later.

Do you want opam to modify ~/.config/fish/config.fish? [N/y/f]
(default is 'no', use 'f' to choose a different file)
<><> Creating initial switch 'default' (invariant ["ocaml" {>= "4.05.0"}] - initially with ocaml-system)

<><> Installing new switch packages <><><><><><><><><><><><><><><><><><><><>  🐫
Switch invariant: ["ocaml" {>= "4.05.0"}]

<><> Processing actions <><><><><><><><><><><><><><><><><><><><><><><><><><>  🐫
∗ installed base-bigarray.base
∗ installed base-threads.base
∗ installed base-unix.base
∗ installed ocaml-system.4.14.0
∗ installed ocaml-config.2
∗ installed ocaml.4.14.0
Done.
# Run eval (opam env --switch=default) to update the current shell environment
```

Note that I use [fish](https://fishshell.com/). This will vary for you depending on your shell.

## Ubuntu (and pretty much any other Debian-based distro)

It's not tremendously different from MacOS:

```console
$ sudo apt install opam
[sudo] password for keith:
...
$ opam init

<><> Required setup - please read <><><><><><><><><><><><><><><><><><><><><><><>

  In normal operation, opam only alters files within ~/.opam.

  However, to best integrate with your system, some environment variables
  should be set. If you allow it to, this initialisation step will update
  your fish configuration by adding the following line to ~/.config/fish/config.fish:

    source $HOME/.opam/opam-init/init.fish > /dev/null 2> /dev/null; or true

  Otherwise, every time you want to access your opam installation, you will
  need to run:

    eval (opam env)

  You can always re-run this setup with 'opam init' later.

Do you want opam to modify ~/.config/fish/config.fish? [N/y/f]
(default is 'no', use 'f' to choose a different file) y
A hook can be added to opam's init scripts to ensure that the shell remains in sync with the opam environment when they are loaded. Set that up? [y/N] y

User configuration:
  ~/.config/fish/config.fish is already up-to-date.
```

Much the same as on MacOS.

## Potential MANPATH corruption with older versions of OPAM

Previously, I've found that running `eval $(opam env)` has corrupted `MANPATH`. If you hit this issue, then try `eval (opam env | sed "s/MANPATH '\//MANPATH ':\//")` instead. This inserts a colon at the start of `MANPATH` so the default manpage paths are still included. [This issue was fixed in opam](https://github.com/ocaml/opam/issues/3878) a few years ago, but if you're working with an older version, it still may affect you.

## OPAM

Here's what packages are installed for me by default:

```console
$ opam list --installed
# Packages matching: installed
# Name        # Installed # Synopsis
base-bigarray base
base-threads  base
base-unix     base
ocaml         4.14.0      The OCaml compiler (virtual package)
ocaml-config  2           OCaml Switch Configuration
ocaml-system  4.14.0      The OCaml compiler (system version, from outside of opam)
```

No `utop`, so let's install that:

```console
$ opam install utop
The following actions will be performed:
  ∗ install ocamlfind         1.9.5  [required by utop]
  ∗ install dune              3.6.1  [required by utop]
  ∗ install ocamlbuild        0.14.2 [required by logs]
  ∗ install base-bytes        base   [required by ocplib-endian]
  ∗ install trie              1.0.0  [required by mew]
  ∗ install result            1.5    [required by zed]
  ∗ install csexp             1.5.1  [required by dune-configurator]
  ∗ install cppo              1.6.9  [required by utop]
  ∗ install uchar             0.0.2  [required by zed]
  ∗ install topkg             1.0.6  [required by logs]
  ∗ install mew               0.1.0  [required by mew_vi]
  ∗ install dune-configurator 3.6.1  [required by lwt]
  ∗ install ocplib-endian     1.2    [required by lwt]
  ∗ install uutf              1.0.3  [required by zed]
  ∗ install react             1.2.2  [required by utop]
  ∗ install lwt               5.6.1  [required by utop]
  ∗ install uucp              15.0.0 [required by zed]
  ∗ install mew_vi            0.5.0  [required by lambda-term]
  ∗ install lwt_react         1.2.0  [required by utop]
  ∗ install logs              0.7.0  [required by utop]
  ∗ install uuseg             15.0.0 [required by zed]
  ∗ install zed               3.2.1  [required by utop]
  ∗ install lambda-term       3.3.1  [required by utop]
  ∗ install utop              2.11.0
===== ∗ 24 =====
Do you want to continue? [Y/n] y

<><> Processing actions <><><><><><><><><><><><><><><><><><><><><><><><><><>  🐫
⬇ retrieved csexp.1.5.1  (https://opam.ocaml.org/cache)
⬇ retrieved cppo.1.6.9  (https://opam.ocaml.org/cache)
⬇ retrieved lambda-term.3.3.1  (https://opam.ocaml.org/cache)
⬇ retrieved logs.0.7.0  (https://opam.ocaml.org/cache)
⬇ retrieved dune.3.6.1  (https://opam.ocaml.org/cache)
⬇ retrieved lwt_react.1.2.0  (https://opam.ocaml.org/cache)
⬇ retrieved lwt.5.6.1  (https://opam.ocaml.org/cache)
⬇ retrieved mew.0.1.0  (https://opam.ocaml.org/cache)
⬇ retrieved mew_vi.0.5.0  (https://opam.ocaml.org/cache)
⬇ retrieved ocamlbuild.0.14.2  (https://opam.ocaml.org/cache)
⬇ retrieved dune-configurator.3.6.1  (https://opam.ocaml.org/cache)
⬇ retrieved ocamlfind.1.9.5  (https://opam.ocaml.org/cache)
⬇ retrieved ocplib-endian.1.2  (https://opam.ocaml.org/cache)
⬇ retrieved result.1.5  (https://opam.ocaml.org/cache)
⬇ retrieved react.1.2.2  (https://opam.ocaml.org/cache)
⬇ retrieved trie.1.0.0  (https://opam.ocaml.org/cache)
⬇ retrieved topkg.1.0.6  (https://opam.ocaml.org/cache)
⬇ retrieved uchar.0.0.2  (https://opam.ocaml.org/cache)
⬇ retrieved uuseg.15.0.0  (https://opam.ocaml.org/cache)
⬇ retrieved utop.2.11.0  (https://opam.ocaml.org/cache)
⬇ retrieved uutf.1.0.3  (https://opam.ocaml.org/cache)
⬇ retrieved uucp.15.0.0  (https://opam.ocaml.org/cache)
⬇ retrieved zed.3.2.1  (https://opam.ocaml.org/cache)
∗ installed ocamlfind.1.9.5
∗ installed base-bytes.base
∗ installed ocamlbuild.0.14.2
∗ installed uchar.0.0.2
∗ installed topkg.1.0.6
∗ installed uutf.1.0.3
∗ installed react.1.2.2
∗ installed dune.3.6.1
∗ installed trie.1.0.0
∗ installed result.1.5
∗ installed csexp.1.5.1
∗ installed mew.0.1.0
∗ installed cppo.1.6.9
∗ installed ocplib-endian.1.2
∗ installed mew_vi.0.5.0
∗ installed dune-configurator.3.6.1
∗ installed lwt.5.6.1
∗ installed lwt_react.1.2.0
∗ installed logs.0.7.0
∗ installed uucp.15.0.0
∗ installed uuseg.15.0.0
∗ installed zed.3.2.1
∗ installed lambda-term.3.3.1
∗ installed utop.2.11.0
Done.
```

Quite a monstrous list of dependencies!

If you try to execute `open Core`[^core] in the `utop` REPL at this point, it won't be able to find it, and respond `Error: Unbound module Core`. Let's fix that:

[^core]: `Core.Std` was merged into `Core`, so substitute any mentions of `Core.Std` with `Core` in the book.

```console
$ opam install core
The following actions will be performed:
  ∗ install ppx_derivers                1.2.1   [required by ppxlib]
  ∗ install seq                         base    [required by re]
  ∗ install sexplib0                    v0.15.1 [required by base]
  ∗ install stdlib-shims                0.3.0   [required by ppxlib]
  ∗ install jane-street-headers         v0.15.0 [required by core]
  ∗ install num                         1.4     [required by sexplib]
  ∗ install ocaml-compiler-libs         v0.12.4 [required by ppxlib]
  ∗ install re                          1.10.4  [required by ppx_expect]
  ∗ install base                        v0.15.1 [required by core]
  ∗ install ppxlib                      0.28.0  [required by ppx_jane]
  ∗ install variantslib                 v0.15.0 [required by core]
  ∗ install typerep                     v0.15.0 [required by core]
  ∗ install stdio                       v0.15.0 [required by core]
  ∗ install parsexp                     v0.15.0 [required by sexplib]
  ∗ install fieldslib                   v0.15.0 [required by core]
  ∗ install ppx_stable                  v0.15.0 [required by ppx_jane]
  ∗ install ppx_sexp_conv               v0.15.1 [required by core]
  ∗ install ppx_pipebang                v0.15.0 [required by ppx_jane]
  ∗ install ppx_optional                v0.15.0 [required by ppx_jane]
  ∗ install ppx_ignore_instrumentation  v0.15.0 [required by ppx_jane]
  ∗ install ppx_here                    v0.15.0 [required by ppx_jane]
  ∗ install ppx_fixed_literal           v0.15.0 [required by ppx_jane]
  ∗ install ppx_enumerate               v0.15.0 [required by ppx_base]
  ∗ install ppx_disable_unused_warnings v0.15.0 [required by ppx_jane]
  ∗ install ppx_compare                 v0.15.0 [required by ppx_base, bin_prot]
  ∗ install ppx_cold                    v0.15.0 [required by ppx_base]
  ∗ install ppx_variants_conv           v0.15.0 [required by ppx_jane]
  ∗ install ppx_typerep_conv            v0.15.0 [required by ppx_jane]
  ∗ install ppx_optcomp                 v0.15.0 [required by ppx_jane]
  ∗ install sexplib                     v0.15.1 [required by core]
  ∗ install ppx_fields_conv             v0.15.0 [required by ppx_jane]
  ∗ install ppx_custom_printf           v0.15.0 [required by ppx_jane]
  ∗ install ppx_sexp_value              v0.15.0 [required by ppx_jane]
  ∗ install ppx_sexp_message            v0.15.0 [required by core]
  ∗ install ppx_let                     v0.15.0 [required by ppx_jane]
  ∗ install ppx_hash                    v0.15.0 [required by core]
  ∗ install ppx_assert                  v0.15.0 [required by core]
  ∗ install bin_prot                    v0.15.0 [required by core]
  ∗ install ppx_log                     v0.15.0 [required by ppx_jane]
  ∗ install ppx_base                    v0.15.0 [required by core]
  ∗ install jst-config                  v0.15.1 [required by core]
  ∗ install ppx_bin_prot                v0.15.0 [required by ppx_jane]
  ∗ install ppx_string                  v0.15.0 [required by ppx_jane]
  ∗ install time_now                    v0.15.0 [required by core]
  ∗ install ppx_module_timer            v0.15.0 [required by ppx_jane]
  ∗ install ppx_inline_test             v0.15.0 [required by core]
  ∗ install ppx_expect                  v0.15.1 [required by ppx_jane]
  ∗ install ppx_bench                   v0.15.0 [required by ppx_jane]
  ∗ install splittable_random           v0.15.0 [required by core]
  ∗ install base_quickcheck             v0.15.0 [required by core]
  ∗ install ppx_jane                    v0.15.0 [required by core]
  ∗ install int_repr                    v0.15.0 [required by base_bigstring]
  ∗ install base_bigstring              v0.15.0 [required by core]
  ∗ install core                        v0.15.1
===== ∗ 54 =====
Do you want to continue? [Y/n] y

<><> Processing actions <><><><><><><><><><><><><><><><><><><><><><><><><><>  🐫
⬇ retrieved base_bigstring.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved base_quickcheck.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved base.v0.15.1  (https://opam.ocaml.org/cache)
⬇ retrieved bin_prot.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved fieldslib.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved core.v0.15.1  (https://opam.ocaml.org/cache)
⬇ retrieved jane-street-headers.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved int_repr.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved num.1.4  (https://opam.ocaml.org/cache)
⬇ retrieved jst-config.v0.15.1  (https://opam.ocaml.org/cache)
⬇ retrieved ocaml-compiler-libs.v0.12.4  (https://opam.ocaml.org/cache)
∗ installed jane-street-headers.v0.15.0
⬇ retrieved ppx_assert.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved parsexp.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_base.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_bench.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_cold.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_bin_prot.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_compare.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_custom_printf.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_derivers.1.2.1  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_disable_unused_warnings.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_enumerate.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_fields_conv.v0.15.0  (https://opam.ocaml.org/cache)
∗ installed ppx_derivers.1.2.1
⬇ retrieved ppx_expect.v0.15.1  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_fixed_literal.v0.15.0  (https://opam.ocaml.org/cache)
∗ installed num.1.4
∗ installed ocaml-compiler-libs.v0.12.4
⬇ retrieved ppx_hash.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_here.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_ignore_instrumentation.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_jane.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_inline_test.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_let.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_log.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_module_timer.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_optcomp.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_optional.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_pipebang.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_sexp_message.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_sexp_value.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_sexp_conv.v0.15.1  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_string.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_stable.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_typerep_conv.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved ppx_variants_conv.v0.15.0  (https://opam.ocaml.org/cache)
∗ installed seq.base
⬇ retrieved re.1.10.4  (https://opam.ocaml.org/cache)
⬇ retrieved ppxlib.0.28.0  (https://opam.ocaml.org/cache)
⬇ retrieved sexplib.v0.15.1  (https://opam.ocaml.org/cache)
⬇ retrieved sexplib0.v0.15.1  (https://opam.ocaml.org/cache)
⬇ retrieved splittable_random.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved stdio.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved stdlib-shims.0.3.0  (https://opam.ocaml.org/cache)
⬇ retrieved time_now.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved typerep.v0.15.0  (https://opam.ocaml.org/cache)
⬇ retrieved variantslib.v0.15.0  (https://opam.ocaml.org/cache)
∗ installed stdlib-shims.0.3.0
∗ installed sexplib0.v0.15.1
∗ installed re.1.10.4
∗ installed base.v0.15.1
∗ installed fieldslib.v0.15.0
∗ installed variantslib.v0.15.0
∗ installed stdio.v0.15.0
∗ installed typerep.v0.15.0
∗ installed parsexp.v0.15.0
∗ installed sexplib.v0.15.1
∗ installed ppxlib.0.28.0
∗ installed ppx_cold.v0.15.0
∗ installed ppx_disable_unused_warnings.v0.15.0
∗ installed ppx_here.v0.15.0
∗ installed ppx_ignore_instrumentation.v0.15.0
∗ installed ppx_optcomp.v0.15.0
∗ installed ppx_fields_conv.v0.15.0
∗ installed ppx_enumerate.v0.15.0
∗ installed ppx_pipebang.v0.15.0
∗ installed ppx_optional.v0.15.0
∗ installed ppx_fixed_literal.v0.15.0
∗ installed ppx_compare.v0.15.0
∗ installed ppx_typerep_conv.v0.15.0
∗ installed ppx_stable.v0.15.0
∗ installed ppx_let.v0.15.0
∗ installed ppx_variants_conv.v0.15.0
∗ installed ppx_sexp_conv.v0.15.1
∗ installed ppx_assert.v0.15.0
∗ installed ppx_sexp_value.v0.15.0
∗ installed ppx_sexp_message.v0.15.0
∗ installed ppx_hash.v0.15.0
∗ installed ppx_custom_printf.v0.15.0
∗ installed ppx_base.v0.15.0
∗ installed ppx_log.v0.15.0
∗ installed ppx_string.v0.15.0
∗ installed jst-config.v0.15.1
∗ installed bin_prot.v0.15.0
∗ installed time_now.v0.15.0
∗ installed ppx_bin_prot.v0.15.0
∗ installed ppx_inline_test.v0.15.0
∗ installed ppx_module_timer.v0.15.0
∗ installed ppx_bench.v0.15.0
∗ installed ppx_expect.v0.15.1
∗ installed splittable_random.v0.15.0
∗ installed base_quickcheck.v0.15.0
∗ installed ppx_jane.v0.15.0
∗ installed int_repr.v0.15.0
∗ installed base_bigstring.v0.15.0
∗ installed core.v0.15.1
Done.
```

If you try `open Core` in `utop` now, it'll work.

## Fixes and observations

I noticed something peculiar with one of the examples where the type inference engine looks to misbehave if `Core` is important. Take the following:

```ocaml
let rec destutter list =
  match list with
  | [] -> []
  | [hd] -> [hd]
  | hd1 :: hd2 :: tl ->
    if hd1 = hd2 then destutter (hd2 :: tl) else hd1 :: destutter (hd2 :: tl);;
```
If you import `Core` or `Base` into the REPL's namespace, you'll get this signature:

```ocaml
val destutter : int list -> int list = <fun>
```

Which is plainly incorrect, but if you don't, you'll get this signature, which is the expected one:

```ocaml
val destutter : 'a list -> 'a list = <fun>
```

If you look at the `remove_sequential_duplicates` function defined in the second edition, which is its equivalent of `destutter`, had the `int list` type rather than `'a list`, but gives no explanation as to why. My assumption is that `Base`/`Core` redefines the `=` operator in some way that forces a concrete type rather than a [type variable](https://en.wikipedia.org/wiki/Type_variable). This is unfortunate as it means the function is no longer polymorphic. That's just an educated guess, but it seems like a good reason not to pollute your namespace.

The `log_entry` function has some surprises too:

```ocaml
let log_entry maybe_time message =
  let time =
    match maybe_time with
    | Some x -> x
    | None -> Core.Time.now ()
  in
    Core.Time.to_sec_string time ^ " -- " ^ message;;
```

Gives the error:

``` { use_pygments=false }
Error: This expression has type zone:Core.Time.Zone.t -> string
       but an expression was expected of type string
```

That's fine, however on my machine, if I try to use the local timezone by changing `Core.Time.to_sec_string time` to `Core.Time.to_sec_string time ~zone:Core.Time.Zone.local`, I get:

``` { use_pygments=false }
Error: This expression has type [ `Use_Time_unix ]
but an expression was expected of type Time.Zone.t
```

That's all rather mysterious, but I took at look at its type:

``` { use_pygments=false }
utop # Core.Time.Zone.local;;
Line 1, characters 0-15:
Alert deprecated: Core.Time.Zone.local
[since 2021-03] Use [Time_unix]
Line 1, characters 0-15:
Alert deprecated: Core.Time.Zone.local
[since 2021-03] Use [Time_unix]
- : [ `Use_Time_unix ] = `Use_Time_unix
```

My assumption is that this refers to the [unix-time](https://opam.ocaml.org/packages/unix-time/) package, but I can't say it communicates this particularly well.

`Core.Time.Zone.utc` (the one true timezone) is an option though, and that works just fine:

```
utop # let log_entry maybe_time message =
  let time =
    match maybe_time with
    | Some x -> x
    | None -> Time.now ()
  in
    (Core.Time.to_sec_string time ~zone:Core.Time.Zone.utc) ^ " -- " ^ message;;
val log_entry : Time.t option -> string -> string = <fun>
```

And people complain about when changes are made in Python!

The `corebuild` script mentioned in the book doesn't appear to exist anymore, and it seems from the second edition that they're pushing the [dune build system](https://dune.build/). I don't want bother with that just yet, though utop pulls it in as a dependency, so I'll try to stick with `ocamlbuild` for now.

There's the sample program given in the chapter updated slightly:

```ocaml
open Core

let rec read_and_accumulate accum =
  let line = In_channel.input_line In_channel.stdin in
  match line with
  | None -> accum
  | Some x -> read_and_accumulate (accum +. Float.of_string x)

let () =
  printf "Total %F\n" (read_and_accumulate 0.)
```

We'll save this as `sum.ml`, and build it:

```console
$ ocamlbuild -pkgs core sum.native
Finished, 4 targets (0 cached) in 00:00:02.
```

`ocamlbuild` is a bit odd: it uses a naming convention to determine whether the build something as native code or bytecode. Thus if you have a module called `sum.ml`, if you want to build it as native code, you use `sum.native` as the target, which will produce a file called `sum.native`. As we want to link to the `core` package so that we have access to the `Core` module, we include the flag `-pkgs core`. Now, let's run it:

```console
$ ./sum.native
4
5
5
2
^D
Total 16.
```

Seems to work!

## Upgrading installed packages

If you've upgraded OCaml, you'll likely need to upgrade any installed packages. Normally, to update everything, you run:

```console
$ opam update
$ opam upgrade
```

After an upgrade of OCaml itself, the second command will give you a message like the following:

```console
[WARNING] File /usr/bin/ocamlc, which package ocaml-system.4.05.0 depends upon, was changed on your system.
          The package will need to be reinstalled.
[WARNING] Upgrade is not possible because of conflicts or packages that are no longer available:
    - Incompatible packages:
    - (invariant) → ocaml-system
    - base-num → ocaml < 4.06.0 → ocaml-base-compiler = 3.08.1
    You can temporarily relax the switch invariant with `--update-invariant'
  - Missing dependency:
    - base-num → ocaml < 4.06.0 → ocaml-variants → ocaml-beta
    unmet availability conditions: 'enable-ocaml-beta-repository'

You may run "opam upgrade --fixup" to let opam fix the current state.
```

In this case, you can run:

```console
$ opam upgrade --fixup
```

## Addendum

I double-checked my suspicion regarding `=`:

``` { use_pygments=false }
utop # (=);;
- : int -> int -> bool = <fun>
```

It appears I was correct. Interestingly, this is not [the signature reported in the documentation for Core](https://ocaml.org/p/core/v0.15.0/doc/Core/index.html#comparisons), but it does correspond to [the signature reported for Base](https://ocaml.org/p/base/v0.15.0/doc/Base/index.html#val-(=)). To restore this, you need to use [Base.Poly](https://ocaml.org/p/base/v0.15.0/doc/Base/Poly/index.html). I'm sure there's some kind of rationale for this.
