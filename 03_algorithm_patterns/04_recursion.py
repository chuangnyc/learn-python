# Recursion solves a problem by having a function call ITSELF on a smaller
# subproblem, until it hits a BASE CASE that stops the recursion. Two parts are
# mandatory: (1) a base case (when to stop), (2) a recursive case that makes
# progress toward it. Miss the base case and you get infinite recursion ->
# RecursionError (Python caps the call-stack depth, ~1000 by default).
# -- Backtracking is recursion that BUILDS UP a partial solution, explores each
#    choice, then UNDOES the choice ("backtracks") to try the next one. It's how
#    you enumerate subsets, permutations, combinations, and solve mazes/Sudoku.
# -- When to reach for it:
#    Tree/graph traversal (already seen), divide-and-conquer, and "generate all
#    possible ..." problems where you make a sequence of choices.


# --- Basic recursion: factorial ---
# n! = n * (n-1)!  with base case 0! = 1. Each call shrinks n toward 0.
def factorial(n):
    if n <= 1:                  # base case
        return 1
    return n * factorial(n - 1)  # recursive case: smaller subproblem


# --- Basic recursion: Fibonacci (naive) ---
# Elegant but EXPONENTIAL (O(2^n)) -- it recomputes the same values endlessly.
# The dynamic-programming lesson fixes this with memoization. Shown here to
# make the cost of naive recursion concrete.
def fib(n):
    if n < 2:                   # base cases: fib(0)=0, fib(1)=1
        return n
    return fib(n - 1) + fib(n - 2)


# --- Backtracking: all subsets (the power set) ---
# At each index you make a binary choice: include this element or not. The call
# tree explores both branches. There are 2^n subsets, so this is O(2^n) -- which
# is inherent to the problem (that many subsets exist), not wasteful like fib.
def subsets(nums):
    result = []

    def backtrack(start, current):
        result.append(list(current))   # record a COPY of the current subset
        for i in range(start, len(nums)):
            current.append(nums[i])     # choose nums[i]
            backtrack(i + 1, current)   # explore with it included
            current.pop()               # UNDO the choice (backtrack)

    backtrack(0, [])
    return result


# --- Backtracking: all permutations ---
# Build an ordering one element at a time; `used` tracks what's already placed.
# When the current permutation is full, record it. n! permutations -> O(n!).
def permutations(nums):
    result = []
    used = [False] * len(nums)

    def backtrack(current):
        if len(current) == len(nums):   # base case: a full permutation
            result.append(list(current))
            return
        for i in range(len(nums)):
            if used[i]:
                continue                # skip elements already in `current`
            used[i] = True
            current.append(nums[i])     # choose
            backtrack(current)          # explore
            current.pop()               # undo
            used[i] = False             # undo

    backtrack([])
    return result


# --- Backtracking: combinations (choose k of n) ---
# Like subsets, but only record paths of exactly length k. The `start` index
# prevents reusing earlier elements, so order doesn't matter (C(n,k)).
def combinations(n, k):
    result = []

    def backtrack(start, current):
        if len(current) == k:           # base case: picked k items
            result.append(list(current))
            return
        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()

    backtrack(1, [])
    return result


if __name__ == "__main__":
    print("=== Basic recursion ===")
    print(f"factorial(5) = {factorial(5)}")     # 120
    print(f"fib(10) = {fib(10)}")               # 55 (but recomputes a LOT)

    print("\n=== Backtracking: subsets ===")
    print(f"subsets([1,2,3]) = {subsets([1, 2, 3])}")
    # [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]  -- all 2^3 = 8

    print("\n=== Backtracking: permutations ===")
    print(f"permutations([1,2,3]) = {permutations([1, 2, 3])}")
    # 3! = 6 orderings

    print("\n=== Backtracking: combinations ===")
    print(f"combinations(n=4, k=2) = {combinations(4, 2)}")
    # C(4,2) = 6: [1,2],[1,3],[1,4],[2,3],[2,4],[3,4]

    print("\n=== The choose / explore / undo skeleton ===")
    # Every backtracking function above is the same three steps in a loop:
    #   choose an option -> recurse to explore it -> UNDO it and try the next.
    # That undo (the pop / resetting `used`) is what makes it "backtracking."
