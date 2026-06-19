# Functions in Python are first-class objects: you can pass them as arguments,
# return them from other functions, and store them in data structures.
# Go has first-class functions too, but Python adds flexible argument handling,
# default values, keyword arguments, and closures that capture by reference.

# --- Defining and Calling ---

def greet(name):
    return f"Hello, {name}!"

print(greet("Ada"))

# Functions always return something: with no explicit return, they return None.
def no_return():
    pass
print(no_return())   # None


# --- Default Arguments ---
# Parameters can have defaults, evaluated once at DEFINITION time.

def power(base, exp=2):     # exp defaults to 2 if not supplied
    return base ** exp

print(power(3))      # 9  -- uses default exp=2
print(power(3, 3))   # 27 -- overrides default

# GOTCHA: never use a MUTABLE default (list/dict/set). It's created once and
# shared across every call, so it accumulates state between calls.
def bad_append(item, target=[]):    # the [] is created ONCE
    target.append(item)
    return target

print(bad_append(1))   # [1]
print(bad_append(2))   # [1, 2]  <- surprise! same list reused

# The fix: use None as the sentinel and create a fresh object inside.
def good_append(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target

print(good_append(1))  # [1]
print(good_append(2))  # [2]  -- fresh list each call


# --- Positional vs Keyword Arguments ---

def describe(name, age, city):
    return f"{name}, {age}, from {city}"

print(describe("Bob", 30, "NYC"))                 # positional, by order
print(describe(age=30, city="LA", name="Carol"))  # keyword, order-independent
print(describe("Dan", city="SF", age=25))         # mix: positional then keyword

# Go has no keyword arguments; you'd pass a config struct to get the same clarity.


# --- *args and **kwargs ---
# *args collects extra POSITIONAL arguments into a tuple.
# **kwargs collects extra KEYWORD arguments into a dict.
# (The names are convention; the * and ** are what matter.)

def total(*args):              # args is a tuple
    return sum(args)

print(total(1, 2, 3, 4))       # 10 -- any number of positional args

def make_tag(tag, **kwargs):   # kwargs is a dict of attr=value
    attrs = " ".join(f'{k}="{v}"' for k, v in kwargs.items())
    return f"<{tag} {attrs}>"

print(make_tag("a", href="/home", target="_blank"))
# <a href="/home" target="_blank">

# Both together: *args before **kwargs
def log(level, *messages, **context):
    return f"[{level}] {' '.join(messages)} {context}"

print(log("INFO", "user", "logged", "in", user_id=42))

# The flip side: SPREAD an existing list/dict into a call with * and **
def point(x, y, z):
    return (x, y, z)

coords = [1, 2, 3]
print(point(*coords))                 # unpack list as positional args
kw = {"x": 1, "y": 2, "z": 3}
print(point(**kw))                     # unpack dict as keyword args


# --- Lambdas (anonymous functions) ---
# Single-expression functions. No statements, no return keyword -- the
# expression IS the return value. Keep them tiny; use def for anything real.

square = lambda x: x * x
print(square(5))   # 25

# Most common use: a key/callback passed to another function.
words = ["banana", "apple", "cherry"]
print(sorted(words, key=lambda w: len(w)))   # sort by length: ['apple', ...]

pairs = [(1, "one"), (3, "three"), (2, "two")]
print(sorted(pairs, key=lambda p: p[0]))     # sort by first element

# Go's closures fill a similar role, but Go has no one-line lambda literal
# distinct from func; Python's lambda is purely for short inline callbacks.


# --- Functions as First-Class Objects ---
# Assign to variables, store in collections, pass around.

def double(x): return x * 2
def triple(x): return x * 3

ops = {"double": double, "triple": triple}   # functions stored in a dict
print(ops["double"](10))   # 20

# Pass a function as an argument (higher-order function)
def apply_twice(fn, value):
    return fn(fn(value))

print(apply_twice(double, 5))   # 20 -- double(double(5))

# Built-in higher-order functions
nums = [1, 2, 3, 4, 5]
print(list(map(lambda x: x * x, nums)))         # [1, 4, 9, 16, 25]
print(list(filter(lambda x: x % 2 == 0, nums))) # [2, 4]
# (Often a comprehension reads better than map/filter -- both are idiomatic.)


# --- Closures ---
# A nested function that captures variables from the enclosing scope.
# The inner function "remembers" those variables even after the outer returns.

def make_counter():
    count = 0
    def increment():
        nonlocal count   # without this, count = ... would create a NEW local
        count += 1
        return count
    return increment      # return the inner function, closing over `count`

counter = make_counter()
print(counter())   # 1
print(counter())   # 2 -- state persists in the closure

# `nonlocal` lets the inner function REBIND an enclosing variable.
# (You don't need it to read or to mutate-in-place, only to reassign.)

# A closure factory: build customized functions
def multiplier(factor):
    return lambda x: x * factor   # captures `factor`

times3 = multiplier(3)
times10 = multiplier(10)
print(times3(5), times10(5))   # 15 50


if __name__ == "__main__":
    print("=== Functions ===\n")

    print("--- Defaults & keyword args ---")
    print(power(2, 10))                       # 1024
    print(describe(name="Eve", age=28, city="Austin"))

    print("\n--- *args / **kwargs ---")
    print(f"total(1..5) = {total(1, 2, 3, 4, 5)}")
    print(make_tag("img", src="cat.png", alt="a cat"))

    print("\n--- Higher-order: sort by custom key ---")
    people = [("alice", 30), ("bob", 25), ("carol", 35)]
    print(sorted(people, key=lambda p: p[1]))   # sort by age

    print("\n--- Closure: counter keeps state ---")
    c = make_counter()
    print([c(), c(), c()])   # [1, 2, 3]

    print("\n--- Mutable-default gotcha (fixed version) ---")
    print(good_append("x"), good_append("y"))   # ['x'] ['y'] -- independent