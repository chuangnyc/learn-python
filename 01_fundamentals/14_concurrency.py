# Python has three concurrency models, and choosing the right one hinges on
# the GIL. Coming from Go (one model: goroutines + channels, true parallelism),
# this is the most surprising area. Overview of all three, with guidance.

# --- The GIL (Global Interpreter Lock) ---
# CPython has a single lock that allows only ONE thread to execute Python
# bytecode at a time. Consequences:
#   - Threads do NOT give parallel speedup for CPU-bound Python code.
#   - Threads DO help I/O-bound work: a thread releases the GIL while waiting
#     on the network/disk, letting others run.
#   - For CPU parallelism you need PROCESSES (separate interpreters, no shared GIL).
# Go has no GIL -- goroutines run truly in parallel across cores. This is the
# key mental adjustment.


# --- 1. asyncio: cooperative concurrency (best for I/O) ---
# `async def` defines a coroutine; `await` yields control at I/O points so the
# event loop can run other coroutines. SINGLE-threaded -- concurrency without
# parallelism. Closest in spirit to goroutines, but cooperative (you must await)
# rather than preemptive, and it does not use multiple cores.

import asyncio
import time

async def fetch(name, delay):
    print(f"  start {name}")
    await asyncio.sleep(delay)       # non-blocking sleep: yields to the loop
    print(f"  done {name}")
    return f"{name}-result"

async def sequential():
    # await one at a time: total time = sum of delays (~0.3s)
    a = await fetch("A", 0.1)
    b = await fetch("B", 0.2)
    return [a, b]

async def concurrent():
    # gather runs coroutines concurrently: total time = MAX delay (~0.2s)
    return await asyncio.gather(
        fetch("X", 0.1),
        fetch("Y", 0.2),
    )

# asyncio.run() starts the event loop and runs a coroutine to completion.
# Calling an async def WITHOUT await just creates a coroutine object; it does
# nothing until scheduled on the loop.


# --- 2. threading: preemptive threads (best for blocking I/O) ---
# Real OS threads, but the GIL serializes Python bytecode. Use for I/O-bound
# work that uses blocking libraries (requests, file I/O) where you can't await.

import threading

def worker(results, idx, n):
    total = sum(range(n))            # (CPU work here won't parallelize -- GIL)
    results[idx] = total

def run_threads():
    results = [0, 0, 0]
    threads = [
        threading.Thread(target=worker, args=(results, i, 1000))
        for i in range(3)
    ]
    for t in threads:
        t.start()                    # begin running
    for t in threads:
        t.join()                     # wait for completion
    return results

# Shared mutable state across threads needs a Lock to avoid races.
counter = 0
lock = threading.Lock()

def increment(n):
    global counter
    for _ in range(n):
        with lock:                   # only one thread in here at a time
            counter += 1


# --- 3. multiprocessing: true parallelism (best for CPU-bound) ---
# Separate processes, each with its OWN interpreter and GIL -> real multicore
# parallelism. Cost: data is passed by pickling between processes (no shared
# memory by default), so there's overhead. Use for heavy CPU work.

from multiprocessing import Pool

def square(n):
    return n * n

def run_multiprocessing():
    # Pool spreads work across CPU cores. Guard with __main__ on some platforms.
    with Pool(processes=4) as pool:
        return pool.map(square, [1, 2, 3, 4, 5])


# --- concurrent.futures: one high-level API for threads AND processes ---
# Executors give a uniform interface; switch the pool type to switch models.

from concurrent.futures import ThreadPoolExecutor

def run_executor():
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = [ex.submit(lambda x: x * 2, i) for i in range(5)]
        return [f.result() for f in futures]


# --- Choosing a Model ---
#   I/O-bound, async-friendly libs  -> asyncio        (thousands of tasks, 1 thread)
#   I/O-bound, blocking libs        -> threading / ThreadPoolExecutor
#   CPU-bound                       -> multiprocessing / ProcessPoolExecutor
# Rule of thumb: asyncio for high-concurrency I/O, processes for CPU parallelism,
# threads for "I just need to not block on a few blocking calls."


if __name__ == "__main__":
    print("=== Concurrency ===\n")

    print("--- asyncio: sequential vs concurrent ---")
    t0 = time.perf_counter()
    asyncio.run(sequential())
    print(f"  sequential took ~{time.perf_counter() - t0:.2f}s (sum of delays)")

    t0 = time.perf_counter()
    out = asyncio.run(concurrent())
    print(f"  concurrent took ~{time.perf_counter() - t0:.2f}s (max delay) -> {out}")

    print("\n--- threading ---")
    print(f"  thread results: {run_threads()}")
    counter = 0
    threads = [threading.Thread(target=increment, args=(10_000,)) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"  locked counter (expect 40000): {counter}")

    print("\n--- multiprocessing ---")
    print(f"  parallel squares: {run_multiprocessing()}")

    print("\n--- concurrent.futures (ThreadPoolExecutor) ---")
    print(f"  executor results: {run_executor()}")

    print("\n(GIL note: the multiprocessing run is the only one using >1 core.)")
