# String Manipulation is an interview staple because Python strings are
# immutable (like Go strings) but come with a huge, expressive method set.
# -- Key Python facts for a Go dev:
#    1. Strings are immutable sequences of Unicode code points. "Mutating" a
#       string always builds a NEW one, so build with a list + "".join(...)
#       instead of repeated += in a loop (that's O(n^2), same trap as Go).
#    2. Iterating a string yields characters; there's no separate rune type.
#    3. collections.Counter is the idiomatic frequency map (Go: map[rune]int).
# -- Common shapes: anagrams, palindromes, encoding/run-length, frequency.

from collections import Counter


# --- Anagram check ---
# Two strings are anagrams if they share the same character multiset.
# Counter builds a frequency map in one pass; comparing two Counters is O(n).
# (In Go you'd build two map[rune]int and compare manually.)
def is_anagram(a, b):
    if len(a) != len(b):
        return False
    return Counter(a) == Counter(b)


# --- Group anagrams ---
# Words are grouped if their sorted letters match. The sorted tuple of chars
# is a hashable key -> dict of key -> list. setdefault avoids a manual
# "if key not in map" check (Go has no equivalent; you check explicitly).
def group_anagrams(words):
    groups = {}
    for word in words:
        key = tuple(sorted(word))   # ("e","a","t") for "eat"/"tea"/"ate"
        groups.setdefault(key, []).append(word)
    return list(groups.values())


# --- Run-length encoding ---
# Compress runs of identical chars: "aaabbc" -> "a3b2c1". Build pieces in a
# list and join once at the end to avoid quadratic string concatenation.
def rle_encode(s):
    if not s:
        return ""
    out = []
    prev = s[0]
    count = 1
    for ch in s[1:]:
        if ch == prev:
            count += 1
        else:
            out.append(f"{prev}{count}")
            prev = ch
            count = 1
    out.append(f"{prev}{count}")
    return "".join(out)


# --- First non-repeating character ---
# Return the index of the first char that appears exactly once, else -1.
# Counter for frequencies, then a second pass to find the first count==1.
def first_unique_char(s):
    freq = Counter(s)
    for i, ch in enumerate(s):
        if freq[ch] == 1:
            return i
    return -1


# --- Longest substring without repeating characters ---
# Sliding window of unique chars. `seen` maps char -> last index. When we hit
# a repeat inside the window, jump `start` past the previous occurrence.
def longest_unique_substring(s):
    seen = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in seen and seen[ch] >= start:
            start = seen[ch] + 1    # shrink window past the duplicate
        seen[ch] = i
        best = max(best, i - start + 1)
    return best


# --- Valid palindrome, alphanumeric only ---
# Normalize (drop non-alphanumerics, lowercase) then two-pointer compare.
# str.isalnum / str.lower handle Unicode correctly out of the box.
def is_clean_palindrome(s):
    cleaned = [ch.lower() for ch in s if ch.isalnum()]
    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True


if __name__ == "__main__":
    print("=== Anagrams ===")
    print(f"is_anagram('listen', 'silent') = {is_anagram('listen', 'silent')}")  # True
    print(f"is_anagram('foo', 'bar')       = {is_anagram('foo', 'bar')}")        # False
    print(f"group_anagrams(['eat','tea','tan','ate','nat','bat']) =")
    print(f"  {group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])}")

    print("\n=== Encoding ===")
    print(f"rle_encode('aaabbc') = {rle_encode('aaabbc')}")  # a3b2c1

    print("\n=== Frequency / windows ===")
    print(f"first_unique_char('leetcode') = {first_unique_char('leetcode')}")  # 0
    print(f"first_unique_char('aabb')     = {first_unique_char('aabb')}")      # -1
    print(f"longest_unique_substring('abcabcbb') = {longest_unique_substring('abcabcbb')}")  # 3
    print(f"longest_unique_substring('bbbbb')    = {longest_unique_substring('bbbbb')}")     # 1

    print("\n=== Palindrome ===")
    print(f"is_clean_palindrome('A man, a plan, a canal: Panama') = "
          f"{is_clean_palindrome('A man, a plan, a canal: Panama')}")  # True
    print(f"is_clean_palindrome('race a car') = {is_clean_palindrome('race a car')}")  # False
