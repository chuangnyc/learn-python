# Comprehensions are Python's signature feature for building collections.
# They replace the build-a-list-in-a-loop pattern with a single expression.
# Go has no equivalent -- you always write an explicit for loop and append.

# --- List Comprehensions ---
# Syntax: [expression for item in iterable if condition]

# The loop version...
squares = []
for n in range(5):
    squares.append(n * n)

# ...becomes one line:
squares = [n * n for n in range(5)]   # [0, 1, 4, 9, 16]
print(squares)

# With a filter (the `if` clause keeps items where the condition is True)
evens = [n for n in range(10) if n % 2 == 0]   # [0, 2, 4, 6, 8]
print(evens)

# Transform AND filter together
labels = [f"#{n}" for n in range(6) if n % 2]   # ['#1', '#3', '#5']
print(labels)

# Nested loops: clauses read left-to-right, same order as nested for loops
pairs = [(x, y) for x in range(2) for y in range(2)]
print(pairs)   # [(0, 0), (0, 1), (1, 0), (1, 1)]

# Flattening a 2D list
matrix = [[1, 2, 3], [4, 5, 6]]
flat = [val for row in matrix for val in row]   # [1, 2, 3, 4, 5, 6]
print(flat)

# Conditional EXPRESSION (ternary) goes before the `for`; this transforms
# every item rather than filtering. Don't confuse it with the filtering `if`.
signs = ["even" if n % 2 == 0 else "odd" for n in range(4)]
print(signs)   # ['even', 'odd', 'even', 'odd']


# --- Dict Comprehensions ---
# Syntax: {key_expr: value_expr for item in iterable if condition}

square_map = {n: n * n for n in range(5)}   # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
print(square_map)

# Invert a dict (swap keys and values)
original = {"a": 1, "b": 2, "c": 3}
inverted = {value: key for key, value in original.items()}
print(inverted)   # {1: 'a', 2: 'b', 3: 'c'}

# Build a lookup from two parallel lists with zip()
names = ["alice", "bob", "carol"]
ages = [30, 25, 35]
people = {name: age for name, age in zip(names, ages)}
print(people)   # {'alice': 30, 'bob': 25, 'carol': 35}


# --- Set Comprehensions ---
# Syntax: {expression for item in iterable} -- note braces, no key:value

unique_lengths = {len(word) for word in ["hi", "hey", "yo", "hello"]}
print(unique_lengths)   # {2, 3, 5} -- duplicates (hi/yo both len 2) collapse


# --- Generator Expressions ---
# Same syntax as a list comprehension but with PARENTHESES. The key difference:
# it's LAZY -- it yields items one at a time instead of building the whole list
# in memory. Ideal for large or infinite sequences, or feeding an aggregator.

gen = (n * n for n in range(1_000_000))   # nothing computed yet
print(type(gen))   # <class 'generator'>

# A generator is consumed once, on demand. Perfect for sum/max/any without
# materializing a giant intermediate list.
total = sum(n * n for n in range(1000))   # parens optional as sole call arg
print(total)

# any() / all() short-circuit over a generator -- they stop at the first
# decisive item instead of scanning everything.
has_negative = any(n < 0 for n in [3, 1, -4, 2])   # stops at -4
print(has_negative)   # True

all_positive = all(n > 0 for n in [3, 1, 4, 2])
print(all_positive)   # True

# Memory contrast: a list comp allocates every element up front; a generator
# holds one element at a time. Reach for a generator when you only iterate once.


# --- When NOT to use a comprehension ---
# If the logic needs multiple statements, side effects, or is hard to read,
# use a plain loop. Comprehensions are for BUILDING a collection, not for
# running side effects. This is a smell:
#     [print(x) for x in items]   # don't -- you're building a throwaway list
# Just write a for loop instead.


if __name__ == "__main__":
    print("=== Comprehensions ===\n")

    print("--- List comp: squares of evens 0-9 ---")
    print([n * n for n in range(10) if n % 2 == 0])

    print("\n--- Dict comp: char -> index ---")
    print({char: i for i, char in enumerate("abc")})

    print("\n--- Set comp: unique first letters ---")
    words = ["apple", "avocado", "banana", "cherry", "cranberry"]
    print({w[0] for w in words})

    print("\n--- Generator: sum of squares without a list ---")
    print(f"sum of squares 1-100: {sum(n * n for n in range(1, 101))}")

    print("\n--- Flatten a matrix ---")
    grid = [[1, 2], [3, 4], [5, 6]]
    print([val for row in grid for val in row])

    print("\n--- Common pattern: filter + transform ---")
    raw = ["  hello ", "WORLD", "  Python  "]
    cleaned = [s.strip().lower() for s in raw if s.strip()]
    print(cleaned)