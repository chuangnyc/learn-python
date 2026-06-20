# A Linked List stores elements in NODES, each holding a value and a reference
# to the next node. Unlike a Python list (a contiguous dynamic array), the
# elements are scattered in memory and chained by pointers.
# -- Trade-offs vs a Python list / Go slice:
#    - O(1) insert/delete at the front (no shifting); arrays are O(n) there
#    - O(n) random access by index (must walk the chain); arrays are O(1)
#    - No "capacity" or resizing; each node is allocated as needed
# -- Practical Applications:
#    - Implementing stacks and queues
#    - LRU caches (doubly linked list + hash map)
#    - Adjacency lists for graphs
#    - Undo/redo histories
# Note: In real Python code you almost always just use a list or collections.deque.
# We implement from scratch here to understand how pointers/references work.
# (Go has explicit pointers; in Python every variable is already a reference to
# an object, so `self.next = other_node` IS the pointer.)


# --- Singly Linked List ---
# Each node points only forward, to the next node. The list tracks the head.

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None        # reference to the next Node (None = end)

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def is_empty(self):
        return self.head is None

    # O(1): insert at the front by pointing the new node at the old head.
    def prepend(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node
        self._size += 1

    # O(n): walk to the end, then link the new node.
    def append(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self._size += 1

    # O(n): unlink the first node whose value matches.
    def delete(self, value):
        current = self.head
        previous = None
        while current is not None:
            if current.value == value:
                if previous is None:        # deleting the head
                    self.head = current.next
                else:
                    previous.next = current.next  # skip over current
                self._size -= 1
                return True
            previous = current
            current = current.next
        return False

    def find(self, value):
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    # O(n) in-place reversal: flip every node's `next` pointer.
    # Classic interview question -- track three pointers as you walk.
    def reverse(self):
        previous = None
        current = self.head
        while current is not None:
            nxt = current.next      # remember the rest of the list
            current.next = previous  # flip the pointer
            previous = current       # advance the two trailing pointers
            current = nxt
        self.head = previous

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def __len__(self):
        return self._size


# --- Doubly Linked List ---
# Each node points BOTH forward (next) and backward (prev). Tracking a tail
# pointer too makes append and pop-from-end O(1) -- the basis of deque/LRU.

class DNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    # O(1): append at the tail using the tail pointer (no walk needed).
    def append(self, value):
        node = DNode(value)
        if self.tail is None:           # empty list
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    # O(1): prepend at the head.
    def prepend(self, value):
        node = DNode(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1

    # O(1): remove and return the last value (the prev pointer makes this cheap;
    # a singly linked list would need an O(n) walk to find the new tail).
    def pop(self):
        if self.tail is None:
            raise IndexError("pop from empty list")
        node = self.tail
        if node.prev is None:           # only one element
            self.head = self.tail = None
        else:
            self.tail = node.prev
            self.tail.next = None
        self._size -= 1
        return node.value

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    # Walking backward is only possible because of the prev pointers.
    def to_list_reversed(self):
        result = []
        current = self.tail
        while current is not None:
            result.append(current.value)
            current = current.prev
        return result

    def __len__(self):
        return self._size


# --- Cycle Detection (Floyd's Tortoise and Hare) ---
# A linked list has a cycle if some node's `next` eventually points back to an
# earlier node, so a naive traversal loops forever. Floyd's algorithm uses two
# pointers moving at different speeds: if there's a cycle, the fast pointer
# eventually laps and meets the slow one. O(n) time, O(1) space.

def has_cycle(head):
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next           # moves 1 step
        fast = fast.next.next      # moves 2 steps
        if slow is fast:           # `is` -- same node object, not equal value
            return True
    return False                   # fast reached the end -> no cycle


if __name__ == "__main__":
    print("=== Singly Linked List ===")
    sll = SinglyLinkedList()
    sll.append(1)
    sll.append(2)
    sll.append(3)
    sll.prepend(0)
    print(f"list: {sll.to_list()}, len: {len(sll)}")   # [0, 1, 2, 3], 4
    print(f"find(2): {sll.find(2)}, find(9): {sll.find(9)}")
    sll.delete(2)
    print(f"after delete(2): {sll.to_list()}")          # [0, 1, 3]
    sll.reverse()
    print(f"reversed: {sll.to_list()}")                 # [3, 1, 0]

    print("\n=== Doubly Linked List ===")
    dll = DoublyLinkedList()
    dll.append("a")
    dll.append("b")
    dll.prepend("start")
    print(f"forward:  {dll.to_list()}")                 # ['start', 'a', 'b']
    print(f"backward: {dll.to_list_reversed()}")        # ['b', 'a', 'start']
    print(f"pop(): {dll.pop()}, now: {dll.to_list()}")  # b, ['start', 'a']

    print("\n=== Cycle Detection ===")
    # Build a small chain a -> b -> c manually.
    a, b, c = Node("a"), Node("b"), Node("c")
    a.next, b.next = b, c
    print(f"a->b->c has cycle? {has_cycle(a)}")         # False
    c.next = a                                          # close the loop: c -> a
    print(f"after c->a, has cycle? {has_cycle(a)}")     # True
