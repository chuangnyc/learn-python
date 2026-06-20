# Python uses EXCEPTIONS for errors, not return values. This is the biggest
# mental shift from Go: there's no `if err != nil`. Code raises exceptions and
# callers catch them, often far up the stack. The idiom is EAFP -- "easier to
# ask forgiveness than permission": try the operation, handle failure if it comes.

# --- try / except ---
# Catch by exception type. Always catch the most specific type you can.

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:        # catch a specific exception
        return None

print(safe_divide(10, 2))            # 5.0
print(safe_divide(10, 0))            # None

# Capture the exception object with `as` to inspect it.
try:
    int("not a number")
except ValueError as e:
    print(f"caught: {e}")            # caught: invalid literal for int()...

# Catch multiple types with a tuple.
def parse(value):
    try:
        return int(value)
    except (ValueError, TypeError) as e:
        return f"bad input ({type(e).__name__})"

print(parse("42"))                   # 42
print(parse("oops"))                 # bad input (ValueError)
print(parse(None))                   # bad input (TypeError)


# --- else and finally ---
# else: runs ONLY if no exception occurred (the success path).
# finally: ALWAYS runs -- cleanup, like Go's defer. Runs even on return/raise.

def read_config(text):
    try:
        value = int(text)
    except ValueError:
        print("  parse failed")
        return None
    else:
        print("  parse succeeded")   # only when try block had no error
        return value
    finally:
        print("  finally always runs")

read_config("123")
read_config("abc")


# --- EAFP vs LBYL ---
# LBYL ("look before you leap"): check preconditions first. Common in Go.
# EAFP ("easier to ask forgiveness"): just try it. The idiomatic Python way --
# avoids race conditions and redundant checks.

data = {"name": "Ada"}

# LBYL (less Pythonic here)
if "name" in data:
    name = data["name"]
else:
    name = "unknown"

# EAFP (more Pythonic)
try:
    name = data["name"]
except KeyError:
    name = "unknown"

# ...though for this exact case, dict.get is cleaner than either. Pick the
# clearest tool; EAFP shines when the "check" is expensive or racy (files, I/O).


# --- Raising Exceptions ---
# Use `raise` to signal an error. Raise a specific built-in or a custom type.

def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise ValueError(f"insufficient funds: have {balance}, need {amount}")
    return balance - amount

try:
    withdraw(100, 150)
except ValueError as e:
    print(f"rejected: {e}")


# --- Custom Exceptions ---
# Define your own by subclassing Exception. Build a hierarchy so callers can
# catch broadly (PaymentError) or narrowly (CardDeclined).

class PaymentError(Exception):
    """Base class for all payment failures."""

class InsufficientFunds(PaymentError):
    def __init__(self, needed, available):
        self.needed = needed
        self.available = available
        super().__init__(f"need {needed}, have {available}")

class CardDeclined(PaymentError):
    pass

def charge(available, amount):
    if amount > available:
        raise InsufficientFunds(amount, available)
    return available - amount

try:
    charge(50, 100)
except InsufficientFunds as e:           # catch the specific subclass
    print(f"specific: short by {e.needed - e.available}")
except PaymentError:                     # ...or any payment error
    print("some payment error")


# --- Re-raising and Exception Chaining ---
# `raise` with no args re-raises the current exception (e.g. after logging).
# `raise New from old` chains, preserving the original cause in the traceback.

def load_user(raw):
    try:
        return int(raw)
    except ValueError as e:
        raise PaymentError("could not load user id") from e   # chains the cause

try:
    load_user("xyz")
except PaymentError as e:
    print(f"chained: {e} (caused by {type(e.__cause__).__name__})")


# --- The Exception Hierarchy (partial) ---
# BaseException
#  +-- Exception            <- catch THIS, not BaseException
#       +-- ValueError, TypeError, KeyError, IndexError, FileNotFoundError, ...
# `except Exception:` catches normal errors but NOT KeyboardInterrupt/SystemExit
# (those derive from BaseException). Never use a bare `except:` -- it swallows
# Ctrl-C and hides bugs.


if __name__ == "__main__":
    print("=== Error Handling ===\n")

    print("--- try/except ---")
    print(f"10/0 -> {safe_divide(10, 0)}")

    print("\n--- else/finally flow ---")
    read_config("99")

    print("\n--- raise + catch ---")
    try:
        withdraw(20, 50)
    except ValueError as e:
        print(f"caught: {e}")

    print("\n--- custom exception hierarchy ---")
    try:
        charge(10, 25)
    except PaymentError as e:
        print(f"caught {type(e).__name__}: {e}")

    print("\n--- exception chaining ---")
    try:
        load_user("not-an-int")
    except PaymentError as e:
        print(f"{e}  <-  {type(e.__cause__).__name__}: {e.__cause__}")
