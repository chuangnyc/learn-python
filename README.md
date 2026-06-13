# learn-python

A hands-on Python course for developers coming from Go. Each file is a self-contained exercise that implements a concept from scratch with inline explanations and runnable examples.

If you already write Go, you know static typing, interfaces, goroutines, and explicit error handling. This course focuses on where Python diverges: dynamic typing, duck typing, generators, decorators, comprehensions, and the patterns that make idiomatic Python feel very different from idiomatic Go. Where a Go comparison clarifies a concept, we draw the parallel directly.

The course starts with Python fundamentals and language-specific features, then builds into data structures, algorithm patterns, and applied interview topics. Designed as both a study guide for tech interviews and a reference for Python idioms you'll encounter in production codebases.

## Setup

**Prerequisites:**
- Python 3.10+ (no external dependencies required)

**Verify your installation:**
```bash
python3 --version
```

**Run any exercise:**
```bash
python3 01_fundamentals/01_hello.py
python3 02_data_structures/01_stacks.py
```

Each file includes a `if __name__ == "__main__"` block with example usage, so you can run them directly and see output.

## Course Outline

### `01_fundamentals/` - Python Language Essentials

Core language features and Python 3 idioms that differentiate Python from other languages.

| # | File | Topic | Status |
|---|------|-------|--------|
| 1 | 01_hello.py | Hello world, interpreter basics | Done |
| 2 | 02_types_and_variables.py | Dynamic typing, type hints, mutability | |
| 3 | 03_strings.py | f-strings, slicing, common methods | |
| 4 | 04_collections.py | Lists, tuples, sets, dicts, unpacking | |
| 5 | 05_comprehensions.py | List/dict/set comprehensions, generator expressions | |
| 6 | 06_functions.py | First-class functions, *args/**kwargs, closures | |
| 7 | 07_classes.py | OOP, dunder methods, dataclasses, protocols | |
| 8 | 08_iterators_generators.py | Iterators, generators, yield, lazy evaluation | |
| 9 | 09_decorators.py | Function/class decorators, functools | |
| 10 | 10_context_managers.py | with statement, contextlib, resource management | |
| 11 | 11_error_handling.py | Exceptions, custom errors, EAFP vs LBYL | |
| 12 | 12_pattern_matching.py | Structural pattern matching (match/case, Python 3.10+) | |
| 13 | 13_typing.py | Type annotations, generics, TypeVar, Protocol | |
| 14 | 14_concurrency.py | asyncio, threading, multiprocessing overview | |

### `02_data_structures/` - Core Data Structures

Implementations from scratch to understand how they work under the hood.

| # | File | Topic | Status |
|---|------|-------|--------|
| 1 | 01_stacks.py | Stacks (LIFO) | Done |
| 2 | 02_queues.py | Queues (FIFO, deque, priority) | Done |
| 3 | 03_linked_lists.py | Linked Lists (singly, doubly, cycle detection) | |
| 4 | 04_hash_maps.py | Hash Maps (collision handling, design) | |
| 5 | 05_binary_trees.py | Binary Trees (traversal, BST, balancing) | Done |
| 6 | 06_heaps.py | Heaps and Priority Queues | |
| 7 | 07_tries.py | Tries (prefix trees, autocomplete) | |
| 8 | 08_graphs.py | Graphs (adjacency list, BFS/DFS) | Done |

### `03_algorithm_patterns/` - Problem-Solving Techniques

Common patterns that appear repeatedly in coding interviews.

| # | File | Topic | Status |
|---|------|-------|--------|
| 1 | 01_two_pointers.py | Two Pointers (sorted arrays, palindromes) | |
| 2 | 02_sliding_window.py | Sliding Window (subarrays, substrings) | |
| 3 | 03_binary_search.py | Binary Search (sorted data, search space) | |
| 4 | 04_recursion.py | Recursion and Backtracking (permutations, subsets) | |
| 5 | 05_sorting.py | Sorting (merge sort, quick sort, comparators) | |
| 6 | 06_dynamic_programming.py | Dynamic Programming (memoization, tabulation) | |
| 7 | 07_greedy.py | Greedy Algorithms (intervals, scheduling) | |
| 8 | 08_topological_sort.py | Topological Sort (DAGs, dependency resolution) | |

### `04_applied_topics/` - Interview Staples

Frequently tested problem categories that combine multiple patterns.

| # | File | Topic | Status |
|---|------|-------|--------|
| 1 | 01_strings.py | String Manipulation (anagrams, encoding) | |
| 2 | 02_intervals.py | Intervals (merge, insert, overlap) | |
| 3 | 03_matrix.py | Matrix Traversal (spiral, island problems) | |
| 4 | 04_bit_manipulation.py | Bit Manipulation (masks, XOR tricks) | |
