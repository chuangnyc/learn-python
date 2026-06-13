# --- How Python programs run (Go dev mental model) ---
#
# Go:  go build  →  single native binary  →  ./myapp  (no runtime needed on the host)
# Py:  source .py files  →  python3 myapp.py  (needs a Python interpreter installed)
#
# Python is not "compiled to a binary" by default. The interpreter:
#   1. reads your .py source
#   2. compiles it to bytecode (.pyc, cached under __pycache__)
#   3. executes bytecode in the CPython VM
#
# There is no go build equivalent in day-to-day Python. You ship source (or wheels)
# plus a dependency manifest (requirements.txt / pyproject.toml), and the runtime
# interprets it on the machine — usually inside a container with a pinned Python version.
#
# Production deployment patterns (contrast with a static Go binary):
#   - Web services:  gunicorn/uvicorn run your app module  (like go run, but long-lived)
#   - Containers:    FROM python:3.14  +  COPY app/  +  pip install -r requirements.txt
#   - CLIs:          pip install .  →  console_scripts entry point on PATH  (or python -m pkg)
#   - "Real" binary: PyInstaller/Nuitka exist, but are niche — not the default workflow
#
# if __name__ == "__main__"  (below) is Python's entry-point guard.
# Go always starts at func main() in package main. Python loads the whole file as a
# module first; this block runs only when the file is executed directly, not when imported.

import sys

def main():
    print("Hello, World!")
    print(f"Python version: {sys.version}")

if __name__ == "__main__":
    main()
