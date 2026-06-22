# A Greedy algorithm builds a solution by always making the choice that looks
# best RIGHT NOW, never reconsidering. When the problem has the "greedy choice
# property" (a locally optimal choice leads to a globally optimal solution),
# this is simpler and faster than dynamic programming.
# -- The catch: greedy is only correct for SOME problems. You must prove (or
#    know) that the local choice is safe. When it isn't, greedy gives a
#    plausible-but-wrong answer -- which is exactly the coin_change trap from
#    the DP lesson. Knowing WHEN greedy works is the real skill.
# -- When it tends to work:
#    Interval scheduling, Huffman coding, minimum spanning trees, and many
#    "sort, then sweep once" problems.


# --- Interval scheduling: max non-overlapping meetings ---
# Pick the most meetings that don't overlap. GREEDY CHOICE: always take the
# meeting that ENDS earliest -- it leaves the most room for the rest. Sort by
# end time, then sweep. O(n log n) for the sort, O(n) sweep. Provably optimal.
def max_meetings(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])  # sort by END time -- the key insight
    count = 1
    last_end = intervals[0][1]
    for start, end in intervals[1:]:
        if start >= last_end:           # doesn't overlap the last one we kept
            count += 1
            last_end = end
    return count


# --- Merge overlapping intervals ---
# Sort by START, then sweep: extend the current interval if the next overlaps,
# otherwise close it off and start a new one. O(n log n).
def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])  # sort by START time
    merged = [list(intervals[0])]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:      # overlaps the current merged interval
            merged[-1][1] = max(merged[-1][1], end)   # extend its end
        else:
            merged.append([start, end])  # gap -> start a fresh interval
    return merged


# --- Jump game: can you reach the last index? ---
# nums[i] = max jump length from i. GREEDY: track the FARTHEST index reachable
# so far; if you ever stand on an index beyond that reach, you're stuck. O(n).
def can_jump(nums):
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:                # can't even get to i
            return False
        farthest = max(farthest, i + jump)
    return True


# --- Where greedy FAILS (the cautionary example) ---
# "Use the largest coin that fits" feels right but is wrong for some coin sets.
# This greedy version disagrees with the DP-correct coin_change from lesson 06.
def coin_change_greedy(coins, amount):
    coins = sorted(coins, reverse=True)
    count = 0
    for coin in coins:
        while amount >= coin:
            amount -= coin
            count += 1
    return count if amount == 0 else -1
    # For coins [1, 3, 4] making 6: greedy takes 4, then 1, 1 -> 3 coins.
    # The optimal (DP) answer is 3 + 3 -> 2 coins. Greedy is locally sensible,
    # globally wrong. This is the canonical "know when greedy is unsafe" lesson.


if __name__ == "__main__":
    print("=== Interval scheduling (greedy IS optimal) ===")
    meetings = [(1, 3), (2, 5), (4, 7), (1, 8), (5, 9), (8, 10)]
    print(f"max_meetings = {max_meetings(meetings)}")   # 3 e.g. (1,3),(4,7),(8,10)

    print("\n=== Merge intervals ===")
    print(f"merge_intervals = {merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)])}")
    # [[1, 6], [8, 10], [15, 18]]

    print("\n=== Jump game ===")
    print(f"can_jump([2,3,1,1,4]) = {can_jump([2, 3, 1, 1, 4])}")  # True
    print(f"can_jump([3,2,1,0,4]) = {can_jump([3, 2, 1, 0, 4])}")  # False (stuck at index 3)

    print("\n=== Greedy gone wrong ===")
    greedy = coin_change_greedy([1, 3, 4], 6)
    print(f"coin_change_greedy([1,3,4], 6) = {greedy}  (WRONG: should be 2)")
    print("Greedy chose 4+1+1=3 coins; DP finds 3+3=2. Greedy isn't always safe.")
