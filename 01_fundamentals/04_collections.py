# Python's built-in collections cover most of what you'd reach for daily.
# Go gives you arrays, slices, and maps (plus structs). Python gives you
# lists, tuples, sets, and dicts as language built-ins -- each with literal
# syntax and a rich set of methods.

# --- Lists ---
# Ordered, mutable, allow duplicates. Closest to a Go slice, but heterogeneous.

nums = [1, 2, 3]
mixed = [1, "two", 3.0, [4]]   # a list can hold any mix of types

nums.append(4)          # add to end (like append(s, x) in Go)
nums.insert(0, 0)       # insert at index: [0, 1, 2, 3, 4]
nums.extend([5, 6])     # append all items from another iterable
popped = nums.pop()     # remove and return last item (6)
nums.remove(0)          # remove first matching VALUE (not index)
print(nums)             # [1, 2, 3, 4, 5]

# Indexing and slicing return list copies; slicing never panics on bounds.
print(nums[1:3])        # [2, 3]
print(nums[-1])         # 5 -- negative index counts from the end

# Useful operations
print(len(nums))        # 5
print(sum(nums))        # 15
print(sorted([3, 1, 2]))         # [1, 2, 3] -- returns a new list
print(sorted([3, 1, 2], reverse=True))  # [3, 2, 1]
nums.sort()             # sorts in place, returns None

# Go has no built-in sort syntax this terse; you'd use sort.Slice with a closure.


# --- Tuples ---
# Ordered, IMMUTABLE, allow duplicates. Use for fixed-size, heterogeneous
# records -- closest analog to a small Go struct or a multi-value return.

point = (3, 4)
single = (42,)          # one-element tuple NEEDS the trailing comma
empty = ()
no_parens = 1, 2, 3     # parentheses are optional; the comma makes the tuple

# Tuples are immutable: point[0] = 9 raises TypeError.
# Because they're hashable, tuples can be dict keys and set members (lists can't).

# Multiple return values are just tuples (like Go's multi-return)
def min_max(values: list[int]) -> tuple[int, int]:
    return min(values), max(values)

lo, hi = min_max([5, 2, 9, 1])   # tuple unpacking
print(lo, hi)                    # 1 9


# --- Unpacking ---
# Python unpacks any iterable into names. This goes well beyond Go.

a, b, c = [1, 2, 3]              # works on lists, tuples, strings, etc.
a, b = b, a                     # swap with no temp variable

# Starred unpacking captures "the rest" into a list
first, *rest = [1, 2, 3, 4]     # first=1, rest=[2, 3, 4]
*head, last = [1, 2, 3, 4]      # head=[1, 2, 3], last=4
x, *mid, z = [1, 2, 3, 4, 5]    # x=1, mid=[2, 3, 4], z=5
print(first, rest, last, mid)

# Unpacking into function calls
def add(x, y, z):
    return x + y + z
args = [1, 2, 3]
print(add(*args))               # spread a list as positional args


# --- Sets ---
# Unordered, mutable, NO duplicates. Membership tests are O(1).
# Go has no built-in set; people fake it with map[T]struct{}.

seen = {1, 2, 3, 3, 2}          # duplicates collapse: {1, 2, 3}
empty_set = set()               # {} is an empty DICT, not a set
seen.add(4)
seen.discard(99)                # remove if present, no error if absent
print(3 in seen)                # True -- fast membership test

# Set algebra (a major reason to reach for sets)
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a | b)    # union:                {1, 2, 3, 4, 5, 6}
print(a & b)    # intersection:         {3, 4}
print(a - b)    # difference:           {1, 2}
print(a ^ b)    # symmetric difference: {1, 2, 5, 6}

# frozenset is the immutable, hashable variant (can be a dict key / set member)
immutable = frozenset([1, 2, 3])


# --- Dicts ---
# Key-value mapping, mutable. Like a Go map, but keys can be any hashable type.
# As of Python 3.7+, dicts preserve INSERTION ORDER (Go maps are unordered).

user = {"name": "Ada", "age": 36}
user["email"] = "ada@example.com"   # add or update
print(user["name"])                 # Ada -- KeyError if key is missing

# Safe access without raising
print(user.get("phone"))            # None -- no KeyError
print(user.get("phone", "n/a"))     # "n/a" -- with a default

# setdefault: get the value, inserting a default if the key is absent
counts = {}
counts.setdefault("a", 0)
counts["a"] += 1

# Iteration
for key in user:                    # iterates over KEYS by default
    pass
for key, value in user.items():     # the common pattern, like Go's `range m`
    print(f"{key} -> {value}")
print(list(user.keys()))
print(list(user.values()))

# Membership tests check KEYS
print("name" in user)               # True

# Merging dicts (Python 3.9+)
defaults = {"theme": "dark", "lang": "en"}
overrides = {"lang": "fr"}
merged = defaults | overrides       # {"theme": "dark", "lang": "fr"}
print(merged)


# --- collections module: specialized containers ---
# The stdlib `collections` module fills common gaps so you don't reinvent them.

from collections import Counter, defaultdict, namedtuple

# Counter: tally hashable items (great for frequency-count interview problems)
freq = Counter("mississippi")
print(freq)                         # Counter({'s': 4, 'i': 4, 'p': 2, 'm': 1})
print(freq.most_common(2))          # [('s', 4), ('i', 4)]

# defaultdict: auto-creates a default value for missing keys
groups = defaultdict(list)
for word in ["apple", "ant", "bee"]:
    groups[word[0]].append(word)    # no need to check/init the key first
print(dict(groups))                 # {'a': ['apple', 'ant'], 'b': ['bee']}

# namedtuple: a lightweight, immutable record with named fields (struct-like)
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)                     # 3 4 -- access by name, still a tuple


if __name__ == "__main__":
    print("=== Collections ===\n")

    print("--- List ---")
    stack = [1, 2, 3]
    stack.append(4)
    print(f"after append: {stack}, pop: {stack.pop()}, now: {stack}")

    print("\n--- Tuple unpacking ---")
    coords = (10, 20)
    x, y = coords
    print(f"x={x}, y={y}")
    head, *tail = [1, 2, 3, 4]
    print(f"head={head}, tail={tail}")

    print("\n--- Set algebra ---")
    evens = {2, 4, 6, 8}
    small = {1, 2, 3, 4}
    print(f"evens & small = {evens & small}")
    print(f"evens | small = {evens | small}")

    print("\n--- Dict ---")
    inventory = {"apples": 3}
    inventory["bananas"] = 5
    print(f"inventory: {inventory}")
    print(f"get('cherries', 0): {inventory.get('cherries', 0)}")

    print("\n--- Counter (word frequency) ---")
    text = "the quick brown fox the lazy dog the end"
    word_counts = Counter(text.split())
    print(f"most common: {word_counts.most_common(2)}")