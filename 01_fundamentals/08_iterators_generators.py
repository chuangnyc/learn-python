# Iteration is everywhere in Python: `for` loops, comprehensions, unpacking,
# and functions like sum()/max()/sorted() all work on the SAME protocol.
# Generators let you produce values lazily -- one at a time, on demand --
# which is the closest Python gets to Go's "goroutine + channel" streaming.

# --- The Iteration Protocol ---
# Two dunder methods power every `for` loop:
#   __iter__()  -> returns an ITERATOR object
#   __next__()  -> returns the next value, or raises StopIteration when done
#
# An ITERABLE is anything with __iter__ (list, dict, str, set, file, ...).
# An ITERATOR is the cursor that produces values and remembers its position.

nums = [10, 20, 30]
it = iter(nums)            # iter(x) calls x.__iter__() -> an iterator
print(next(it))            # 10  -- next(it) calls it.__next__()
print(next(it))            # 20
print(next(it))            # 30
# next(it) now would raise StopIteration -- the loop's stop signal.

# A `for` loop is just this protocol with the StopIteration handled for you:
#   for x in nums:  <=>  it = iter(nums); while True: x = next(it) ... until StopIteration


# --- A Hand-Written Iterator Class ---
# You rarely need this (generators are easier), but it shows what's underneath.

class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self            # the object is its own iterator

    def __next__(self):
        if self.current <= 0:
            raise StopIteration   # signal "no more values"
        self.current -= 1
        return self.current + 1

for n in Countdown(3):
    print(n)                   # 3, 2, 1


# --- Generators: the easy way ---
# A function with `yield` is a GENERATOR FUNCTION. Calling it does NOT run the
# body -- it returns a generator object. The body runs lazily, pausing at each
# `yield` and resuming on the next next() call, preserving all local state.

def countdown(start):
    while start > 0:
        yield start            # hand back `start`, then PAUSE here
        start -= 1             # resumes here on the next iteration

gen = countdown(3)
print(type(gen).__name__)      # generator
print(list(gen))               # [3, 2, 1]
# Equivalent to the Countdown class above, but in 3 lines with no StopIteration
# bookkeeping -- the generator raises it automatically when the function ends.


# --- Why Lazy? Memory and Infinite Sequences ---
# A list builds every element up front. A generator holds ONE at a time.

def first_n_squares_list(n):
    return [i * i for i in range(n)]     # allocates all n elements now

def first_n_squares_gen(n):
    for i in range(n):
        yield i * i                       # produces one per request

# A generator can even be INFINITE -- impossible with a list.
def naturals():
    n = 0
    while True:                           # never terminates on its own
        yield n
        n += 1

# Safe because we stop pulling. itertools.islice takes just the first few.
import itertools
print(list(itertools.islice(naturals(), 5)))   # [0, 1, 2, 3, 4]


# --- Generators Are Single-Use ---
# Once exhausted, a generator is done. Iterating again yields nothing.

g = countdown(3)
print(list(g))   # [3, 2, 1]
print(list(g))   # []  <- already consumed; no "rewind"
# (A list, by contrast, can be looped over again and again.)


# --- Generator Expressions ---
# Same lazy behavior as a generator function, but in comprehension syntax with
# PARENTHESES. Ideal as an argument to an aggregator -- no intermediate list.

total = sum(i * i for i in range(1000))   # streams squares into sum()
print(total)                              # 332833500
# Compare: sum([i*i for i in range(1000)]) builds the whole list first.


# --- yield from: delegating to another iterable ---
# Flattens nested generators -- yields every item from a sub-iterable in turn.

def chain(*iterables):
    for it in iterables:
        yield from it          # = for x in it: yield x

print(list(chain([1, 2], (3, 4), "ab")))   # [1, 2, 3, 4, 'a', 'b']


# --- A Practical Generator: streaming pipeline ---
# Generators compose into lazy pipelines: each stage pulls from the previous
# one, processing a single item at a time -- like piping data through stages.

def read_lines(text):
    for line in text.splitlines():
        yield line

def non_empty(lines):
    for line in lines:
        if line.strip():
            yield line

def parse_ints(lines):
    for line in lines:
        yield int(line.strip())

raw = "1\n\n2\n  3  \n\n4"
pipeline = parse_ints(non_empty(read_lines(raw)))   # nothing consumed yet
print(sum(pipeline))   # 10 -- data flows one line at a time through 3 stages


# --- Go Comparison ---
# yield is the closest Python analog to streaming over a Go channel:
#   Go:     for v := range ch { ... }     // producer sends on ch in a goroutine
#   Python: for v in gen():     ...        // generator yields values lazily
# Key difference: a generator is single-threaded and COOPERATIVE -- it only
# advances when the consumer calls next(). No real concurrency, just
# paused/resumed execution on one thread.


if __name__ == "__main__":
    print("=== Iterators & Generators ===\n")

    print("--- Manual iterator protocol ---")
    it = iter([1, 2])
    print(f"next: {next(it)}, next: {next(it)}")

    print("\n--- Generator function ---")
    print(f"countdown(5): {list(countdown(5))}")

    print("\n--- Infinite generator + islice ---")
    evens = (n for n in naturals() if n % 2 == 0)
    print(f"first 5 evens: {list(itertools.islice(evens, 5))}")

    print("\n--- Single-use ---")
    once = countdown(2)
    print(f"first pass: {list(once)}, second pass: {list(once)}")

    print("\n--- yield from (flatten) ---")
    print(list(chain([1, 2], [3], [4, 5])))

    print("\n--- Lazy pipeline ---")
    data = "10\n\n  20\n30  \n\n"
    print(f"sum of parsed lines: {sum(parse_ints(non_empty(read_lines(data))))}")

    print("\n--- Fibonacci generator (from an earlier question) ---")
    def fib():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    print(f"first 10 fibs: {list(itertools.islice(fib(), 10))}")