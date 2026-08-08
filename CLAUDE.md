# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a hands-on Python course aimed at developers coming from Go. The primary goal is learning and mastering Python. The secondary goal is building a study guide useful for practicing tech interview problems.

## Audience

The author has deep Go experience. Exercises should draw Go comparisons where they clarify Python-specific behavior (duck typing, generators, decorators, EAFP error handling, asyncio vs goroutines, etc.). Skip explanations of concepts that are identical across both languages.

## Running exercises

No external dependencies, build step, linter, or test suite — this is Python 3.10+ stdlib only. Each file runs standalone:

```bash
python3 01_fundamentals/01_hello.py
python3 02_data_structures/01_stacks.py
```

There is no test framework in the repo; correctness is demonstrated via the labeled `print()` output in each file's `__main__` block, not assertions.

## Course structure

The repo is organized into four numbered sections that build on each other, tracked in the README.md course outline table (update that table when adding or changing an exercise file):

1. `01_fundamentals/` - Python language features and idioms
2. `02_data_structures/` - Implementations from scratch
3. `03_algorithm_patterns/` - Common interview problem-solving techniques
4. `04_applied_topics/` - Frequently tested problem categories

Files within a section are numbered in teaching order (e.g. `02_data_structures/03_linked_lists.py` assumes `01_stacks.py` and `02_queues.py` concepts are already known). When inserting a new exercise, keep this ordering intact rather than appending unrelated topics at the end.

## Exercise conventions

- Each `.py` file is self-contained with no external dependencies
- Comments should be concise and clear, placed above the code they describe
- Introduce Go comparisons inline when they help illustrate a Python-specific behavior
- Every file has an `if __name__ == "__main__"` block with runnable examples demonstrating the concepts
- Output should be clear and labeled so readers can follow along

## Content guidelines

- Prioritize idiomatic Python over transliterated Go
- Show the Pythonic way first, then note how it differs from Go if relevant
- Cover common gotchas and footguns that would trip up a Go developer
- For data structures and algorithms, implement from scratch before showing stdlib equivalents
- Keep exercises progressively building on earlier topics where possible
