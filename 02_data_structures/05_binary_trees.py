# Tree data structure:
# - A tree is a non-linear data structure.
# - It is a collection of nodes connected by edges.
# - A tree has a root node and zero or more sub-trees.
# - A tree is a recursive data structure.
# - The topmost node is called the root of the tree.
# - The elements that are directly under an element are called its children.

# Binary Tree:
# - A binary tree is a tree in which each node has at most two children.
# - The children are referred to as the left child and the right child.
# - A binary tree is a recursive data structure.
# - A binary tree can be empty.

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key

class BinaryTree:
    def __init__(self):
        self.root = None

    # The insert() method inserts a new node into the binary tree.
    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert(self.root, key)

    # The _insert() method is a helper method that recursively inserts a new node into the binary tree.
    def _insert(self, node, key):
        if key < node.value:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert(node.right, key)

    # The inorder_traversal() method performs an inorder traversal of the binary tree.
    # In inorder traversal, the nodes are recursively visited in this order: left, root, right.
    def inorder_traversal(self, node, result):
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.value)
            self.inorder_traversal(node.right, result)

    # Preorder traversal is a method of traversing a binary tree in which the nodes are visited in the following order: 
    # root node, left subtree, and then right subtree. 
    # This traversal method is useful for creating a copy of the tree or for prefix notation of expressions.
    def preorder_traversal(self, node, result):
        if node:
            result.append(node.value)
            self.preorder_traversal(node.left, result)
            self.preorder_traversal(node.right, result)

    # Postorder traversal is a method of traversing a binary tree in which the nodes are visited in the following order: 
    # left subtree, right subtree, and then root node. 
    # This traversal method is useful for deleting a tree or evaluating postfix expressions.
    def postorder_traversal(self, node, result):
        if node:
            self.postorder_traversal(node.left, result)
            self.postorder_traversal(node.right, result)
            result.append(node.value)


# --Example usage--
# Tree should look like this:
#     10
#    /  \
#   5    20
#  / \   / \
# 3   7 15  25
if __name__ == "__main__":
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(20)
    tree.insert(3)
    tree.insert(7)
    tree.insert(15)
    tree.insert(25)

    inorder_result = []
    tree.inorder_traversal(tree.root, inorder_result)
    print("Inorder Traversal:", inorder_result)  # Output: [3, 5, 7, 10, 15, 20, 25]

    preorder_result = []
    tree.preorder_traversal(tree.root, preorder_result)
    print("Preorder Traversal:", preorder_result)  # Output: [10, 5, 3, 7, 20, 15, 25]

    postorder_result = []
    tree.postorder_traversal(tree.root, postorder_result)
    print("Postorder Traversal:", postorder_result)  # Output: [3, 7, 5, 15, 25, 20, 10]