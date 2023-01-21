Title: Notes from Real World OCaml, chapter 7, part 1
Slug: rwocaml-4
Category: Coding
Date: 2023-01-21 19:23
Series: Real World OCaml
Status: published

In `compute_bounds`, `cmp` should be replaced with `compare`:

```ocaml
let compute_bounds ~compare list =
  let sorted = List.sort ~compare list in
  match List.hd sorted, List.last sorted with
  | None, _ | _, None -> None
  | Some x, Some y -> Some (x, y)
```

The resulting type signature will be the same as in the book.

Typing `find_mismatches` into `utop` gave a very odd type signature after spinning for a while.

```ocaml
val find_mismatches :
  ('a, int) Timezone.Table.hashtbl ->
  ('a, int) Timezone.Table.hashtbl -> 'a list = <fun>
```

Here's the function rewritten not to depend on Core:

```ocaml
let find_mismatches table1 table2 =
  let f key data mismatches =
    match Hashtbl.find_opt table2 key with
    | Some data' when data' <> data -> key :: mismatches
    | _ -> mismatches
  in Hashtbl.fold f table1 [];;
```

Which gives a more resaonable signature:

```ocaml
val find_mismatches :
  ('a, 'b) Hashtbl.t -> ('a, 'b) Hashtbl.t -> 'a list = <fun>
```

On the off-chance that the issue was down to the contents of my `~/.opam` directory, nuked it and reinstalled it:

```console
$ rm -rf ~/.opam
$ opam init
$ opam install core utop
```

This gave a better result:

``` { use_pygments=false }
utop # open Core;;
utop # let find_mismatches table1 table2 =
  Hashtbl.fold table1 ~init:[] ~f:(fun ~key ~data mismatches ->
    match Hashtbl.find table2 key with
    | Some data' when data' <> data -> key :: mismatches
    | _ -> mismatches
  );;
val find_mismatches :
  ('a, int) Core.Hashtbl.t -> ('a, int) Core.Hashtbl.t -> 'a list = <fun>
```

Notice, however, that this means the value _must_ be an `int`. As before, you must do `open Base.Poly` to fix this before defining the function to make the comparison polymorphic again:

```ocaml
val find_mismatches :
  ('a, 'b) Core.Hashtbl.t -> ('a, 'b) Core.Hashtbl.t -> 'a list = <fun>
```

As to why this was happening, I'm more sure, but if you see this, you may need to do something similar.

## S-expressions

The example using `Core.Time.sexp_of_t` no longer works: this function is deprecated:

``` { use_pygments=false }
utop # Time.sexp_of_t;;
Line 1, characters 0-14:
Alert deprecated: Core.Time.sexp_of_t
[since 2021-03] Use [Time_unix]
Line 1, characters 0-14:
Alert deprecated: Core.Time.sexp_of_t
[since 2021-03] Use [Time_unix]
- : [ `Use_Time_unix ] = `Use_Time_unix
```

Unfortunately, `Time_unix` provided by [unix-time](https://github.com/dsheets/ocaml-unix-time) doesn't have this functionality. [core_unix](https://ocaml.org/p/core_unix/v0.15.2) [does have this functionality](https://ocaml.org/p/core_unix/v0.15.2/doc/Time_unix/). Once you have that installed, try the following:

``` { use_pygments=false }
utop # #require "core_unix.time_unix";;
utop # Time_unix.sexp_of_t;;
Time_unix.t -> Sexplib0.Sexp.t = <fun>
utop # Error.create "Something failed a long time ago" Time.epoch Time_unix.sexp_of_t;;
- : Error.t =
("Something failed a long time ago" (1970-01-01 01:00:00.000000+01:00))
```

The `<:sexp_of<...>>` extended syntax no longer seems to work. You instead need to use `ppx_jane` for this and the `[%sexp ...]` syntax. For instance:

```ocaml
let custom_to_sexp = <:sexp_of<float * string list * int>>
```

Becomes:

``` { use_pygments=false }
utop # #require "ppx_jane";;
utop # [%sexp (3.5, ["a"; "b"; "c"], 6034)];;
- : Sexp.t = (3.5 (a b c) 6034)
utop # Error.create "Something went wrong" [%sexp (3.5, ["a"; "b"; "c"], 6034)] Fn.id;;
- : Error.t = ("Something went wrong" (3.5 (a b c) 6034))
```

`Fn.id` is the function `fun x -> x`: `Error.create` takes a third argument that can manipulate the second argument passed in. This would also work, and would typecheck the second argument:

``` { use_pygments=false }
utop # Error.create "Something went wrong" (3.5, ["a"; "b"; "c"], 6034) [%sexp_of: (float * string list * int)];;
- : Error.t = ("Something went wrong" (3.5 (a b c) 6034))
```

## "bind and Other Error Handling Idioms"

Congratulations! You're being introduced to monads! Specifically, this is the [Maybe monad]. Here's a modified version of the function with the expected labels:

[Maybe monad]: https://en.wikipedia.org/wiki/Monad_(functional_programming)#An_example:_Maybe

```ocaml
let compute_bounds_monadic ~compare list =
  let sorted = List.sort ~compare list in
  Option.bind (List.hd sorted) ~f:(fun first ->
    Option.bind (List.last sorted) ~f:(fun last ->
      Some (first, last)))
```

## "Deriving exceptions using sexp"

Rather than:

```ocaml
exception Wrong_date of Date.t with sexp
```

Use an annotation:

```ocaml
exception Wrong_date of Date.t [@@deriving sexp]
```

## "Cleaning Up in the Presence of Exceptions"

`load_reminders` becomes:

```ocaml
let load_reminders filename =
  let inc = In_channel.create filename in
  let reminders = [%of_sexp: ((Time_unix.t * string) list)] (Sexp.input_sexp inc) in
  In_channel.close inc;
  reminders;;
```

Note that you'll need require the `ppx_jane` library for `%of_sexp`, `core_unix.time_unix` for `Time_unix`.
