# The Sliding Window pattern maintains a "window" (a contiguous range) over a
# sequence and slides it along, reusing work from the previous position instead
# of recomputing from scratch. It turns many O(n*k) or O(n^2) subarray/substring
# problems into a single O(n) pass.
# -- Two shapes:
#    1. FIXED window: the window is always size k. Slide by adding the new
#       element and removing the one that fell off the back.
#    2. VARIABLE window: two pointers (start, end) grow and shrink the window
#       to satisfy a condition (e.g. "no repeats", "sum >= target").
# -- When to reach for it:
#    "longest/shortest/max/min subarray or substring that satisfies X" over
#    CONTIGUOUS elements. (For non-contiguous subsets, that's a different tool.)
# It's really a specialized two-pointer technique -- the pointers bound a window.


# --- Fixed window: max sum of any k consecutive elements ---
# Brute force recomputes each window's sum in O(k) -> O(n*k). Instead, slide:
# subtract the element leaving the window, add the one entering. O(n).
def max_sum_subarray(nums, k):
    if len(nums) < k:
        return None
    window_sum = sum(nums[:k])          # sum the first window once
    best = window_sum
    for end in range(k, len(nums)):
        window_sum += nums[end] - nums[end - k]   # add new, drop old: O(1) update
        best = max(best, window_sum)
    return best


# --- Variable window: longest substring with no repeating characters ---
# Grow `end` to extend the window; when a duplicate appears, shrink from
# `start` until the window is valid again. Each char enters/leaves once -> O(n).
def longest_unique_substring(s):
    seen = {}                           # char -> last index it was seen at
    start = 0
    longest = 0
    for end, char in enumerate(s):
        # If we've seen this char inside the current window, jump start past it.
        if char in seen and seen[char] >= start:
            start = seen[char] + 1
        seen[char] = end
        longest = max(longest, end - start + 1)
    return longest


# --- Variable window: shortest subarray with sum >= target ---
# Grow the window until the sum is big enough, then shrink from the left as far
# as possible while still valid, tracking the smallest length seen. O(n).
def min_subarray_len(nums, target):
    start = 0
    window_sum = 0
    best = float("inf")                 # "infinity" sentinel for "not found yet"
    for end in range(len(nums)):
        window_sum += nums[end]         # grow the window
        while window_sum >= target:     # shrink while still valid
            best = min(best, end - start + 1)
            window_sum -= nums[start]
            start += 1
    return best if best != float("inf") else 0


# --- Variable window: longest substring with at most K distinct characters ---
# A dict counts chars in the window; when distinct count exceeds K, shrink left.
def longest_k_distinct(s, k):
    counts = {}
    start = 0
    longest = 0
    for end, char in enumerate(s):
        counts[char] = counts.get(char, 0) + 1
        while len(counts) > k:          # too many distinct -> shrink
            counts[s[start]] -= 1
            if counts[s[start]] == 0:
                del counts[s[start]]    # drop chars that left the window
            start += 1
        longest = max(longest, end - start + 1)
    return longest


if __name__ == "__main__":
    print("=== Fixed window ===")
    print(f"max_sum_subarray([2,1,5,1,3,2], k=3) = {max_sum_subarray([2, 1, 5, 1, 3, 2], 3)}")  # 9 (5+1+3)

    print("\n=== Variable window ===")
    print(f"longest_unique_substring('abcabcbb') = {longest_unique_substring('abcabcbb')}")  # 3 ('abc')
    print(f"longest_unique_substring('bbbbb')    = {longest_unique_substring('bbbbb')}")     # 1
    print(f"min_subarray_len([2,3,1,2,4,3], 7)   = {min_subarray_len([2, 3, 1, 2, 4, 3], 7)}")  # 2 ([4,3])
    print(f"min_subarray_len([1,1,1], 7)         = {min_subarray_len([1, 1, 1], 7)}")        # 0 (impossible)
    print(f"longest_k_distinct('eceba', k=2)     = {longest_k_distinct('eceba', 2)}")        # 3 ('ece')
