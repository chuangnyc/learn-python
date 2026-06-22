# Sorting arranges elements in order. Python's built-in sort (Timsort) is
# excellent -- O(n log n), stable, and what you should ALWAYS use in real code.
# We implement merge sort and quick sort from scratch because they teach the
# two great algorithmic strategies and show up constantly in interviews.
# -- The two strategies (both divide-and-conquer, both O(n log n) typical):
#    - MERGE SORT: split in half, sort each half, MERGE the sorted halves.
#      Always O(n log n); stable; needs O(n) extra space.
#    - QUICK SORT: pick a pivot, PARTITION around it, recurse on each side.
#      O(n log n) average but O(n^2) worst case; in-place; not stable.
# -- Also covered: how to control Python's sort with `key` and comparators,
#    which is what you'll actually use day to day.


# --- Merge sort ---
# Divide: split the list into halves until each piece has one element (trivially
# sorted). Conquer: merge sorted pieces back together. The merge step walks two
# sorted lists with two pointers, always taking the smaller front element.
def merge_sort(nums):
    if len(nums) <= 1:                  # base case: 0 or 1 element is sorted
        return nums
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])       # sort each half recursively
    right = merge_sort(nums[mid:])
    return _merge(left, right)

def _merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:         # <= keeps it STABLE (ties keep order)
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])             # append whatever remains in either half
    merged.extend(right[j:])
    return merged


# --- Quick sort ---
# Pick a pivot, partition the rest into "< pivot" and ">= pivot", recurse on
# each, and concatenate. This version is readable (extra lists); a production
# quick sort partitions in place to save memory.
def quick_sort(nums):
    if len(nums) <= 1:
        return nums
    pivot = nums[len(nums) // 2]        # middle element as pivot
    less = [x for x in nums if x < pivot]
    equal = [x for x in nums if x == pivot]
    greater = [x for x in nums if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)
    # Worst case O(n^2) if pivots are consistently bad (e.g. already-sorted input
    # with a naive first-element pivot); average O(n log n).


# --- Controlling Python's built-in sort (what you actually use) ---
# sorted() returns a new list; list.sort() sorts in place. Both take `key`.

def sorting_with_key_demo():
    words = ["banana", "kiwi", "apple", "fig"]
    by_length = sorted(words, key=len)                  # sort by a computed value
    by_length_desc = sorted(words, key=len, reverse=True)

    people = [("alice", 30), ("bob", 25), ("carol", 30)]
    # Sort by age, then name -- return a TUPLE key for multi-level sorting.
    by_age_then_name = sorted(people, key=lambda p: (p[1], p[0]))

    return by_length, by_length_desc, by_age_then_name


# --- Custom comparator (when a simple key isn't enough) ---
# Sometimes ordering depends on a PAIRWISE comparison, not a per-item key.
# functools.cmp_to_key adapts an old-style comparator: return negative if a<b,
# positive if a>b, zero if equal. Classic use: arrange numbers to form the
# largest possible concatenated number ("3","30" -> "330" beats "303").
from functools import cmp_to_key

def largest_number(nums):
    strs = [str(n) for n in nums]

    def compare(a, b):
        if a + b > b + a:               # a should come first
            return -1
        elif a + b < b + a:
            return 1
        return 0

    strs.sort(key=cmp_to_key(compare))
    return "".join(strs)


if __name__ == "__main__":
    data = [5, 2, 9, 1, 5, 6, 3]
    print("=== From-scratch sorts ===")
    print(f"merge_sort({data}) = {merge_sort(data)}")
    print(f"quick_sort({data}) = {quick_sort(data)}")

    print("\n=== Built-in sort with key ===")
    by_len, by_len_desc, by_age_name = sorting_with_key_demo()
    print(f"by length:        {by_len}")
    print(f"by length (desc): {by_len_desc}")
    print(f"by age then name: {by_age_name}")

    print("\n=== Custom comparator ===")
    print(f"largest_number([3, 30, 34, 5, 9]) = {largest_number([3, 30, 34, 5, 9])}")  # 9534330

    print("\n=== In real code: just use sorted() / .sort() ===")
    # Timsort is stable, adaptive, and O(n log n). Don't hand-roll in production.
    print(sorted(data))
