# Structural pattern matching (match/case, Python 3.10+) matches a value
# against PATTERNS, not just constants. It's far more powerful than a C/Go
# switch: it can destructure sequences, mappings, and objects, bind variables,
# and apply guards. Think "switch + unpacking + type check" in one construct.

# --- Basic match (like a switch) ---

def http_label(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:                      # _ is the wildcard / default (catch-all)
            return "Unknown"

print(http_label(200))               # OK
print(http_label(418))               # Unknown


# --- OR patterns and value binding ---

def categorize(status):
    match status:
        case 200 | 201 | 204:        # `|` matches any of these
            return "success"
        case 400 | 401 | 403 | 404:
            return "client error"
        case 500 | 502 | 503:
            return "server error"
        case code:                   # bare name BINDS the value (catch-all)
            return f"other: {code}"

print(categorize(201))               # success
print(categorize(302))               # other: 302


# --- Sequence Patterns (destructuring) ---
# Patterns can match the SHAPE of a list/tuple and bind its parts.
# *rest captures the middle/tail, just like unpacking in lesson 04.

def describe_point(point):
    match point:
        case (0, 0):
            return "origin"
        case (0, y):                 # x is 0, bind the second to y
            return f"on Y axis at {y}"
        case (x, 0):
            return f"on X axis at {x}"
        case (x, y):
            return f"point ({x}, {y})"
        case _:
            return "not a 2D point"

print(describe_point((0, 0)))        # origin
print(describe_point((0, 5)))        # on Y axis at 5
print(describe_point((3, 4)))        # point (3, 4)

def head_tail(items):
    match items:
        case []:
            return "empty"
        case [single]:
            return f"one item: {single}"
        case [first, *rest]:         # bind first, capture the rest as a list
            return f"first={first}, rest={rest}"

print(head_tail([]))                 # empty
print(head_tail([1, 2, 3, 4]))       # first=1, rest=[2, 3, 4]


# --- Guards (extra conditions with if) ---

def classify_number(n):
    match n:
        case 0:
            return "zero"
        case x if x < 0:             # pattern PLUS a boolean guard
            return "negative"
        case x if x % 2 == 0:
            return "positive even"
        case _:
            return "positive odd"

print(classify_number(-3))           # negative
print(classify_number(4))            # positive even
print(classify_number(7))            # positive odd


# --- Mapping Patterns (dicts) ---
# Match on keys present; bind their values. Extra keys are ignored.

def handle_event(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"click at ({x}, {y})"
        case {"type": "key", "key": k}:
            return f"key press: {k}"
        case {"type": t}:
            return f"unhandled event type: {t}"
        case _:
            return "not an event"

print(handle_event({"type": "click", "x": 10, "y": 20}))   # click at (10, 20)
print(handle_event({"type": "scroll", "delta": 5}))        # unhandled: scroll


# --- Class Patterns (match on type + attributes) ---
# Destructure objects by type and capture their fields. Works great with
# dataclasses (lesson 07).

from dataclasses import dataclass

@dataclass
class Circle:
    radius: float

@dataclass
class Rectangle:
    width: float
    height: float

def area(shape):
    match shape:
        case Circle(radius=r):                   # match type, bind attribute
            return 3.14159 * r ** 2
        case Rectangle(width=w, height=h):
            return w * h
        case _:
            raise ValueError("unknown shape")

print(area(Circle(radius=5)))        # 78.53975
print(area(Rectangle(3, 4)))         # 12


# --- Capturing the whole match with `as` ---

def first_admin(users):
    match users:
        case [{"role": "admin"} as admin, *_]:   # bind the matched dict to admin
            return admin["name"]
        case _:
            return None

print(first_admin([{"role": "admin", "name": "root"}, {"role": "user"}]))  # root


# --- Go Comparison ---
# Go's switch matches values/types but cannot destructure. Python's match is
# closer to Rust's match or a functional language's pattern matching: it
# inspects structure and binds names in one step. Use it when you'd otherwise
# write a chain of isinstance() checks plus manual unpacking.


if __name__ == "__main__":
    print("=== Pattern Matching ===\n")

    print("--- Literal + wildcard ---")
    for code in (200, 404, 999):
        print(f"  {code}: {http_label(code)}")

    print("\n--- Sequence destructuring ---")
    print(f"  {describe_point((0, 7))}")
    print(f"  {head_tail([10, 20, 30])}")

    print("\n--- Guards ---")
    for n in (-5, 0, 6, 9):
        print(f"  {n}: {classify_number(n)}")

    print("\n--- Mapping pattern ---")
    print(f"  {handle_event({'type': 'key', 'key': 'Enter'})}")

    print("\n--- Class pattern ---")
    shapes = [Circle(2), Rectangle(5, 6)]
    for s in shapes:
        print(f"  {type(s).__name__}: area = {area(s):.2f}")
