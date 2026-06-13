# Python is dynamically typed: variables don't have fixed types,
# values do. A variable is just a name bound to an object.

# --- Basic Types ---

x = 42          # int (arbitrary precision, no overflow)
y = 3.14        # float (64-bit double)
z = 2 + 3j     # complex
name = "hello"  # str (immutable sequence of Unicode)
flag = True     # bool (subclass of int: True == 1, False == 0)
nothing = None  # NoneType (singleton, used like null)


# --- Dynamic Typing ---
# The same variable can be rebound to a different type at any time.

value = 10
value = "now a string"
value = [1, 2, 3]

# type() returns the runtime type of an object
print(type(value))  # <class 'list'>

# isinstance() checks against a type or tuple of types
print(isinstance(value, list))        # True
print(isinstance(value, (list, str))) # True


# --- Type Hints (Python 3.5+) ---
# Annotations are metadata only -- they don't enforce anything at runtime.
# They exist for readability, IDE support, and static analysis (mypy, pyright).

def greet(name: str, times: int = 1) -> str:
    return (f"Hello, {name}! " * times).strip()

# Python 3.10+ union syntax
def parse_id(raw: int | str) -> int:
    return int(raw)

# Python 3.9+ built-in generics (no need for typing.List, typing.Dict)
def first_item(items: list[str]) -> str | None:
    return items[0] if items else None


# --- Mutability ---
# Mutable: list, dict, set, bytearray
# Immutable: int, float, str, tuple, frozenset, bytes

# Immutable objects can't be changed in place
s = "hello"
# s[0] = "H"  # TypeError: 'str' object does not support item assignment
s = "H" + s[1:]  # creates a new string

# Mutable objects are changed in place
nums = [1, 2, 3]
nums.append(4)  # modifies the same list object

# This matters for function arguments and aliasing
a = [1, 2, 3]
b = a          # b points to the SAME list object
b.append(4)
print(a)       # [1, 2, 3, 4] -- a is affected because a and b are aliases

# To make an independent copy:
c = a.copy()        # shallow copy
c.append(5)
print(a)            # [1, 2, 3, 4] -- a is unaffected

# Deep copy for nested structures
import copy
nested = [[1, 2], [3, 4]]
shallow = nested.copy()
deep = copy.deepcopy(nested)

shallow[0].append(99)
print(nested[0])  # [1, 2, 99] -- shallow copy shares inner lists
print(deep[0])    # [1, 2] -- deep copy is fully independent


# --- Identity vs Equality ---

x = [1, 2, 3]
y = [1, 2, 3]
print(x == y)   # True  -- same value
print(x is y)   # False -- different objects in memory

# `is` checks identity (same object), `==` checks value equality.
# Use `is` only for singletons: None, True, False
if x is not None:
    print("x exists")


# --- Numeric Gotchas ---

# int: arbitrary precision — no fixed 32/64-bit cap; grows until memory runs out.
# Unlike C/Java (overflow) or JS (Infinity), 10**100 is still a normal int.
big = 10 ** 100
print(type(big))  # <class 'int'>

# float has precision limits (IEEE 754)
print(0.1 + 0.2)           # 0.30000000000000004
print(0.1 + 0.2 == 0.3)    # False

# Use math.isclose for float comparison
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True

# Integer division vs true division
print(7 / 2)   # 3.5 (true division, always returns float)
print(7 // 2)  # 3   (floor division)
print(-7 // 2) # -4  (floors toward negative infinity, unlike C which truncates)


if __name__ == "__main__":
    print("=== Types and Variables ===\n")

    print(f"greet('World', 2) = {greet('World', 2)}")
    print(f"parse_id('42') = {parse_id('42')}")
    print(f"first_item([]) = {first_item([])}")

    print(f"\n--- Mutability Demo ---")
    original = [1, 2, 3]
    alias = original
    independent = original.copy()
    alias.append(4)
    independent.append(5)
    print(f"original = {original}")      # [1, 2, 3, 4]
    print(f"alias = {alias}")            # [1, 2, 3, 4]
    print(f"independent = {independent}")  # [1, 2, 3, 5]

    print(f"\n--- Identity vs Equality ---")
    a = [1, 2]
    b = [1, 2]
    print(f"a == b: {a == b}")   # True
    print(f"a is b: {a is b}")   # False

    print(f"\n--- Numeric Precision ---")
    print(f"10**100 type: {type(10**100).__name__}")
    print(f"0.1 + 0.2 = {0.1 + 0.2}")
    print(f"7 // 2 = {7 // 2}, -7 // 2 = {-7 // 2}")
