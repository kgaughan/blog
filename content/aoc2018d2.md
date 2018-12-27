Title: Advent of Code 2018, Day 2
Date: 2018-12-26 13:18
Category: Advent of Code
Status: published

## Part 1

This one has us applying a simple algorithm to a list of strings to extract some characteristics of a string - specificially, whether a given string contains exactly two or three of any letter - then summing up how many each of these characteristics applies to the strings, and multiplying the result for the final checksum.

The function I created to analyse the box IDs returns a struct with two booleans. For the test to run, I needed two things: for it to derive the [`PartialEq`](https://doc.rust-lang.org/core/cmp/trait.PartialEq.html) and [`Debug`](https://doc.rust-lang.org/core/fmt/trait.Debug.html) traits. How this all works is a bit magical, and I assume that both use reflection by default to find all the information they need to compare for equality and format the struct. Both are required for the test as I'm using [`assert_eq!`](https://doc.rust-lang.org/core/macro.assert_eq.html), and the former is needed for the equality check while the latter is needed to print out the values if the assertion fails.

I wrote an intentionally failing test to make sure any test code worked, and then started working on implementing `analyse_box_id` properly. Here's what I wrote, because I think it's worth picking apart:

```rust
let mut character_counts: HashMap<char, i32> = HashMap::new();

for ch in s.chars() {
    let counter = character_counts.entry(ch).or_insert(0);
    *counter += 1
}
```

The [`entry`](https://doc.rust-lang.org/std/collections/struct.HashMap.html#method.entry) and [`or_insert`](https://doc.rust-lang.org/std/collections/hash_map/enum.Entry.html#method.or_insert) methods were are interesting. The former does a lookup on the `HashMap` to return one of two variants on the [`Entry`](https://doc.rust-lang.org/std/collections/hash_map/enum.Entry.html) type, depending on whether the given slot in the map is vacant or occupied. Using `or_insert` on the resulting type will insert a value if this type is `VacantEntry`. As I'm inserting `0`, I could equally have used [`or_default`](https://doc.rust-lang.org/std/collections/hash_map/enum.Entry.html#method.or_default), which would insert the default value for the value type, which for an `i32` would be `0`.

`or_insert` and company return a mutable reference to the value in the entry, so we need to use the `*` operator to [dereference this](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html) to increment it.

Once the analysis is done, we can check if there are any characters that occur twice or three times. When I was doing that, I hit a surprise:

```rust
for n in character_counts.values() {
    if n == 2 {
        result.has_two = true
    } else if n == 3 {
        result.has_three = true
    }
}
```

It hadn't occurred to me that [`values`](https://doc.rust-lang.org/std/collections/struct.HashMap.html?search=#method.values) would return an iterator of references to the integers, so doing `n == 2` failed with the message _no implementation for `&i32 == {integer}`_. This was easily solved by replacing `n` with `*n` to dereference the reference.

With that fix applied and the test fixed so it passes, we can move on to the box ID checksum.

A quick aside on the signature of `analyse_box_id`:

```rust
fn analyse_box_id(s: &str) -> Characteristics {
    ...
}
```

Notice the use of `&`? This is because Rust does [pass by value](https://en.wikipedia.org/wiki/Evaluation_strategy#Call_by_value). A string can be an arbitrary size, so the compiler will complain if you try to pass one as it needs to know beforehand the size of the stack frame to allocate. A reference to any object is a fixed size, so the compiler will happily accept this instead.

The same goes for [`Vec`](https://doc.rust-lang.org/std/vec/struct.Vec.html), which is a contiguous growable array values. Because it's a contiguous array, the values have to be fixed size, and thus you can't have a `Vec<str>`, but need to use `Vec<&str>` instead. Hence the signature of my `checksum_box_ids` function:

```rust
fn checksum_box_ids(ids: Vec<&str>) -> i32 {
    ...
}
```

`checksum_box_ids` is a trivial function, so all that's needed at this point is to implement a driver to parse the file into lines and pass the result to `checksum_box_ids`.

The driver raised an interesting issue:

```rust
let mut values: vec::Vec<&str> = vec![];
for line in reader.lines() {
    values.push(line?.trim_end());
}
```

This code looks fine, but the compiler complains that the temporary value returned by, I assume, `trim_end`, goes out of scope:

```text
error[E0716]: temporary value dropped while borrowed
  --> src/main.rs:14:21
   |
14 |         values.push(line?.trim_end());
   |         ------      ^^^^^            - temporary value is freed at the end of this statement
   |         |           |
   |         |           creates a temporary which is freed while still in use
   |         borrow used here, in later iteration of loop
   |
   = note: consider using a `let` binding to create a longer lived value
```

That's a bit weird, as you'd expect the compiler to automatically lift the value from the stack to the heap. Tried a slightly different tack, with the same result:

```rust
let values = reader.lines().map(|line| {
    line.unwrap_or_default().trim_end()
}).collect();
```

Adding [`to_owned`](https://doc.rust-lang.org/std/borrow/trait.ToOwned.html#tymethod.to_owned) almost does the trick, but that gives a type error later:

```text
error[E0277]: a collection of type `std::vec::Vec<&str>` cannot be built from an iterator over elements of type `std::string::String`
  --> src/main.rs:13:8
   |
13 |     }).collect();
   |        ^^^^^^^ a collection of type `std::vec::Vec<&str>` cannot be built from `std::iter::Iterator<Item=std::string::String>`
   |
   = help: the trait `std::iter::FromIterator<std::string::String>` is not implemented for `std::vec::Vec<&str>`
```

I did what feels like a cheat, but is probably the right way to do thingscheated a bit, and changed `checksum_box_ids` to this:

```rust
fn checksum_box_ids(ids: Vec<String>) -> i32 {
    ...
    for id in ids {
        let characteristics = analyse_box_id(&id);
        ...
    }
    ...
}
```

That necessitated some gross calls to [`to_string`](https://doc.rust-lang.org/std/primitive.str.html#method.to_string) in the tests.

## Part 2

There's probably a smarter way of doing this, but I chose to do a brute force search, comparing each entry to any subsequent entries until I found a match.

## Solutions

For the source code, see [here](https://github.com/kgaughan/adventofcode2018/tree/master/day02).
