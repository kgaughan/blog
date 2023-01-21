Title: Notes from Real World OCaml, chapter 7, part 2
Slug: rwocaml-5
Category: Coding
Date: 2023-01-21 21:45
Series: Real World OCaml
Status: published

This finishes up [my earlier post on chapter 7]({filename}rwocaml-4.md). I was feeling a bit tired at the time, so needed a break.

## Cleaning up in the presence of errors

Typing in:

```ocaml
let lookup_weight ~compute_weight alist key =
  try
    let data = List.Assoc.find_exn alist key in
    compute_weight data
  with Not_found -> 0.
```

Gives the signature:

```ocaml
val lookup_weight :
  compute_weight:((equal:('a -> 'a -> bool) -> 'b) -> float) ->
  ('a, 'b) Base.List.Assoc.t -> 'a -> float = <fun>
```

And the following error when executed:

``` { use_pygments=false }
Error: This expression has type int -> float
       but an expression was expected of type
         (equal:('a -> 'a -> bool) -> 'b) -> float
       Type int is not compatible with type equal:('a -> 'a -> bool) -> 'b
```

They key bit is `Type int is not compatible with type equal:('a -> 'a -> bool) -> 'b`: that's an indication that [there's a named parameter, `equal`, that we need to specify](https://v3.ocaml.org/p/core/v0.15.1/doc/Core/List/Assoc/index.html#val-find_exn). The signature `'a -> 'a -> bool` implies it takes two values of the same type an returns a boolean, so let's try this instead:

```ocaml
let lookup_weight ~compute_weight alist key =
  try
    let data = List.Assoc.find_exn ~equal:(=) alist key in
    compute_weight data
  with Not_found -> 0.
```

The signature is much more reasonable:

```ocaml
val lookup_weight :
  compute_weight:('a -> float) -> ('b, 'a) Base.List.Assoc.t -> 'b -> float =
  <fun>
```

``` { use_pygments=false }
utop # lookup_weight ~compute_weight:Float.of_int [("a", 3); ("b", 4)] "a";;
- : float = 3.
utop # lookup_weight ~compute_weight:Float.of_int [("a", 3); ("b", 4)] "b";;
- : float = 4.
utop # lookup_weight ~compute_weight:Float.of_int [("a", 3); ("b", 4)] "c";;
Exception: (Not_found_s "List.Assoc.find_exn: not found").
Raised at Base__List.Assoc.find_exn.find_exn in file "src/list.ml", line 1068, characters 16-31
Called from unknown location
Called from Stdlib__Fun.protect in file "fun.ml", line 33, characters 8-15
Re-raised at Stdlib__Fun.protect in file "fun.ml", line 38, characters 6-52
Called from Topeval.load_lambda in file "toplevel/byte/topeval.ml", line 89, characters 4-150
```

## Backtraces

Be sure the run the following:

```console
$ opam install core_bench core_unix
```

Here's a corrected version of the benchmark program:

```ocaml
open Core
open Core_bench

let simple_computation () =
  List.range 0 10
  |> List.fold ~init:0 ~f:(fun sum x -> sum + x * x)
  |> ignore

let simple_with_handler () =
  try
    simple_computation ()
  with Exit -> ()

let end_with_exc () =
  try
    simple_computation ();
    raise Exit
  with Exit -> ()

let () =
  [
    Bench.Test.create ~name:"simple computation" simple_computation;
    Bench.Test.create ~name:"simple computation w/ handler" simple_with_handler;
    Bench.Test.create ~name:"end with exn" end_with_exc
  ]
  |> Bench.make_command
  |> Command_unix.run
```

It's quite similar to the one in the book with the one _real_ difference being that `Command.run` is replaced iwth `Command_unix.run`. I also got rid of the pointless wrapper functions.

Assuming you've called the file `backtrace.ml`, build it with:

```console
$ ocamlbuild -use-ocamlfind -pkg core,core_bench,core_unix.command_unix -tag thread backtrace.native
Finished, 4 targets (0 cached) in 00:00:01.
```

Notice the use of [`core_unix.command_unix`](https://ocaml.org/p/core_unix/v0.14.0/doc/Command_unix/): this is a library within the `core_unix` package, so needs to be qualified. `-tag thread` is needed to prevent the following error:

``` { use_pygments=false }
+ ocamlfind ocamlc -c -package core,core_bench,core_unix.command_unix -o backtrace.cmo backtrace.ml
ocamlfind: [WARNING] Package `threads': Linking problems may arise because of the missing -thread or -vmthread switch
+ ocamlfind ocamlopt -c -package core,core_bench,core_unix.command_unix -o backtrace.cmx backtrace.ml
ocamlfind: [WARNING] Package `threads': Linking problems may arise because of the missing -thread or -vmthread switch
+ ocamlfind ocamlopt -linkpkg -package core,core_bench,core_unix.command_unix backtrace.cmx -o backtrace.native
ocamlfind: [WARNING] Package `threads': Linking problems may arise because of the missing -thread or -vmthread switch
File "_none_", line 1:
Error: No implementations provided for the following modules:
         Thread referenced from ~/.opam/default/lib/core_unix/core_thread/core_thread.cmxa(Core_thread)
         Mutex referenced from ~/.opam/default/lib/core_unix/error_checking_mutex/error_checking_mutex.cmxa(Error_checking_mutex)
         Condition referenced from ~/.opam/default/lib/core_unix/error_checking_mutex/error_checking_mutex.cmxa(Error_checking_mutex)
         Event referenced from ~/.opam/default/lib/core_unix/core_thread/core_thread.cmxa(Core_thread)
Command exited with code 2.
Hint: Recursive traversal of subdirectories was not enabled for this build,
  as the working directory does not look like an ocamlbuild project (no
  '_tags' or 'myocamlbuild.ml' file). If you have modules in subdirectories,
  you should add the option "-r" or create an empty '_tags' file.

  To enable recursive traversal for some subdirectories only, you can use the
  following '_tags' file:

      true: -traverse
      <dir1> or <dir2>: traverse
```

And run:

```console
$ _build/backtrace.native 
Estimated testing time 30s (3 benchmarks x 10s). Change using '-quota'.
┌───────────────────────────────┬──────────┬─────────┬────────────┐
│ Name                          │ Time/Run │ mWd/Run │ Percentage │
├───────────────────────────────┼──────────┼─────────┼────────────┤
│ simple computation            │ 150.45ns │  84.00w │     92.79% │
│ simple computation w/ handler │ 152.38ns │  84.00w │     93.98% │
│ end with exn                  │ 162.14ns │  84.00w │    100.00% │
└───────────────────────────────┴──────────┴─────────┴────────────┘
```

The exception overhead seems to be reduced from that given in the book. With backtraces disabled, it's reduced to jitter:

```console
$ OCAMLRUNPARAM= _build/backtrace.native
Estimated testing time 30s (3 benchmarks x 10s). Change using '-quota'.
┌───────────────────────────────┬──────────┬─────────┬────────────┐
│ Name                          │ Time/Run │ mWd/Run │ Percentage │
├───────────────────────────────┼──────────┼─────────┼────────────┤
│ simple computation            │ 150.34ns │  84.00w │     98.05% │
│ simple computation w/ handler │ 153.33ns │  84.00w │    100.00% │
│ end with exn                  │ 152.86ns │  84.00w │     99.70% │
└───────────────────────────────┴──────────┴─────────┴────────────┘
```
