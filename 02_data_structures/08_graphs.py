# Simple Graph

# Representing the graph as an adjacency list
#     A
#    / \
#   B   C
#    \ / \
#     D - E

graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D', 'E'],
    'D': ['E'],
    'E': []
}

# Recursive DFS function to find the target
def dfs_recursive(node, target, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    # Mark the current node as visited and add it to the path
    visited.add(node)
    path.append(node)

    # If we reach the target node, return the path
    if node == target:
        return path

    # Recur for all the neighbors of the current node
    for neighbor in graph[node]:
        if neighbor not in visited:
            result = dfs_recursive(neighbor, target, visited, path)
            if result:  # If the target is found, stop recursion
                return result

    # Backtrack if no path is found from this node
    path.pop()
    return None

# Example: Find a path from node A to node E
if __name__ == "__main__":
    path = dfs_recursive('A', 'E')
    print("Path from A to E:", path)
