# A context manager guarantees setup/teardown around a block via `with`.
# The classic case: open a resource, use it, and ALWAYS clean up -- even if
# an exception fires. This is Python's answer to Go's `defer`.

# --- The with Statement ---
# `with EXPR as var:` calls EXPR.__enter__() on entry and EXPR.__exit__() on
# exit (normal OR exception). The file is closed no matter how the block ends.

import os
tmp = "/tmp/_ctx_demo.txt"

with open(tmp, "w") as f:        # __enter__ returns the file -> bound to f
    f.write("hello\n")
    f.write("world\n")
# <- file is closed HERE automatically, even if write() had raised.

with open(tmp) as f:
    print(f.read().strip())      # hello\nworld

# Without `with`, you'd need try/finally to guarantee f.close():
#   f = open(tmp)
#   try:    ... use f ...
#   finally: f.close()
# `with` collapses that boilerplate -- similar role to Go's `defer f.Close()`.


# --- Writing a Context Manager as a Class ---
# Implement __enter__ (setup, returns the "as" value) and __exit__ (teardown).

class Timer:
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self                  # whatever you return is bound after `as`

    def __exit__(self, exc_type, exc_value, traceback):
        import time
        self.elapsed = time.perf_counter() - self.start
        print(f"  block took {self.elapsed*1000:.2f}ms")
        # Return False (or None) to let any exception propagate.
        # Return True to SUPPRESS the exception (rarely what you want).
        return False

with Timer():
    total = sum(range(100_000))
print(f"total = {total}")


# --- __exit__ Receives Exception Info ---
# The three args describe any exception raised in the block (all None if clean).
# This lets cleanup run AND lets you decide whether to swallow the error.

class ManagedResource:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"  acquire {self.name}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"  release {self.name}")     # always runs -- the cleanup
        if exc_type is not None:
            print(f"  (handled {exc_type.__name__}: {exc_value})")
        return True                          # True = suppress the exception

with ManagedResource("db-connection"):
    raise ValueError("boom")                 # release still runs; error suppressed
print("execution continues -- exception was suppressed")


# --- The Easy Way: @contextmanager ---
# contextlib turns a generator into a context manager. Code BEFORE yield is
# __enter__; the yielded value is the `as` target; code AFTER yield (in a
# finally) is __exit__. Far less boilerplate than a class.

from contextlib import contextmanager

@contextmanager
def managed(name):
    print(f"  open {name}")
    try:
        yield name                  # <- the `as` value; block runs here
    finally:
        print(f"  close {name}")    # runs on normal exit AND on exception

with managed("session") as s:
    print(f"  using {s}")


# --- Useful contextlib Helpers ---
from contextlib import suppress

# suppress: ignore specific exceptions (cleaner than try/except: pass)
with suppress(FileNotFoundError):
    os.remove("/tmp/does_not_exist_12345")   # no error if it's missing
print("suppress: missing file ignored")


# --- Multiple Context Managers ---
# Comma-separate (or use parentheses in 3.10+) to manage several at once.
src, dst = "/tmp/_ctx_src.txt", "/tmp/_ctx_dst.txt"
with open(src, "w") as f:
    f.write("copy me")

with open(src) as fin, open(dst, "w") as fout:
    fout.write(fin.read())          # both files closed when the block exits
print("copied:", open(dst).read())


if __name__ == "__main__":
    print("=== Context Managers ===\n")

    print("--- with + file (auto-close) ---")
    with open(tmp, "w") as f:
        f.write("line1\nline2")
    with open(tmp) as f:
        print(f"read back: {f.read()!r}")

    print("\n--- Class-based (Timer) ---")
    with Timer():
        _ = [x * x for x in range(50_000)]

    print("\n--- @contextmanager generator ---")
    with managed("transaction") as t:
        print(f"  working inside {t}")

    print("\n--- suppress ---")
    with suppress(ZeroDivisionError):
        result = 1 / 0
        print("never reached")
    print("  division error suppressed, moving on")

    # cleanup demo files
    for path in (tmp, src, dst):
        with suppress(FileNotFoundError):
            os.remove(path)
