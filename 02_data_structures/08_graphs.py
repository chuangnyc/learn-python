# Simple Graph

from collections import deque

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

# BFS explores level by level (all immediate neighbors first, then theirs),
# so the FIRST time it reaches the target it has used the fewest edges --
# making it the go-to for SHORTEST-path problems. The only structural change
# from DFS is the container: DFS dives deep via a stack (here, recursion's call
# stack); BFS goes wide via a QUEUE (FIFO), pulling the oldest path first.
def bfs(start, target):
    visited = {start}              # mark on ENQUEUE so a node is queued only once
    queue = deque([[start]])       # the queue holds whole PATHS, not bare nodes

    while queue:
        path = queue.popleft()     # popleft() = FIFO -- take the oldest path
        node = path[-1]            # the node we're currently standing on

        if node == target:         # first arrival == a shortest path
            return path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])  # extend path, enqueue it

    return None                    # target unreachable from start

# Example: Find a path from node A to node E with each strategy.
# DFS dives down the first neighbor; BFS fans out by distance -- so they can
# return DIFFERENT paths. BFS's is always shortest (fewest edges).
if __name__ == "__main__":
    dfs_path = dfs_recursive('A', 'E')
    print("DFS path from A to E:", dfs_path)  # ['A', 'B', 'D', 'E'] (4 nodes)

    bfs_path = bfs('A', 'E')
    print("BFS path from A to E:", bfs_path)  # ['A', 'C', 'E']      (3 nodes)
