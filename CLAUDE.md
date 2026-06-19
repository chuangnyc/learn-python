# CLAUDE.md

## Purpose

This is a hands-on Python course aimed at developers coming from Go. The primary goal is learning and mastering Python. The secondary goal is building a study guide useful for practicing tech interview problems.

## Audience

The author has deep Go experience. Exercises should draw Go comparisons where they clarify Python-specific behavior (duck typing, generators, decorators, EAFP error handling, asyncio vs goroutines, etc.). Skip explanations of concepts that are identical across both languages.

## Course Structure

The repo is organized into numbered sections that build on each other:

1. `01_fundamentals/` - Python language features and idioms
2. `02_data_structures/` - Implementations from scratch
3. `03_algorithm_patterns/` - Common interview problem-solving techniques
4. `04_applied_topics/` - Frequently tested problem categories

## Exercise Conventions

- Each `.py` file is self-contained with no external dependencies
- Comments should be concise and clear, placed above the code they describe
- Introduce Go comparisons inline when they help illustrate a Python-specific behavior
- Every file has a `if __name__ == "__main__"` block with runnable examples demonstrating the concepts
- Output should be clear and labeled so readers can follow along

## Content Guidelines

- Prioritize idiomatic Python over transliterated Go
- Show the Pythonic way first, then note how it differs from Go if relevant
- Cover common gotchas and footguns that would trip up a Go developer
- For data structures and algorithms, implement from scratch before showing stdlib equivalents
- Keep exercises progressively building on earlier topics where possible
