# Stacks follow a LIFO (Last In First Out) order of operations.
# The last element added to the stack is the first element to be removed.
# -- Pratical Applications:
#    - Function call stack:
#      Each time a function is called, a new frame is pushed onto the stack, and when the function returns, the frame is popped off the stack.
#    - Undo mechanism in text editors
#    - Browser History
#    - Expression evaluation
#    - Backtracking algorithms
#    - Depth-First Search (DFS):
#      Stacks are used in graph algorithms like Depth-First Search (DFS) to keep track of the vertices to be explored.


# Stacks can be implemented using lists in Python.
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    # The push() method adds an element to the end of the list.
    def push(self, item):
        self.items.append(item)

    # The pop() method removes the last element from the list.
    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    # The peek() method returns the last element of the list without removing it.
    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def size(self):
        return len(self.items)
    
# Example usage:
if __name__ == "__main__":
    stack = Stack()
    stack.push(1)
    print(stack.peek())  # Output should be 1
    stack.push(2)
    print(stack.peek())  # Output should be 2
    stack.push(3)
    print(stack.peek())  # Output should be 3
    print(stack.pop())   # Output should be 3
    print(stack.pop())   # Output should be 2
    print(stack.pop())   # Output should be 1
    print(stack.is_empty())  # Output should be True
