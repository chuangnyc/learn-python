# Strings in Python are immutable sequences of Unicode characters.
# Unlike Go, there's no separate byte/rune distinction -- str is always Unicode text.
# For raw bytes, Python has a separate `bytes` type (similar to Go's []byte).

# --- String Literals ---

single = 'hello'
double = "hello"          # no difference between single and double quotes
multi = """line one
line two
line three"""             # triple quotes for multi-line (like Go backtick strings)

raw = r"no \n escape"    # raw string, backslashes are literal (like Go `raw strings`)
print(raw)               # no \n escape


# --- f-strings (Python 3.6+) ---
# Similar to fmt.Sprintf, but embedded directly in the string.

name = "World"
count = 3
print(f"Hello, {name}!")              # variable interpolation
print(f"count * 2 = {count * 2}")     # expressions inside braces
print(f"{'left':<10}|{'right':>10}")  # format spec: alignment and width
print(f"{3.14159:.2f}")               # format spec: decimal places
print(f"{1000000:,}")                 # format spec: thousands separator

# In Go you'd write: fmt.Sprintf("Hello, %s! count = %d", name, count)


# --- Slicing ---
# Python slicing uses [start:stop:step]. stop is exclusive.
# Go slices work similarly but only support [start:stop].

s = "abcdefgh"
print(s[0])      # 'a' -- indexing
print(s[-1])     # 'h' -- negative index counts from end
print(s[2:5])    # 'cde' -- slice from index 2 up to (not including) 5
print(s[:3])     # 'abc' -- from start
print(s[5:])     # 'fgh' -- to end
print(s[::2])    # 'aceg' -- every 2nd character
print(s[::-1])   # 'hgfedcba' -- reverse (no equivalent one-liner in Go)


# --- Common String Methods ---
# Strings are immutable, so methods always return a new string.

text = "  Hello, World!  "
print(text.strip())          # "Hello, World!" -- trim whitespace (like strings.TrimSpace)
print(text.lower())          # "  hello, world!  "
print(text.upper())          # "  HELLO, WORLD!  "
print(text.replace("World", "Python"))

# Checking content
print("hello".startswith("he"))  # True (like strings.HasPrefix)
print("hello".endswith("lo"))    # True (like strings.HasSuffix)
print("hello".isalpha())         # True
print("123".isdigit())           # True

# Finding substrings
print("hello world".find("world"))  # 6 (like strings.Index, returns -1 if not found)
print("hello world".count("l"))     # 3 (like strings.Count)
print("world" in "hello world")     # True -- `in` operator for containment


# --- Split and Join ---
# In Go: strings.Split / strings.Join

csv = "one,two,three"
parts = csv.split(",")        # ['one', 'two', 'three']
print(parts)

rejoined = " | ".join(parts)  # "one | two | three"
print(rejoined)

# Split with maxsplit
print("a.b.c.d".split(".", 2))  # ['a', 'b', 'c.d'] -- split at most 2 times

# Splitlines for multi-line strings
lines = "line1\nline2\nline3".splitlines()
print(lines)  # ['line1', 'line2', 'line3']


# --- String Multiplication and Concatenation ---

print("ha" * 3)        # "hahaha" -- repeat operator (no Go equivalent)
print("hello" + " " + "world")  # concatenation (same as Go)

# For building strings in a loop, use join (like strings.Builder in Go)
# BAD: s += chunk in a loop creates a new string each time
# GOOD:
chunks = ["hello", "world", "from", "python"]
result = " ".join(chunks)


# --- Encoding: str vs bytes ---
# str = Unicode text, bytes = raw byte sequence
# In Go, string is already a byte slice with UTF-8 encoding by default.

text = "café"                    # str with Unicode
encoded = text.encode("utf-8")       # bytes: b'caf\xc3\xa9'
decoded = encoded.decode("utf-8")    # back to str: "café"
print(f"str: {text}, bytes: {encoded}, len(str): {len(text)}, len(bytes): {len(encoded)}")
# len(str) = 4 characters, len(bytes) = 5 bytes (é is 2 bytes in UTF-8)
# In Go: len("café") gives byte length, utf8.RuneCountInString gives rune count


# --- String Formatting Styles ---
# f-strings are preferred, but you'll encounter these in older code:

# % formatting (old style, like C's printf)
print("Hello, %s! Count: %d" % ("World", 5))

# .format() method (Python 2.6+)
print("Hello, {}! Count: {}".format("World", 5))

# f-string (Python 3.6+, preferred)
print(f"Hello, {'World'}! Count: {5}")


if __name__ == "__main__":
    print("=== Strings ===\n")

    # Demonstrate slicing
    word = "python"
    print(f"word = '{word}'")
    print(f"word[0:2] = '{word[0:2]}'")
    print(f"word[::-1] = '{word[::-1]}'")

    # Demonstrate split/join round-trip
    path = "/usr/local/bin"
    parts = path.split("/")
    print(f"\nsplit('{path}') = {parts}")
    print(f"join back = {'/'.join(parts)}")

    # Demonstrate encoding
    emoji = "hello 🐍"
    print(f"\n'{emoji}' has {len(emoji)} characters, {len(emoji.encode('utf-8'))} bytes")

    # Common interview pattern: check if two strings are anagrams
    def is_anagram(a: str, b: str) -> bool:
        return sorted(a.lower()) == sorted(b.lower())

    print(f"\nis_anagram('listen', 'silent') = {is_anagram('listen', 'silent')}")
    print(f"is_anagram('hello', 'world') = {is_anagram('hello', 'world')}")
