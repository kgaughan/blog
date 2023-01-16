Title: Notes from Real World OCaml, chapters 4, 5, and 6
Slug: rwocaml-3
Category: Coding
Date: 2023-01-16 17:03
Series: Real World OCaml
Status: published

## Chapter 4

Chapter 4 mostly works, but you need to replace `open Core.Std` with `open Core`, and include `open Base.Poly` _after_ `open Core` in `session_info.ml`. This latter change restores the polymorphic equality operators. My updated code from it at the end of the chapter is [here](https://github.com/kgaughan/learning/tree/master/0015-real-world-ocaml/ch04).

## Chapter 5

Instead of using `Core_extended`, which appears to be a mere shadow of itself, you should install the [`shell`](https://ocaml.org/p/shell/v0.14.0/doc/Shell/) package. This appears to be the `Shell` module from `Core_extended` broken out to its own package. Thus, in `utop`, instead of:

``` { use_pygments=false }
utop # #require "core_extended";;
utop # open Core_extended.Std;;
```

Run this instead:

``` { use_pygments=false }
utop # #require "shell";;
utop # open Core;;
```

For the example, here's the code:

```ocaml
type host_info = {
  hostname : string;
  os_name : string;
  cpu_arch : string;
  timestamp : Core.Time.t;
}

let my_host =
  let sh = Shell.sh_first_line_exn in {
    hostname = sh "hostname";
    os_name = sh "uname -s";
    cpu_arch = sh "uname -p";
    timestamp = Core.Time.now ();
  }
```

Notice how I've substituted `sh_first_line_exn` for `sh_one_exn`? The latter is deprecated, but the former has the same behaviour but is not deprecated.

For `host_info_to_string`, you'll need to do `open Printf` to include `sprintf` in the REPL's namespace.

For the `get_users` function, it tells you to add `with fields` at the end of the `Login module`. This no longer works. Instead, you need the [`ppx_jane`](https://opam.ocaml.org/packages/ppx_jane/) package, which appears to have superceded `fieldslib` for this purpose, and rather than the `with fields`, you put the annotation `[@@deriving fields]` after the type. `ppx_janne` should already be installed as a dependency previously. Recember that if you want its contents available within `utop`, you'll need to run `#require "ppx_jane"`. If you don't, the annotation won't result in any code being generated.

## Chapter 6

This worked without issue.
