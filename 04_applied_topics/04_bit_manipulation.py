# Bit Manipulation uses integers as bitsets and exploits binary properties to
# solve problems in O(1) space or to shave constant factors.
# -- Python notes for a Go dev:
#    1. Python ints are arbitrary precision -- they never overflow. There is no
#       uint32/int64 wraparound, so a "shift left" just keeps growing. When a
#       problem assumes 32-bit ints, mask with & 0xFFFFFFFF yourself.
#    2. Same operators as Go: & | ^ ~ << >>. Negative numbers behave as if in
#       infinite two's complement, so ~x == -x - 1.
#    3. Handy built-ins: bin(x) -> "0b101", x.bit_count() (3.10+) counts set
#       bits, int(s, 2) parses binary. Go has math/bits.OnesCount instead.

# --- Core single-bit operations (the four you must know cold) ---
# i is a 0-based bit index from the right (least significant bit = 0).
def get_bit(x, i):
    return (x >> i) & 1              # isolate bit i


def set_bit(x, i):
    return x | (1 << i)             # force bit i to 1


def clear_bit(x, i):
    return x & ~(1 << i)            # force bit i to 0


def toggle_bit(x, i):
    return x ^ (1 << i)            # flip bit i


# --- Count set bits (population count) ---
# Brian Kernighan's trick: x & (x - 1) clears the LOWEST set bit. Loop until
# zero, counting iterations -> runs once per set bit, not once per total bit.
def count_set_bits(x):
    count = 0
    while x:
        x &= x - 1
        count += 1
    return count


# --- Single number: every value appears twice except one ---
# XOR is its own inverse (a ^ a == 0) and commutes, so XOR-ing everything
# cancels the pairs and leaves the lone value. O(n) time, O(1) space.
def single_number(nums):
    result = 0
    for n in nums:
        result ^= n
    return result


# --- Is x a power of two? ---
# Powers of two have exactly one set bit, so x & (x - 1) wipes it to 0.
# Guard against x == 0, which would falsely pass.
def is_power_of_two(x):
    return x > 0 and (x & (x - 1)) == 0


# --- Reverse the bits of a 32-bit unsigned integer ---
# Pull the low bit off x and push it onto result, shifting result left each
# step. The 0xFFFFFFFF mask keeps us inside 32 bits despite Python's bignums.
def reverse_bits_32(x):
    result = 0
    for _ in range(32):
        result = (result << 1) | (x & 1)
        x >>= 1
    return result & 0xFFFFFFFF


# --- Sum of two integers without + or - ---
# XOR adds without carrying; (a & b) << 1 is the carry. Repeat until no carry.
# The mask simulates 32-bit wraparound that Python ints don't do natively.
def add_without_plus(a, b):
    mask = 0xFFFFFFFF
    while b & mask:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    a &= mask
    # reinterpret as signed 32-bit if the sign bit is set
    return a if a < 0x80000000 else ~(a ^ mask)


if __name__ == "__main__":
    print("=== Single-bit ops on 0b1010 (10) ===")
    print(f"get_bit(10, 1)   = {get_bit(10, 1)}")     # 1
    print(f"get_bit(10, 0)   = {get_bit(10, 0)}")     # 0
    print(f"set_bit(10, 0)   = {set_bit(10, 0)}")     # 11
    print(f"clear_bit(10, 1) = {clear_bit(10, 1)}")   # 8
    print(f"toggle_bit(10, 2)= {toggle_bit(10, 2)}")  # 14

    print("\n=== Counting / XOR ===")
    print(f"count_set_bits(0b1011) = {count_set_bits(0b1011)}")  # 3
    print(f"single_number([4,1,2,1,2]) = {single_number([4, 1, 2, 1, 2])}")  # 4

    print("\n=== Power of two ===")
    print(f"is_power_of_two(16) = {is_power_of_two(16)}")  # True
    print(f"is_power_of_two(18) = {is_power_of_two(18)}")  # False

    print("\n=== Bit tricks ===")
    print(f"reverse_bits_32(1) = {reverse_bits_32(1)}")  # 2147483648
    print(f"add_without_plus(7, 5)  = {add_without_plus(7, 5)}")    # 12
    print(f"add_without_plus(-3, 8) = {add_without_plus(-3, 8)}")   # 5
