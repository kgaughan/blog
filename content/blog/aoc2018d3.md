Title: Advent of Code 2018, Day 3
Date: 2018-12-30 23:30
Category: Advent of Code
Status: published

## Part 1

There's some parsing needed on the input file, and because there doesn't seem much point in writing the parsing code myself, I used the [text_io](https://crates.io/crates/text_io) crate.

Also, I needed some representation of the rectangles, so I wrote a simple implementation with some tests for a method to check if one overlaps with another.

In my first attempt, I misread what was requested, and ended up summing the areas of any intersections. This is wrong, because that's actually needed is the total area of the interestions, which is a _much_ smaller amount, and a more difficult problem.

Researching for an algorithm, I basically [found the solution](http://codercareer.blogspot.com/2011/12/no-27-area-of-rectangles.html).

However, out of laziness and to stop myself from faffing about, I decided to just bruteforce the solution by plotting everything into an array of array.

Rust's syntax for declaring this is interesting:

```rust
let mut sheet: [[u8; 1000]; 1000] = [[0; 1000]; 1000];
```

That declares an array of arrays of bytes, each of which is 1000 elements in size. The literal on the right hand size declares an array of that type where each element of the byte arrays is `0`, thus you end up with a 1000x1000 array of bytes, fully zeroed out.

Before starting on part 2, I factored apart the plotting and counting code. For this, I had to use the above declaration in the signature. I'm guessing there are better ways of doing this, likely using slices, but in this case hardwiring the size is just fine.

## Part 2

Nothing particularly special here: checking for no overlap is pretty similar to plotting the rectangles, except you're checking if any of the plotted points have a value of `2` (meaning there's a previously-plotted overlap), in which case the rectangle being checked is rejected.

## Solutions

For the source code, see [here](https://github.com/kgaughan/adventofcode2018/tree/master/day03).
