# Dynamic Programming (DP) solves problems that have (1) OVERLAPPING
# SUBPROBLEMS -- the same smaller problem is solved repeatedly -- and (2)
# OPTIMAL SUBSTRUCTURE -- the best answer is built from best answers to
# subproblems. The fix for the repeated work is to STORE each subproblem's
# answer and reuse it. That turns exponential recursion into polynomial time.
# -- Two styles (same idea, opposite directions):
#    - MEMOIZATION (top-down): ordinary recursion + a cache. Solve on demand,
#      remember results. Easy to write from a recursive formula.
#    - TABULATION (bottom-up): fill a table from the smallest subproblems up.
#      No recursion/stack; often more space-efficient.
# -- When to reach for it:
#    "count the ways", "min/max cost", "longest/shortest", "can we reach X" --
#    where greedy doesn't work and brute-force recursion recomputes subproblems.


# --- The motivating example: Fibonacci ---
# Naive recursion is O(2^n) because fib(n-2) etc. are recomputed many times
# (see the recursion lesson). DP collapses it to O(n).

# Memoization (top-down): cache results in a dict.
def fib_memo(n, cache=None):
    if cache is None:
        cache = {}
    if n < 2:
        return n
    if n in cache:                      # already solved -> reuse
        return cache[n]
    cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]

# Tabulation (bottom-up): build an array from fib(0) upward.
def fib_tab(n):
    if n < 2:
        return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]   # each entry from earlier ones
    return table[n]

# The idiomatic Python shortcut: functools.lru_cache memoizes for you (lesson 09).
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n):
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)


# --- Climbing stairs: how many ways to climb n steps taking 1 or 2 at a time? ---
# Ways(n) = Ways(n-1) + Ways(n-2) -- it's Fibonacci in disguise. We only need the
# last two values, so O(n) time and O(1) space.
def climb_stairs(n):
    if n <= 2:
        return n
    prev, curr = 1, 2                   # ways to climb 1 step, 2 steps
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr  # slide the window of two
    return curr


# --- Coin change: fewest coins to make `amount` (classic DP, greedy FAILS) ---
# dp[a] = min coins to make amount a. Build the table from 0 up; for each amount
# try every coin and take the best. O(amount * len(coins)).
def coin_change(coins, amount):
    INF = amount + 1                    # sentinel "impossible" (more than any real answer)
    dp = [0] + [INF] * amount           # dp[0] = 0 coins to make 0
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != INF else -1
    # Note: a greedy "take the biggest coin" approach gives wrong answers for
    # coin sets like [1, 3, 4] making 6 (greedy: 4+1+1=3 coins; optimal: 3+3=2).


# --- Longest Common Subsequence (LCS): a 2D DP staple ---
# Length of the longest sequence appearing (in order, not necessarily contiguous)
# in both strings. dp[i][j] = LCS of a[:i] and b[:j]. O(len(a) * len(b)).
def lcs(a, b):
    rows, cols = len(a) + 1, len(b) + 1
    dp = [[0] * cols for _ in range(rows)]   # (len(a)+1) x (len(b)+1) grid of 0s
    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:          # chars match -> extend the diagonal
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:                             # else carry the best neighbor
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[len(a)][len(b)]


if __name__ == "__main__":
    print("=== Fibonacci, three ways (all O(n) now) ===")
    print(f"fib_memo(30)   = {fib_memo(30)}")     # 832040
    print(f"fib_tab(30)    = {fib_tab(30)}")      # 832040
    print(f"fib_cached(30) = {fib_cached(30)}")   # 832040
    print(f"cache stats:   {fib_cached.cache_info()}")

    print("\n=== Climbing stairs ===")
    print(f"climb_stairs(5) = {climb_stairs(5)}")  # 8

    print("\n=== Coin change (greedy would fail) ===")
    print(f"coin_change([1,3,4], 6)   = {coin_change([1, 3, 4], 6)}")    # 2 (3+3)
    print(f"coin_change([2], 3)       = {coin_change([2], 3)}")          # -1 (impossible)
    print(f"coin_change([1,2,5], 11)  = {coin_change([1, 2, 5], 11)}")   # 3 (5+5+1)

    print("\n=== Longest Common Subsequence ===")
    print(f"lcs('abcde', 'ace') = {lcs('abcde', 'ace')}")   # 3 ('ace')
    print(f"lcs('abc', 'xyz')   = {lcs('abc', 'xyz')}")     # 0
