# A Hash Map (hash table) stores key-value pairs with O(1) average lookup,
# insert, and delete. It's the structure behind Python's dict and set, and
# behind Go's built-in map.
# -- The core idea:
#    A hash FUNCTION turns a key into an integer; that integer (mod the number
#    of buckets) picks a slot in an underlying array. So instead of searching
#    for a key, you COMPUTE where it lives -- that's why lookup is O(1).
# -- Practical Applications:
#    - Caches and memoization (key -> cached result)
#    - Counting / frequency tables (collections.Counter is a dict)
#    - De-duplication and membership tests (set)
#    - Database indexes, symbol tables in compilers
# Note: In real Python you just use dict / set. We build one from scratch here
# to see WHY it's O(1) and what "hash collision" means.


# --- The two problems every hash map must solve ---
# 1. Hashing: map an arbitrary key to a bucket index.
# 2. Collisions: two different keys can hash to the SAME bucket. We handle this
#    with "separate chaining" -- each bucket holds a list of (key, value) pairs.

class HashMap:
    def __init__(self, num_buckets=8, auto_resize=True):
        # Each bucket is a list of [key, value] pairs (the "chain").
        self.buckets = [[] for _ in range(num_buckets)]
        self._size = 0                      # number of stored pairs
        self.auto_resize = auto_resize      # off in the demo to force collisions

    # Turn a key into a bucket index. Python's built-in hash() does the heavy
    # lifting (works on any hashable: str, int, tuple, ...); we just fold it
    # into the valid index range with modulo.
    def _index(self, key):
        return hash(key) % len(self.buckets)

    # O(1) average: jump to the bucket, then scan its (usually tiny) chain.
    def put(self, key, value):
        bucket = self.buckets[self._index(key)]
        for pair in bucket:
            if pair[0] == key:              # key already present -> update
                pair[1] = value
                return
        bucket.append([key, value])         # new key -> append to the chain
        self._size += 1
        # Keep chains short: if the table is getting full, grow and rehash.
        if self.auto_resize and self._size / len(self.buckets) > 0.75:  # "load factor"
            self._resize()

    # O(1) average: hash to the bucket, scan the chain for the key.
    def get(self, key, default=None):
        bucket = self.buckets[self._index(key)]
        for k, v in bucket:
            if k == key:
                return v
        return default                      # not found

    def delete(self, key):
        bucket = self.buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def __contains__(self, key):            # enables: key in hashmap
        bucket = self.buckets[self._index(key)]
        return any(k == key for k, _ in bucket)

    def __len__(self):
        return self._size

    # When chains get long, lookups drift toward O(n). Resizing doubles the
    # bucket count and re-inserts everything so each key lands in a fresh slot,
    # restoring short chains. This is why dicts occasionally do extra work on
    # insert -- amortized O(1), not worst-case.
    def _resize(self):
        old = [pair for bucket in self.buckets for pair in bucket]
        self.buckets = [[] for _ in range(len(self.buckets) * 2)]
        self._size = 0
        for key, value in old:
            self.put(key, value)

    def items(self):
        return [tuple(pair) for bucket in self.buckets for pair in bucket]


# --- Why collisions are unavoidable ---
# There are infinitely many possible keys but a fixed number of buckets, so by
# the pigeonhole principle some keys MUST share a bucket. A good hash function
# spreads keys evenly so chains stay short; a bad one piles everything into one
# bucket, degrading the map to an O(n) linked-list scan.

def demo_collision():
    # Force a tiny table (resizing off) so keys MUST share buckets. We use int
    # keys here because hash(int) == int, so the distribution is deterministic:
    # with 2 buckets, even keys land in bucket 0 and odd keys in bucket 1.
    # (String hashing is randomized per run, so it wouldn't give a stable demo.)
    hm = HashMap(num_buckets=2, auto_resize=False)
    for k in [1, 2, 3, 4]:
        hm.put(k, k * 10)
    # Each bucket now holds a chain of >1 key -- that's a collision, handled.
    return [[pair[0] for pair in bucket] for bucket in hm.buckets]


if __name__ == "__main__":
    print("=== HashMap basics ===")
    hm = HashMap()
    hm.put("alice", 30)
    hm.put("bob", 25)
    hm.put("alice", 31)                     # update, not insert
    print(f"get('alice') = {hm.get('alice')}")   # 31
    print(f"get('carol', 0) = {hm.get('carol', 0)}")  # 0 (default)
    print(f"'bob' in hm = {'bob' in hm}")        # True
    print(f"len = {len(hm)}")                    # 2
    hm.delete("bob")
    print(f"after delete('bob'): 'bob' in hm = {'bob' in hm}, len = {len(hm)}")

    print("\n=== Collisions / chaining (2 buckets, resize off) ===")
    print(f"bucket contents: {demo_collision()}")
    # [[2, 4], [1, 3]] -- evens chain in bucket 0, odds in bucket 1

    print("\n=== Resizing keeps it O(1) ===")
    big = HashMap(num_buckets=2)
    for i in range(20):
        big.put(f"key{i}", i)
    print(f"stored {len(big)} pairs, grew to {len(big.buckets)} buckets")
    print(f"get('key17') = {big.get('key17')}")  # still found after rehashing

    print("\n=== The real thing: dict ===")
    # Everything above is what Python's dict does internally (in C, with open
    # addressing rather than chaining, but the same O(1) idea).
    d = {"alice": 31, "bob": 25}
    print(f"d['alice'] = {d['alice']}, 'carol' in d = {'carol' in d}")
