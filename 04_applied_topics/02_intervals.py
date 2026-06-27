# Interval problems work on pairs [start, end] and almost always begin the
# same way: SORT by start, then sweep left to right deciding whether the
# current interval overlaps the previous one.
# -- The overlap test for [a, b] and [c, d] (after sorting by start) is just
#    c <= b: the next interval begins before the previous one ends.
# -- Python notes for a Go dev:
#    1. sorted(...) with a key lambda replaces sort.Slice; intervals are plain
#       lists, no struct needed.
#    2. Tuple/list unpacking (start, end = interval) reads cleanly vs indexing.
#    3. There's no generics ceremony -- the same code handles any numbers.


# --- Merge overlapping intervals ---
# Sort by start, then either extend the last merged interval's end (overlap)
# or append a fresh interval (gap). Classic O(n log n) from the sort.
def merge(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda iv: iv[0])
    merged = [intervals[0][:]]          # copy so we don't mutate the input
    for start, end in intervals[1:]:
        last = merged[-1]
        if start <= last[1]:            # overlap -> stretch the end outward
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])  # disjoint -> start a new block
    return merged


# --- Insert a new interval into a sorted, non-overlapping list ---
# Three phases: intervals strictly before the new one, the block that overlaps
# (merge them all), then everything strictly after. O(n), single pass.
def insert(intervals, new):
    result = []
    i, n = 0, len(intervals)
    new = new[:]                        # local copy we can widen

    while i < n and intervals[i][1] < new[0]:   # ends before new starts
        result.append(intervals[i])
        i += 1

    while i < n and intervals[i][0] <= new[1]:  # overlaps new
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    result.append(new)

    while i < n:                        # remainder, all after new
        result.append(intervals[i])
        i += 1
    return result


# --- Can a person attend all meetings? ---
# Sort by start; if any meeting begins before the previous one ends, conflict.
def can_attend_all(meetings):
    meetings = sorted(meetings, key=lambda iv: iv[0])
    for prev, curr in zip(meetings, meetings[1:]):
        if curr[0] < prev[1]:           # starts before prev ends -> overlap
            return False
    return True


# --- Minimum meeting rooms required ---
# Separate the start and end times, sort each, and sweep with two pointers.
# Every start before the next end needs a new room; each end frees one.
# This is the "chronological sweep" trick -- track concurrent overlaps.
def min_meeting_rooms(meetings):
    if not meetings:
        return 0
    starts = sorted(iv[0] for iv in meetings)
    ends = sorted(iv[1] for iv in meetings)
    rooms = 0
    most = 0
    s = e = 0
    while s < len(starts):
        if starts[s] < ends[e]:
            rooms += 1                  # a meeting starts before one ends
            s += 1
            most = max(most, rooms)
        else:
            rooms -= 1                  # a meeting ended, free its room
            e += 1
    return most


if __name__ == "__main__":
    print("=== Merge ===")
    print(f"merge([[1,3],[2,6],[8,10],[15,18]]) = "
          f"{merge([[1, 3], [2, 6], [8, 10], [15, 18]])}")  # [[1,6],[8,10],[15,18]]
    print(f"merge([[1,4],[4,5]]) = {merge([[1, 4], [4, 5]])}")  # [[1,5]]

    print("\n=== Insert ===")
    print(f"insert([[1,3],[6,9]], [2,5]) = {insert([[1, 3], [6, 9]], [2, 5])}")  # [[1,5],[6,9]]
    print(f"insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8]) = "
          f"{insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8])}")      # [[1,2],[3,10],[12,16]]

    print("\n=== Scheduling ===")
    print(f"can_attend_all([[0,30],[5,10],[15,20]]) = "
          f"{can_attend_all([[0, 30], [5, 10], [15, 20]])}")  # False
    print(f"can_attend_all([[7,10],[2,4]]) = {can_attend_all([[7, 10], [2, 4]])}")  # True
    print(f"min_meeting_rooms([[0,30],[5,10],[15,20]]) = "
          f"{min_meeting_rooms([[0, 30], [5, 10], [15, 20]])}")  # 2
