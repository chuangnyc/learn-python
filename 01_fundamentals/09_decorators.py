# A decorator is a function that takes a function and returns a NEW function,
# usually wrapping the original to add behavior. The @syntax is just sugar.
# This builds directly on lesson 06: closures + functions as first-class objects.
# Go has no decorator syntax; you'd manually wrap funcs (middleware-style).

import functools
import time


# --- The Idea Without @ ---
# A decorator is any callable that wraps another function.

def shout(fn):
    def wrapper(name):
        return fn(name).upper()      # call the original, then modify its result
    return wrapper                   # return the replacement function

def greet(name):
    return f"hello, {name}"

greet = shout(greet)                 # manually wrap: greet is now the wrapper
print(greet("ada"))                  # HELLO, ADA


# --- The @ Syntax ---
# @shout above a def means: greet2 = shout(greet2). Pure syntactic sugar.

@shout
def greet2(name):
    return f"hi, {name}"

print(greet2("bob"))                 # HI, BOB


# --- General-Purpose Decorator (*args/**kwargs + functools.wraps) ---
# To wrap ANY function regardless of signature, accept *args/**kwargs.
# @functools.wraps copies the original's name/docstring onto the wrapper,
# so introspection (__name__, help()) still points at the real function.

def timer(fn):
    @functools.wraps(fn)             # preserve fn's identity/metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [{fn.__name__} took {elapsed*1000:.2f}ms]")
        return result
    return wrapper

@timer
def slow_square(n):
    time.sleep(0.01)
    return n * n

print(slow_square(9))                # prints timing, then 81
print(slow_square.__name__)          # slow_square (thanks to @wraps; else 'wrapper')


# --- Decorator That Takes Arguments ---
# Add one more layer: a function that RETURNS a decorator. Three nested levels:
#   repeat(times) -> decorator -> wrapper

def repeat(times):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def ping():
    print("  ping")
    return "pong"

ping()                               # prints "  ping" three times


# --- Stacking Decorators ---
# Decorators apply bottom-up: the one nearest the def wraps first.
# @timer @repeat(2) f  ==  timer(repeat(2)(f))

@timer
@repeat(times=2)
def work():
    return sum(range(100))

work()                               # repeat runs twice, timer measures the whole


# --- Common Stdlib Decorators ---

# functools.lru_cache: memoize results (huge win for recursive/expensive calls).
@functools.lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(50))                       # instant despite naive recursion -- cached
print(fib.cache_info())              # hits/misses stats

# You've already met these class-related decorators in lesson 07:
#   @property        -- expose a method as an attribute
#   @staticmethod    -- method that takes no self (a namespaced plain function)
#   @classmethod     -- method that takes the class (cls) instead of an instance

class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, f):     # alternative constructor
        return cls((f - 32) * 5 / 9)

    @staticmethod
    def is_freezing(celsius):        # utility tied to the class, no instance/cls
        return celsius <= 0

t = Temperature.from_fahrenheit(212)
print(t.celsius)                     # 100.0
print(Temperature.is_freezing(-5))   # True


if __name__ == "__main__":
    print("=== Decorators ===\n")

    print("--- @timer + @wraps ---")
    print(f"result: {slow_square(12)}")
    print(f"name preserved: {slow_square.__name__}")

    print("\n--- Decorator with args (@repeat) ---")
    ping()

    print("\n--- Stacked decorators ---")
    print(f"work() = {work()}")

    print("\n--- @lru_cache memoization ---")
    print(f"fib(40) = {fib(40)}")
    print(f"cache: {fib.cache_info()}")

    print("\n--- @classmethod / @staticmethod ---")
    boiling = Temperature.from_fahrenheit(212)
    print(f"212F = {boiling.celsius}C, freezing(-1)? {Temperature.is_freezing(-1)}")