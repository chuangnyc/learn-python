# The Two Pointers pattern uses two index variables that walk through a
# sequence, instead of nested loops. It turns many O(n^2) brute-force scans
# into a single O(n) pass with O(1) extra space.
# -- Two common shapes:
#    1. OPPOSITE ENDS: one pointer at the start, one at the end, moving toward
#       each other. Works on SORTED data or symmetric checks (palindromes).
#    2. SAME DIRECTION: both start at the front; a "slow" pointer trails a
#       "fast" pointer. Good for in-place filtering / partitioning.
# -- When to reach for it:
#    "Find a pair/triplet", "is it a palindrome", "remove/dedupe in place",
#    "reverse in place" -- especially when the input is sorted.


# --- Opposite ends: two-sum on a SORTED array ---
# Find two numbers that add to target. Brute force checks all pairs O(n^2).
# With sorted input: if the current pair is too small, move the LEFT pointer
# right (increase the sum); if too big, move RIGHT left (decrease it). Each
# step eliminates a number, so it's a single O(n) sweep.
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return (left, right)
        elif total < target:
            left += 1           # need a bigger sum -> raise the low end
        else:
            right -= 1          # need a smaller sum -> lower the high end
    return None


# --- Opposite ends: palindrome check ---
# Compare characters from both ends inward; mismatch anywhere -> not a palindrome.
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


# --- Opposite ends: reverse a list in place ---
# Swap the ends and walk inward. O(n) time, O(1) space (no new list).
def reverse_in_place(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]   # tuple swap
        left += 1
        right -= 1
    return nums


# --- Same direction: remove duplicates from a SORTED list in place ---
# `slow` marks the end of the deduped region; `fast` scans ahead. When fast
# finds a new value, write it just past slow. Classic interview question.
def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0                    # last unique index
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]   # overwrite the next slot with the new value
    return slow + 1             # length of the deduped prefix


# --- Same direction: move all zeros to the end, keep order ---
# `slow` points at the next slot for a non-zero value.
def move_zeros(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
    return nums


if __name__ == "__main__":
    print("=== Opposite ends ===")
    print(f"two_sum_sorted([1,2,4,7,11], 15) = {two_sum_sorted([1, 2, 4, 7, 11], 15)}")  # (2, 4): 4+11
    print(f"two_sum_sorted([1,2,3], 7) = {two_sum_sorted([1, 2, 3], 7)}")                # None
    print(f"is_palindrome('racecar') = {is_palindrome('racecar')}")  # True
    print(f"is_palindrome('hello')   = {is_palindrome('hello')}")    # False
    print(f"reverse_in_place([1,2,3,4,5]) = {reverse_in_place([1, 2, 3, 4, 5])}")  # [5,4,3,2,1]

    print("\n=== Same direction ===")
    arr = [1, 1, 2, 2, 2, 3, 4, 4]
    n = remove_duplicates(arr)
    print(f"remove_duplicates -> length {n}, prefix {arr[:n]}")   # 4, [1, 2, 3, 4]
    print(f"move_zeros([0,1,0,3,12]) = {move_zeros([0, 1, 0, 3, 12])}")  # [1, 3, 12, 0, 0]
