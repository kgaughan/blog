Title: Notes from Real World OCaml, chapter 3
Slug: rwocaml-2
Category: Coding
Date: 2023-01-15 13:43
Series: Real World OCaml
Status: published

I didn't notice any issues with chapter 2, but in chapter 3, it expects [_core_bench_](https://opam.ocaml.org/packages/core_bench/) to be installed. Similarly to `Core`, you'll want to replace mentions of `Core_bench.Std` with simply `Core_bench`.

`Bench.bench` has changed considerably and requires less boilerplate, meaning that you can ditch `run_bench` and use `Bench.bench` directly.

``` { use_pygments=false }
utop # Bench.bench [
  Bench.Test.create ~name:"plus_one_match" (fun() -> ignore (plus_one_match 10));
  Bench.Test.create ~name:"plus_one_if" (fun() -> ignore (plus_one_if 10))
];;
Estimated testing time 20s (2 benchmarks x 10s). Change using '-quota'.
┌────────────────┬──────────┐
│ Name           │ Time/Run │
├────────────────┼──────────┤
│ plus_one_match │  21.22ns │
│ plus_one_if    │  58.94ns │
└────────────────┴──────────┘
- : unit = ()
```

It looks like the speed advantage of pattern matching has increased even more since the first edition.

Out of curiosity, I wrote a version of the `sum` function using `Core.List.fold`, as it's the way I'd write something like that in real life rather than manually munging things with pattern matching:

```ocaml
let sum = List.fold ~init:0 ~f:(+)
```

This benched worse than I'd expected, but I'm guessing this is down to the bytecode interpreter not eliminating a bunch of function calls:

``` { use_pygments=false }
utop # let numbers = List.range 0 1000 in
  Bench.bench [
    Bench.Test.create ~name:"sum_if" (fun () -> ignore (sum_if numbers));
    Bench.Test.create ~name:"sum" (fun () -> ignore (sum numbers))
  ];;
Estimated testing time 20s (2 benchmarks x 10s). Change using '-quota'.
┌────────┬──────────┐
│ Name   │ Time/Run │
├────────┼──────────┤
│ sum_if │  40.25us │
│ sum    │  20.03us │
└────────┴──────────┘
- : unit = ()
```

`List.fold` is only clocking in at twice as fast as using conditionals. I'd expect `List.iter` would be on par if not faster than `List.fold`, but then you're essentially writing imperative code.
