# Topological Sort orders the nodes of a DIRECTED ACYCLIC GRAPH (DAG) so that
# every edge points "forward" -- if A must come before B (edge A -> B), then A
# appears before B in the ordering. It answers "in what order can I do these
# tasks given their dependencies?"
# -- Precondition: the graph must be a DAG. If there's a CYCLE (A needs B needs
#    A), no valid order exists -- detecting that is part of the job.
# -- Two standard algorithms (both O(V + E) -- vertices + edges):
#    1. KAHN'S (BFS): repeatedly remove nodes with no remaining dependencies.
#    2. DFS-based: post-order DFS, then reverse.
# -- Practical Applications:
#    - Build systems / task schedulers (compile order)
#    - Package/dependency resolution (pip, npm, apt)
#    - Course prerequisites, spreadsheet cell recalculation
# Builds directly on the graphs lesson (adjacency list, BFS, DFS, visited sets).


# --- Kahn's algorithm (BFS with in-degree counting) ---
# in-degree(node) = how many edges point AT it = how many unmet prerequisites.
# Start with all zero-in-degree nodes (no prerequisites). Remove one, "complete"
# it by decrementing its neighbors' in-degrees; any that hit zero are now ready.
# If we can't order every node, a cycle exists.
from collections import deque

def topo_sort_kahn(graph):
    # 1. Compute in-degrees. graph maps node -> list of nodes it points to.
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # 2. Seed the queue with everything that has no prerequisites.
    queue = deque([node for node in graph if in_degree[node] == 0])
    order = []

    # 3. Process: take a ready node, then "release" its dependents.
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1        # one prerequisite satisfied
            if in_degree[neighbor] == 0:    # all prerequisites met -> now ready
                queue.append(neighbor)

    # 4. If we ordered fewer than all nodes, the leftovers are stuck in a cycle.
    if len(order) != len(graph):
        return None                         # cycle detected -> no valid ordering
    return order


# --- DFS-based topological sort ---
# Visit a node's dependents fully (recurse), THEN record the node. That post-
# order places dependents before the node, so reversing gives a valid order.
# A `visiting` set catches cycles (we re-enter a node still on the current path).
def topo_sort_dfs(graph):
    WHITE, GRAY, BLACK = 0, 1, 2            # unvisited, in-progress, done
    color = {node: WHITE for node in graph}
    order = []
    has_cycle = False

    def dfs(node):
        nonlocal has_cycle
        color[node] = GRAY                  # mark as on the current DFS path
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:     # back-edge to the current path = cycle
                has_cycle = True
                return
            if color[neighbor] == WHITE:
                dfs(neighbor)
        color[node] = BLACK                 # fully explored
        order.append(node)                  # post-order: record AFTER dependents

    for node in graph:
        if color[node] == WHITE:
            dfs(node)
            if has_cycle:
                return None

    order.reverse()                         # post-order reversed = topological order
    return order


# --- Practical demo: resolve build/task dependencies ---
# Edge A -> B means "A must be done before B" (A is a prerequisite of B).
def can_finish_all(graph):
    return topo_sort_kahn(graph) is not None


if __name__ == "__main__":
    # A small dependency graph (a DAG):
    #   "boil water" and "get mug" have no prerequisites.
    #   "steep tea" needs both; "drink" needs "steep tea".
    tasks = {
        "boil water": ["steep tea"],
        "get mug": ["steep tea"],
        "steep tea": ["drink"],
        "drink": [],
    }
    print("=== Kahn's (BFS) ===")
    print(f"order: {topo_sort_kahn(tasks)}")
    # e.g. ['boil water', 'get mug', 'steep tea', 'drink']

    print("\n=== DFS-based ===")
    print(f"order: {topo_sort_dfs(tasks)}")
    # a valid ordering (may differ from Kahn's but still respects dependencies)

    print("\n=== Cycle detection ===")
    cyclic = {"a": ["b"], "b": ["c"], "c": ["a"]}   # a -> b -> c -> a (impossible)
    print(f"can_finish_all(cyclic) = {can_finish_all(cyclic)}")  # False
    print(f"topo_sort_kahn(cyclic) = {topo_sort_kahn(cyclic)}")  # None
    print(f"can_finish_all(tasks)  = {can_finish_all(tasks)}")   # True
