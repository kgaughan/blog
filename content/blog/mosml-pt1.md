Title: Messing with Standard ML and Moscow ML, part one: The core language
Date: 2008-03-18 13:27
Slug: mosml-pt1
Category: Coding
Status: published

!!! note
    A cache of the original post is [here](https://web.archive.org/web/20080829001200/http://talideon.com/weblog/2008/03/mosml-pt1.cfm).

I was playing with [Moscow ML](http://www.itu.dk/~sestoft/mosml.html) because I've wanted to give [Standard ML](http://en.wikipedia.org/wiki/Standard_ML) a bash for a while now, but I could never get [SML/NJ](http://www.smlnj.org/) to play nice for me back when I tried it first on Windows. That, and there was no documentation download.

So why Moscow ML and not SML/NJ, or [Mlton](http://mlton.org/), or one of the other proper Standard ML compilers? Well, even though Moscow ML is getting on a bit and uses bytecode compilation rather than native compilation, it's simple to use, is well-documented, and, unlike Mlton, doesn't require FreeBSD 7.0 and much as I'd like to, I haven't upgraded yet.

It also helps that I'd already fetched it down ages ago, so the source was already in my distfiles folder. 😀

It was dead easy to get something compiled and running. Here's the "Hello, World" program:

```sml
(* helloworld.sml *)
val _ =
  print "Hello, world!\n";
```

`(*` and `*)` mark the beginning and end of comment blocks. They can be nested, so...

```sml
(* This (* is completely legal and *) makes commenting out code easy. *)
```

I made a really dumb mistake the first time I tried this. I'd been playing with the mosml console and forgot that in actual programs the results of expressions need to be assigned somewhere. So, my first program was like this:

```sml
(* brokenhello.sml *)
print "Hello, world!\n";
```

Which got me this:

```
% mosmlc -standalone -o hello brokenhello.sml
File "brokenhello.sml", line 2, characters 0-5:
! print "Hello, world!";
! ^^^^^
! Syntax error.
```

When I saw this, I stared at the screen trying to remember what I'd missed. I felt like a right dolt when I remembered.

I then rewrote the program to use the _[TextIO](http://mosml.org/mosmllib/TextIO.html)_ module:

```sml
(* helloworld-mod.sml *)
val _ =
  TextIO.output (TextIO.stdOut, "Hello, world!\n");
```

This showed that I could access modules just fine.

You're probably wondering what `val _???_ =` means. That's declaration that the value of such-and-such a variable (given by _???_) has the value of the expression that follows. In this case, the wildcard variable `_` is being bound to the result of evaluating the "Hello, World" program.

Next I tried something a little more substantial: factorials.

```sml
(* fac1.sml *)
fun fac n = if n = 0 then 1 else n * fac (n - 1);

val _ = print (Int.toString (fac 5) ^ "\n");
```

Which wrote out _120_, just as I'd expected. As you might guess, Standard ML's if-expressions are just like a more readable version of C's trinary operator.

A quick word on functions. Standard ML functions really only take one argument. To be able to take more than one, you need to either pass everything in an n-[tuple](http://en.wikipedia.org/wiki/Tuple) or use curried function, though naturally because tuples are just another kind of value, you can mix and match both methods. The _[TextIO.output](http://mosml.org/mosmllib/TextIO.html#output-val)_ function above is an example of using a tuple to supply multiple arguments.

A [curried functions](http://en.wikipedia.org/wiki/Currying) is one that use individual one-argument functions to consume each argument. Curried functions are useful in that they allow one to partially apply functions and apply them in interesting ways. For instance, what if we wrapped _TextIO.output_ as follows:

```sml
fun sayToStream str s = TextIO.output (str, s);
```

Here we've a two-argument curried function called _sayToStream_, that take a stream, _str_, and a string to output, _s_. Evaluating this function in the mosml [REPL](http://en.wikipedia.org/wiki/REPL) says the function has this type:

```sml
val sayToStream = fn : outstream -> string -> unit
```

The arrow (`->`) can be thought of as meaning ‘evaluates to', so _sayToStream_ is a function that takes an `outstream` and evaluates to a function that takes a `string`, which evaluates to `unit`, Standard ML's rough equivalent of `void` in C-derived lanuages, but here, `unit` equates to a proper value rather than some notional one. You see, our above declaration of _sayToStream_ is just a shorter, less noisy, way of saying:

```sml
val sayToStream = fn str => fn s => TextIO.output (str, s);
```

Where `fn _arg_ => _expr_` defines a [lambda function](http://en.wikipedia.org/wiki/Lambda_calculus) evaluating to _expr_. `fn` is pronounced ‘lambda', I'm told, which would make sense if they'd used something that at least looked vaguely like a lambda such as a backslash like [Haskell](http://www.haskell.org/) uses, but there you go.

We can partially evaluate _sayToStream_ to create a function that writes its argument to standard output. Here's what we'd get typing at the mosml REPL (`-` is the prompt, by the way, and `>` precedes the result of the preceding expression):

```sml
- val sayToStdOut = sayToStream TextIO.stdOut;
> val sayToStdOut = fn : string -> unit
```

So now we have _sayToStdOut_, a function that does just what we wanted. It's pretty much equivalent to the toplevel `print` function.

Where this becomes really useful is when you want to pass the partially applied function to, say, a mapping function, or if you want to compose it with other functions. Here's an example of the former, writing out the contents of a string array:

```sml
- List.map (sayToStream TextIO.stdOut) ["Each ", "word ", "is ", "an ", "element.\n"];
Each word is an element.
> val it = [(), (), (), (), ()] : unit list
```

An here's an example of the latter, where we compose a function called _shout_ and map it to the same array:

```sml
- val shout = (sayToStream TextIO.stdOut) o (String.map Char.toUpper);
> val shout = fn : string -> unit
- shout "hello\n";
HELLO
> val it = () : unit
- List.map shout ["Each ", "word ", "is ", "an ", "element.\n"];
EACH WORD IS AN ELEMENT.
> val it = [(), (), (), (), ()] : unit list
```

`o` is the [functional composition](http://en.wikipedia.org/wiki/Function_composition) operator and glues two functions together. The operand order is backwards when compared with how the same operator works in maths. In maths, `_h_ = _g_ o _f_` would mean `_h_(_x_) = _f_(_g_(_x_))`, but in Standard ML, `_h_ = _g_ o _f_` means `_h_ _x_ = _g_ (_f_ _x_)`, which is completely arseways. Oh, well...

Another example of the nifty things curried functions allow you to do would be [OCaml](https://ocaml.org/)'s typesafe _[Printf.printf](http://caml.inria.fr/pub/docs/manual-ocaml/libref/Printf.html)_ function. It takes a formatting string and returns functions that accept arguments of the correct types for each placeholder in the formatting string. The consequence of this is that the kind of exploits _[printf](http://www.cplusplus.com/reference/clibrary/cstdio/printf.html)()_ and company are used for in C aren't possible in O'Caml. It's quite possible to do the same thing in Standard ML.

Keep in mind that functions are value too. That's the reason I've used brackets where I have. I've used them where there's an expression I want to evaluate before passing its result as an argument. `fac n - 1` means something quite different from `fac (n - 1)`.

Back to factorials. Now to try the same function, but this time using pattern matching instead:

```sml
(* fac2.sml *)
fun fac 0 = 1
  | fac n = n * fac (n - 1);

val _ = print (Int.toString (fac 5) ^ "\n");
```

Again, this gave me the same answer as my original _fac_ function: _120_.

Pattern matching is pretty useful. It can simplify code quite a bit by separating out the various cases of a function. Rather than having lots of conditional logic, we just make statements about what the results of evaluating the function are under different circumstances.

The pattern matching syntax above is shorthand for the following:

```sml
(* fac3.sml *)
fun fac n =
  case n of
    0 => 1
  | n => n * fac (n - 1);
```

Next up, I tried writing a function to join the elements of an array into a string. The function takes a function to convert each element to a string, a string to use a an element separator, and finally the list to join.

To avoid having to write any special purpose code, I decided to write a helper function that would take an extra parameter that would be prefixed onto the stringified list element. When the helper calls itself to cope with the list tail, it would then pass the separator argument as both the prefix and separator argument. When we're initially calling the helper function, an empty string is passed in the prefix argument.

```sml
(* join1.sml *)
fun helper _ _ _ [] = ""
  | helper toString pre sep (h::t) = pre ^ (toString h) ^ (helper toString sep sep t);

fun join toString sep lst = helper toString "" sep lst;
```

A quick note on this: notice `(_h_::_t_)` in the helper function's argument list. The `::` operator is the list construction operator and in patterns can be used to decompose a list into a head element and a trailing list. As I haven't mentioned it yet, `^` is the string concatenation operator.

Let's try executing it in the mosml REPL:

```sml
- load "Int";
> val it = () : unit
- join Int.toString ", " [1, 2, 3, 4, 5];
> val it = "1, 2, 3, 4, 5" : string
```

We don't really want the outside world to know about our helper functions. One way to hide them is to use a `local _pvtdecls_ in _decls_ end` block. This is particularly useful if the helpers are used by a number of different functions.

```sml
(* join2.sml *)
local
  fun helper _ _ _ [] = ""
    | helper toString pre sep (h::t) = pre ^ (toString h) ^ (helper toString sep sep t)
in
  fun join toString sep lst = helper toString "" sep lst
end;
```

Now only _join_ can see _helper_. However, as _join_ is the only function that needs to about _helper_, we can declare it within _join_ using a `let _decls_ in _expr_ end` block:

```sml
(* join3.sml *)
fun join toString sep lst =
let
  fun helper _ _ _ [] = ""
    | helper toString pre sep (h::t) = pre ^ (toString h) ^ (helper toString sep sep t)
in
  helper toString "" sep lst
end;
```

Because functions declared within other functions are contained within the scope of their parent function, we don't need to pass these values in, meaning we can simplify our helper function down like so:

```sml
(* join4.sml *)
fun join toString sep lst =
let
  fun helper _ [] = ""
    | helper pre (h::t) = pre ^ (toString h) ^ (helper sep t)
in
  helper "" lst
end;
```

I could've approached the join function differently. Rather than using a helper function an prefixing the separator on, I could've treated the separator as a suffix and omitted appending the suffix in the case of an one-element list:

```sml
(* join5.sml *)
fun join _ _ [] = ""
  | join toString _ [h] = toString h
  | join toString sep (h::t) = (toString h) ^ sep ^ (join toString sep t);
```

But then we wouldn't have learned as much. 😃

`[_h_]`, by the way, is a pattern that matches a single element list.

That's enough for now. I'll talk a bit about the type system later and about records, exceptions, references, the imperative side of the language, the module system, and all of that when I get the notion. However, if you've understood everything so far, you understand a fair bit of the core language.

In the meantime, you might want to read Mads Tofte's [Tips for Computer Scientists on Standard ML](http://www.itu.dk/people/sestoft/mosml/mosmllib.pdf) (PDF), which is quite readable and easy to understand, or Stephen Gilmore's [Programming in Standard ML 97: A Tutorial Introduction](http://www.dcs.ed.ac.uk/home/stg/NOTES/), which I found more difficult to follow in places, but covers everything in much more detail.
