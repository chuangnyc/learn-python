# Type hints annotate the expected types of variables, parameters, and returns.
# CRUCIAL: they are NOT enforced at runtime -- Python ignores them when running.
# They exist for static checkers (mypy, pyright), IDE autocomplete, and as
# documentation. Coming from Go's compile-time types, this is "optional, opt-in,
# checked by a separate tool" rather than "enforced by the language."

from __future__ import annotations   # lets all annotations be lazy/forward-ref


# --- Basic Annotations ---

name: str = "Ada"                    # variable annotation
age: int = 36
ratio: float = 1.5
active: bool = True

def greet(name: str, times: int = 1) -> str:   # params and return type
    return (f"Hi {name}! " * times).strip()

# Nothing checks these at runtime; greet(123) RUNS fine but mypy would flag it.


# --- Built-in Generics (Python 3.9+) ---
# Use lowercase built-ins directly; no need for typing.List/Dict in modern code.

def total(nums: list[int]) -> int:
    return sum(nums)

def index_users(users: dict[str, int]) -> list[str]:
    return list(users.keys())

coords: tuple[int, int] = (3, 4)         # fixed-size, typed positions
tags: set[str] = {"a", "b"}


# --- Optional and Union ---
# X | None means "X or None" (3.10+ syntax; older: Optional[X]).
# A | B means "either type" (older: Union[A, B]).

def find(items: list[str], target: str) -> int | None:
    return items.index(target) if target in items else None

def to_int(value: int | str) -> int:     # accepts int OR str
    return int(value)

result: int | None = find(["a", "b"], "b")


# --- Type Aliases ---
# Name a complex type once and reuse it for readability.

Vector = list[float]
Matrix = list[list[float]]
JsonDict = dict[str, "JsonValue"]        # can be recursive via forward ref
JsonValue = int | str | bool | None | list | dict

def scale(v: Vector, factor: float) -> Vector:
    return [x * factor for x in v]


# --- Callable: typing functions ---
# Callable[[ArgTypes], ReturnType] describes a function value (lesson 06).

from typing import Callable

def apply(fn: Callable[[int], int], value: int) -> int:
    return fn(value)

print(apply(lambda x: x * 2, 21))        # 42


# --- TypeVar and Generics ---
# A TypeVar is a placeholder so a function/class can work with ANY type while
# preserving the relationship between input and output (like Go generics).

from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T | None:   # returns the SAME type it received
    return items[0] if items else None

# Checkers know first([1,2,3]) is int|None and first(["a"]) is str|None.

# A generic class: Stack[int], Stack[str], etc.
from typing import Generic

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)

int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)


# --- Protocol: structural typing (recap from lesson 07) ---
# Define a SHAPE; any object with matching members satisfies it -- no
# inheritance needed. This is Python's equivalent of a Go interface, checked
# statically by mypy/pyright.

from typing import Protocol

class Sized(Protocol):
    def __len__(self) -> int: ...

def describe_size(obj: Sized) -> str:    # accepts ANYTHING with __len__
    return f"has {len(obj)} items"

print(describe_size([1, 2, 3]))          # works: list has __len__
print(describe_size("hello"))            # works: str has __len__
print(describe_size(int_stack))          # works: our Stack defined __len__


# --- Final, ClassVar, and Literal (handy extras) ---
from typing import Final, Literal

MAX_RETRIES: Final = 3                    # checker flags any reassignment

def set_mode(mode: Literal["r", "w", "a"]) -> str:   # only these exact values
    return f"opened in {mode} mode"

print(set_mode("r"))                      # ok; set_mode("x") would be flagged


# --- Running a Type Checker ---
# Type hints do nothing on their own. To actually catch type errors:
#   pip install mypy && mypy 01_fundamentals/13_typing.py
# mypy reads these annotations and reports mismatches WITHOUT running the code.


if __name__ == "__main__":
    print("=== Typing ===\n")

    print("--- Annotated function ---")
    print(f"  {greet('World', 2)}")

    print("\n--- Optional return ---")
    print(f"  find b -> {find(['a', 'b', 'c'], 'b')}")
    print(f"  find z -> {find(['a', 'b', 'c'], 'z')}")

    print("\n--- TypeVar preserves type ---")
    print(f"  first([10,20]) = {first([10, 20])}")
    print(f"  first([]) = {first([])}")

    print("\n--- Generic Stack[int] ---")
    s: Stack[int] = Stack()
    s.push(1); s.push(2); s.push(3)
    print(f"  len = {len(s)}, pop = {s.pop()}")

    print("\n--- Protocol (structural) ---")
    print(f"  {describe_size('typing')}")

    print("\n--- Literal ---")
    print(f"  {set_mode('w')}")
