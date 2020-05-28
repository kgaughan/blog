Title: Scoping and use of the 'global' keyword in Python
Slug: global-in-python
Date: 2010-08-31 17:34
Category: Coding
Status: published

[Here's something I knocked up for one of my co-workers who's an experienced developer, but a Python neophyte. It may be useful to others.]

As in PHP, the `global` keyword in Python declares that any reference to a given variable name within the scope of a function or method refers to a variable in module/global scope. However, the scoping behaviour of the two languages differs subtly.

In PHP, variables within a function or method are local unless declared as global. With Python, the behaviour is more subtle. Firstly, let's take a simple case:

```python
foo = 0

def bar():
	print "In bar(), foo is", foo

bar()
print "And in module scope, foo is", foo
```

This will result in:

```text
In bar(), foo is 0
And in module scope, foo is 0
```

However, if we try to modify *foo* without declaring it global:

```python
foo = 0

def bar():
	print "Entering bar(), foo is", foo
	foo += 1
	print "Leaving bar(), foo is", foo

bar()
print "And in module scope, foo is", foo
```

You'll get an error:

```text
Entering bar(), foo is
Traceback (most recent call last):
  File "globaltest.py", line 8, in <module>bar()
  File "globaltest.py", line 4, in bar
    print "Entering bar(), foo is", foo
UnboundLocalError: local variable 'foo' referenced before assignment
```

This is because module/global scope is a read-only shadow within the local function/method scope: you can access it, providing there's nothing declared with the same name in local scope, but you can't change it. There are very good, though non-trivial, reasons for this behaviour.

If you _specifically_ want to be able to change the value a given variable in the global scope contains, then use the `global` keyword.

```python
foo = 0

def bar():
	global foo
	print "Entering bar(), foo is", foo
	foo += 1
	print "Leaving bar(), foo is", foo

bar()
print "And in module scope, foo is", foo
```

Which yields:

```text
Entering bar(), foo is 0
Leaving bar(), foo is 1
And in module scope, foo is 1
```

However, if all you want to do is access methods on the object the variable contains a reference to, `global` isn't needed, and should be avoided.

## What's the reason for this behaviour?

In a nutshell, functions types and modules are just regular objects, no different from any other object, and when you declare a function or class, or import a module, you're just using some syntactic sugar around a variable assignment. If Python behaved like PHP, you'd need to do stuff like this:

```python
def boogie():
	print "I'm dancing, I'm dancing!"


def claptrap():
	# 'boogie' is a variable that contains a reference to the function
	# object declared above.
	global boogie
	print "Come on everybody check me out."
	boogie()


claptrap()
```

Also, Python are simply pigeonholes for holding references to objects; variables are not the objects they contain and everything, even number and strings, are objects. Variables containing immutable objects like numbers and strings may appear to act otherwise, but this is simply because those types of object are immutable.
