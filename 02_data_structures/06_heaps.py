# A Heap is a binary tree (stored compactly in an array) that keeps the
# smallest (min-heap) or largest (max-heap) element instantly accessible at
# the root. It does NOT keep everything sorted -- just enough order to always
# know the min/max. That partial order is what makes it fast.
# -- Cost profile:
#    - peek min/max:  O(1)   (it's always at index 0)
#    - push:          O(log n)
#    - pop min/max:   O(log n)
#    Compare: a sorted list gives O(1) peek but O(n) insert; an unsorted list
#    gives O(1) insert but O(n) to find the min. A heap balances both.
# -- Practical Applications:
#    - Priority queues (process the most urgent item next)
#    - Dijkstra's shortest-path, Prim's MST
#    - "Top K" / "K largest" problems, streaming medians
#    - Task schedulers, event simulation
# Note: Python ships heapq (a min-heap over a list); Go has container/heap.
# We build one from scratch to see the sift-up / sift-down mechanics.


# --- Array representation of a binary tree ---
# A complete binary tree maps onto an array with simple index arithmetic --
# no node objects or pointers needed:
#     parent(i)      = (i - 1) // 2
#     left_child(i)  = 2*i + 1
#     right_child(i) = 2*i + 2
# The heap invariant (min-heap): every parent <= its children. So the global
# minimum is always at index 0, but siblings are NOT ordered relative to
# each other -- that's why a heap is "partially ordered," not sorted.

class MinHeap:
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def peek(self):
        if not self.data:
            raise IndexError("peek from empty heap")
        return self.data[0]             # O(1): the min is always the root

    # Push: append at the end, then "sift up" -- swap with the parent while
    # it's smaller, bubbling the new value up to its correct level. O(log n)
    # because the tree height is log n.
    def push(self, value):
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2 # // is integer division
            if self.data[i] < self.data[parent]:
                self.data[i], self.data[parent] = self.data[parent], self.data[i]
                i = parent              # keep climbing
            else:
                break                   # parent <= child -> invariant restored

    # Pop: the root is the min. Move the LAST element to the root to keep the
    # tree complete, then "sift down" -- swap with the smaller child while it's
    # bigger, sinking it to its correct level. O(log n).
    def pop(self):
        if not self.data:
            raise IndexError("pop from empty heap")
        root = self.data[0]
        last = self.data.pop()          # remove the final element
        if self.data:                   # if anything remains, reseat it at root
            self.data[0] = last
            self._sift_down(0)
        return root

    def _sift_down(self, i):
        n = len(self.data)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and self.data[left] < self.data[smallest]:
                smallest = left
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right
            if smallest == i:           # parent <= both children -> done
                break
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            i = smallest                # keep sinking


# --- heapsort: a heap gives sorting almost for free ---
# Push everything, then pop repeatedly -- each pop yields the next smallest.
# n pushes + n pops, each O(log n), so O(n log n) overall.
def heapsort(values):
    h = MinHeap()
    for v in values:
        h.push(v)
    return [h.pop() for _ in range(len(h))]


if __name__ == "__main__":
    print("=== MinHeap (from scratch) ===")
    h = MinHeap()
    for v in [5, 3, 8, 1, 9, 2]:
        h.push(v)
    print(f"min (peek): {h.peek()}")                 # 1
    print(f"internal array: {h.data}")               # partially ordered, not sorted
    popped = [h.pop() for _ in range(len(h))]
    print(f"popped in order: {popped}")              # [1, 2, 3, 5, 8, 9] -- sorted out

    print("\n=== heapsort ===")
    print(heapsort([5, 3, 8, 1, 9, 2, 7]))           # [1, 2, 3, 5, 7, 8, 9]

    print("\n=== Priority queue use case ===")
    # Tuples compare element-by-element, so (priority, task) heaps by priority.
    tasks = MinHeap()
    for item in [(2, "email"), (1, "page on-call"), (3, "tidy logs")]:
        tasks.push(item)
    print("processing by priority:")
    while len(tasks):
        priority, name = tasks.pop()
        print(f"  [{priority}] {name}")              # page on-call, email, tidy logs

    print("\n=== The real thing: heapq ===")
    import heapq
    # heapq operates on a plain list in place -- same min-heap, written in C.
    nums = [5, 3, 8, 1, 9, 2]
    heapq.heapify(nums)                              # O(n) build
    print(f"heapq smallest: {nums[0]}")             # 1
    print(f"3 smallest: {heapq.nsmallest(3, [5, 3, 8, 1, 9, 2])}")  # [1, 2, 3]
