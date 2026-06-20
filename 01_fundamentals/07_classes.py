# Python classes bundle data and behavior. Coming from Go, the big shifts:
# Python has real inheritance (Go has only struct embedding + interfaces),
# there's no public/private keyword (just naming conventions), and "magic"
# dunder methods (__init__, __str__, __eq__, ...) hook into language operators.

# --- Defining a Class ---

class Dog:
    # Class variable: shared by ALL instances (like a Go package-level var).
    species = "Canis familiaris"

    # __init__ is the constructor. `self` is the instance (Go's receiver),
    # and it's ALWAYS the explicit first parameter of every method.
    def __init__(self, name, age):
        self.name = name    # instance variables: unique per object
        self.age = age

    # A regular method. `self` gives access to the instance.
    def bark(self):
        return f"{self.name} says woof!"

    def birthday(self):
        self.age += 1
        return self.age

rex = Dog("Rex", 3)
print(rex.bark())        # Rex says woof!
print(rex.species)       # Canis familiaris (read from the class)
print(rex.birthday())    # 4


# --- "Private" by Convention ---
# Python has NO access keywords. Conventions instead:
#   _name   -> "internal, please don't touch" (single underscore)
#   __name  -> name-mangled to _ClassName__name (avoids subclass clashes)

class BankAccount:
    def __init__(self, balance):
        self._balance = balance        # convention: treat as internal
        self.__pin = "1234"            # name-mangled, harder to access by accident

    def deposit(self, amount):
        self._balance += amount
        return self._balance

acct = BankAccount(100)
print(acct.deposit(50))   # 150
print(acct._balance)      # 150 -- still accessible; nothing is truly enforced


# --- Properties (computed/guarded attributes) ---
# @property exposes a method as if it were an attribute. Use it for computed
# values or to validate on assignment, without changing the caller's syntax.

class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):              # getter: accessed as circle.radius (no parens)
        return self._radius

    @radius.setter
    def radius(self, value):       # setter: runs on circle.radius = ...
        if value < 0:
            raise ValueError("radius cannot be negative")
        self._radius = value

    @property
    def area(self):                # read-only computed attribute
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.area)        # 78.53975 -- looks like an attribute, runs a method
c.radius = 10        # goes through the setter (validates)
print(c.area)        # 314.159


# --- Dunder (Magic) Methods ---
# Double-underscore methods let your objects work with built-in operators and
# functions: print(), ==, <, len(), [], etc. This is Python's operator hooks.

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # __repr__: unambiguous, dev-facing (used in the REPL, debugging, lists).
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    # __str__: human-facing (used by print/str). Falls back to __repr__ if absent.
    def __str__(self):
        return f"({self.x}, {self.y})"

    # __eq__: defines == comparison (default compares identity, like `is`).
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # __add__: defines the + operator.
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    # __len__: makes len(v) work.
    def __len__(self):
        return 2

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)           # (4, 6)   -- __add__ then __str__
print(v1 == Vector(1, 2))  # True   -- __eq__
print(repr(v1))          # Vector(1, 2)
print([v1, v2])          # [Vector(1, 2), Vector(3, 4)] -- lists use __repr__


# --- Inheritance ---
# Python supports single and multiple inheritance. super() calls the parent.

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("subclasses must implement speak()")

class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name)     # call the parent constructor
        self.indoor = indoor

    def speak(self):               # override the parent method
        return f"{self.name} says meow"

felix = Cat("Felix")
print(felix.speak())               # Felix says meow
print(isinstance(felix, Animal))   # True -- Cat IS-A Animal


# --- @dataclass: boilerplate-free data holders ---
# @dataclass auto-generates __init__, __repr__, and __eq__ from annotated
# fields. This is the idiomatic "struct with methods" -- closest to a Go struct.

from dataclasses import dataclass, field

@dataclass
class Point:
    x: int
    y: int
    label: str = "origin"          # field with a default

    def distance_to(self, other):  # you can still add methods
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

p1 = Point(0, 0)
p2 = Point(3, 4)
print(p1)                  # Point(x=0, y=0, label='origin')  -- free __repr__
print(p1 == Point(0, 0))   # True                             -- free __eq__
print(p2.distance_to(p1))  # 5.0

# Use field(default_factory=...) for mutable defaults (same gotcha as functions)
@dataclass
class Cart:
    items: list = field(default_factory=list)   # fresh list per instance

# @dataclass(frozen=True) makes instances immutable and hashable.


# --- Protocols: duck typing, structural typing (like Go interfaces) ---
# A Protocol defines a SHAPE. Any class with matching methods satisfies it --
# no explicit "implements" needed. This is exactly Go's structural interfaces.

from typing import Protocol

class Speaker(Protocol):
    def speak(self) -> str: ...    # any object with a speak() -> str fits

def announce(speaker: Speaker) -> str:
    return f"Announcement: {speaker.speak()}"

# Cat never declared it implements Speaker, but it has speak(), so it works.
print(announce(felix))             # Announcement: Felix says meow
# "If it walks like a duck and quacks like a duck, it's a duck." Python checks
# behavior, not declared type -- the same philosophy as Go interfaces, but
# Python doesn't even require the type hint to actually call the method.


if __name__ == "__main__":
    print("=== Classes ===\n")

    print("--- Basic class ---")
    d = Dog("Buddy", 2)
    print(d.bark(), "| age after birthday:", d.birthday())

    print("\n--- Property with validation ---")
    circle = Circle(3)
    print(f"area: {circle.area:.2f}")
    try:
        circle.radius = -1
    except ValueError as e:
        print(f"rejected: {e}")

    print("\n--- Operator overloading ---")
    print(f"{Vector(1, 1)} + {Vector(2, 3)} = {Vector(1, 1) + Vector(2, 3)}")

    print("\n--- Inheritance ---")
    animals = [Cat("Mochi"), Cat("Tom", indoor=False)]
    for a in animals:
        print(f"{a.name} (indoor={a.indoor}): {a.speak()}")

    print("\n--- dataclass ---")
    origin = Point(0, 0)
    far = Point(6, 8)
    print(f"{far} is {far.distance_to(origin)} from {origin}")

    print("\n--- Protocol (duck typing) ---")
    print(announce(Cat("Whiskers")))