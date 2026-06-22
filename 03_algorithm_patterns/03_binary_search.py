# Binary Search finds a target in SORTED data by repeatedly halving the search
# range: check the middle, then discard the half that can't contain the answer.
# O(log n) -- a billion elements in ~30 comparisons (see the binary-trees lesson).
# -- The precondition: the data must be SORTED (or, more generally, the
#    search space must be "monotonic" -- some property flips false->true once
#    and never flips back).
# -- When to reach for it:
#    "find X in sorted data", "first/last position of X", "smallest value that
#    satisfies a condition", "search on the answer" (e.g. min capacity, sqrt).
# Note: Python's `bisect` module is the production tool; we implement by hand
# first to understand the index bookkeeping (the classic source of off-by-one bugs).


# --- Classic binary search: is target present? ---
# Maintain a [low, high] inclusive range. Compare the midpoint; shrink toward
# the half that could hold the target. Return the index, or -1 if absent.
def binary_search(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:                  # inclusive range -> loop while low <= high
        mid = (low + high) // 2         # midpoint (integer division)
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1               # target is in the upper half
        else:
            high = mid - 1              # target is in the lower half
    return -1


# --- Search-insert position ---
# Where would target go to keep the list sorted? When the loop ends, `low` is
# exactly that insertion index -- a very common binary-search variant.
def search_insert(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return low                          # first index where nums[i] >= target


# --- Leftmost / rightmost occurrence (for duplicates) ---
# Plain binary search finds *a* match; to find the FIRST one, don't stop on a
# hit -- record it and keep searching the left half.
def find_first(nums, target):
    low, high = 0, len(nums) - 1
    result = -1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            result = mid                # candidate; keep looking left
            high = mid - 1
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return result


# --- "Binary search on the answer": integer square root ---
# The answer space (0..n) is monotonic: mid*mid <= n is true up to a point, then
# false forever. Binary-search that boundary -- no sorted array involved at all.
def int_sqrt(n):
    if n < 2:
        return n
    low, high = 1, n
    while low <= high:
        mid = (low + high) // 2
        if mid * mid <= n:
            low = mid + 1               # mid is a valid candidate; try larger
        else:
            high = mid - 1
    return high                         # largest value whose square is <= n


if __name__ == "__main__":
    nums = [1, 3, 5, 7, 9, 11]
    print("=== Classic search ===")
    print(f"binary_search({nums}, 7) = {binary_search(nums, 7)}")   # 3
    print(f"binary_search({nums}, 8) = {binary_search(nums, 8)}")   # -1

    print("\n=== Insert position ===")
    print(f"search_insert({nums}, 8) = {search_insert(nums, 8)}")   # 4
    print(f"search_insert({nums}, 0) = {search_insert(nums, 0)}")   # 0

    print("\n=== First occurrence (duplicates) ===")
    dups = [1, 2, 2, 2, 3, 4]
    print(f"find_first({dups}, 2) = {find_first(dups, 2)}")         # 1

    print("\n=== Search on the answer ===")
    print(f"int_sqrt(26) = {int_sqrt(26)}")                         # 5
    print(f"int_sqrt(1)  = {int_sqrt(1)}")                          # 1

    print("\n=== The real thing: bisect ===")
    import bisect
    # bisect_left finds the leftmost insertion point; bisect_right the rightmost.
    print(f"bisect_left([1,2,2,3], 2)  = {bisect.bisect_left([1, 2, 2, 3], 2)}")   # 1
    print(f"bisect_right([1,2,2,3], 2) = {bisect.bisect_right([1, 2, 2, 3], 2)}")  # 3
    # insort keeps a list sorted as you insert -- binary search + insert.
    sorted_list = [1, 3, 5]
    bisect.insort(sorted_list, 4)
    print(f"after insort 4: {sorted_list}")                         # [1, 3, 4, 5]
