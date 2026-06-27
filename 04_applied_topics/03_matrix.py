# Matrix (2D grid) problems test how you walk a grid with bounds checking and
# how you explore connected regions with BFS/DFS.
# -- Python notes for a Go dev:
#    1. A 2D grid is a list of lists. Build one with
#       [[0] * cols for _ in range(rows)] -- NOT [[0] * cols] * rows, which
#       aliases the SAME inner list (the classic Python footgun; Go's [][]int
#       has no such trap because slices are copied per make).
#    2. len(grid) is the row count, len(grid[0]) the column count.
#    3. Directions as a list of (dr, dc) deltas keeps neighbor loops tidy.

from collections import deque


# --- Spiral traversal ---
# Peel the matrix like an onion: top row, right col, bottom row, left col,
# shrinking the four boundaries each loop until they cross.
def spiral_order(grid):
    if not grid:
        return []
    result = []
    top, bottom = 0, len(grid) - 1
    left, right = 0, len(grid[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):        # top row, left -> right
            result.append(grid[top][c])
        top += 1
        for r in range(top, bottom + 1):        # right col, top -> bottom
            result.append(grid[r][right])
        right -= 1
        if top <= bottom:                       # bottom row, right -> left
            for c in range(right, left - 1, -1):
                result.append(grid[bottom][c])
            bottom -= 1
        if left <= right:                       # left col, bottom -> top
            for r in range(bottom, top - 1, -1):
                result.append(grid[r][left])
            left += 1
    return result


# --- Rotate a square matrix 90 degrees clockwise, in place ---
# Two steps: transpose (swap across the diagonal), then reverse each row.
def rotate_90(grid):
    n = len(grid)
    for r in range(n):                          # transpose upper triangle
        for c in range(r + 1, n):
            grid[r][c], grid[c][r] = grid[c][r], grid[r][c]
    for row in grid:                            # mirror each row horizontally
        row.reverse()
    return grid


# --- Number of islands (connected components of '1's) ---
# Scan every cell; when we hit unvisited land, flood-fill its whole island
# with BFS so we never recount it. Each cell is visited once -> O(rows*cols).
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right
    count = 0

    def bfs(sr, sc):
        queue = deque([(sr, sc)])
        seen.add((sr, sc))
        while queue:
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and grid[nr][nc] == "1" and (nr, nc) not in seen):
                    seen.add((nr, nc))
                    queue.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                count += 1
                bfs(r, c)
    return count


# --- Set entire row and column to zero where a zero appears ---
# Record which rows/cols contain a zero first (a single scan), then blank them
# in a second pass. Doing it inline would corrupt cells you haven't read yet.
def set_zeroes(grid):
    zero_rows, zero_cols = set(), set()
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 0:
                zero_rows.add(r)
                zero_cols.add(c)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if r in zero_rows or c in zero_cols:
                grid[r][c] = 0
    return grid


if __name__ == "__main__":
    print("=== Spiral ===")
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"spiral_order(3x3) = {spiral_order(m)}")  # [1,2,3,6,9,8,7,4,5]

    print("\n=== Rotate ===")
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"rotate_90(3x3) = {rotate_90(m)}")  # [[7,4,1],[8,5,2],[9,6,3]]

    print("\n=== Islands ===")
    island_grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    print(f"num_islands = {num_islands(island_grid)}")  # 3

    print("\n=== Set zeroes ===")
    m = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    print(f"set_zeroes = {set_zeroes(m)}")  # [[1,0,1],[0,0,0],[1,0,1]]
