# Queue uses FIFO (First In First Out) ordering. That is, the first element added to the queue is the first one to be removed.
# -- Practical Applications:
#    - Task scheduling
#      Operating systems use queues to manage tasks and processes, 
#      scheduling them for execution based on priority and availability of resources.
#    - Breadth-First Search (BFS):
#      Queues are used in graph algorithms like Breadth-First Search (BFS) to keep track of the vertices to be explored.
#    - Load balancing
#      Queues are used in load balancing to distribute tasks evenly across multiple servers or processors.

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    # The enqueue() method adds an element to the end of the list.
    def enqueue(self, item):
        self.items.append(item)

    # The dequeue() method removes the first element from the list.
    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.pop(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self.items[0]

    def size(self):
        return len(self.items)

# Example usage:
if __name__ == "__main__":
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    print(queue.dequeue())  # Output: 1
    print(queue.peek())     # Output: 2
    print(queue.size())     # Output: 2
    print(queue.is_empty()) # Output: False
    print(queue.dequeue())  # Output: 2
    print(queue.peek())     # Output: 3