# A Trie (prefix tree, pronounced "try") stores strings by their CHARACTERS,
# one node per character, sharing common prefixes. Words like "cat", "car",
# and "card" share the path c -> a -> r before branching, so the shared prefix
# is stored once.
# -- Cost profile (L = length of the word/prefix, NOT the number of words):
#    - insert / search / starts_with:  O(L)
#    The number of stored words doesn't affect lookup time -- only the word's
#    length does. A hash set also gives ~O(L) membership, but a trie uniquely
#    answers PREFIX queries ("all words starting with 'ca'") efficiently.
# -- Practical Applications:
#    - Autocomplete / typeahead suggestions
#    - Spell checkers and dictionaries
#    - IP routing tables (longest-prefix match)
#    - Word games (Boggle, Scrabble solvers)
# Note: There's no built-in trie in Python or Go -- you build it. A nested dict
# is the idiomatic from-scratch representation.


# --- Structure ---
# Each node has:
#   - children: a dict mapping a single character -> the child TrieNode
#   - is_end:   marks whether a complete word ends here (so "car" and "card"
#               can both exist on the same path -- "car" is an end, and the
#               path continues to "card")

class TrieNode:
    def __init__(self):
        self.children = {}      # char -> TrieNode (a dict, for O(1) char lookup)
        self.is_end = False     # True if a word terminates at this node

class Trie:
    def __init__(self):
        self.root = TrieNode()  # the root represents the empty prefix ""

    # Walk/create one node per character, then flag the final node as a word end.
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()   # extend the path
            node = node.children[char]
        node.is_end = True

    # Helper: walk down by each character, return the node where `prefix` ends
    # (or None if the path breaks). Both search and starts_with build on this.
    def _walk(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None        # path doesn't exist -> no such prefix
            node = node.children[char]
        return node

    # Exact word match: the path must exist AND end on a word boundary.
    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    # Prefix match: the path just has to exist (is_end doesn't matter).
    # This is the trie's signature operation -- the reason to use one over a set.
    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    # Autocomplete: find the prefix node, then collect every word beneath it.
    def autocomplete(self, prefix):
        node = self._walk(prefix)
        if node is None:
            return []
        results = []
        self._collect(node, prefix, results)
        return results

    # Depth-first walk gathering completed words (this is DFS on the trie --
    # the same traversal idea from the graphs/trees lessons).
    def _collect(self, node, path, results):
        if node.is_end:
            results.append(path)
        for char, child in node.children.items():
            self._collect(child, path + char, results)


if __name__ == "__main__":
    trie = Trie()
    for word in ["cat", "car", "card", "care", "dog", "do"]:
        trie.insert(word)

    print("=== search (exact word) ===")
    print(f"search('car')  = {trie.search('car')}")    # True
    print(f"search('ca')   = {trie.search('ca')}")     # False -- prefix, not a word
    print(f"search('cards')= {trie.search('cards')}")  # False -- path breaks

    print("\n=== starts_with (prefix) ===")
    print(f"starts_with('ca') = {trie.starts_with('ca')}")  # True
    print(f"starts_with('z')  = {trie.starts_with('z')}")   # False

    print("\n=== autocomplete ===")
    print(f"prefix 'ca' -> {sorted(trie.autocomplete('ca'))}")
    # ['car', 'card', 'care', 'cat']
    print(f"prefix 'do' -> {sorted(trie.autocomplete('do'))}")
    # ['do', 'dog']  -- 'do' is itself a word AND a prefix
    print(f"prefix 'x'  -> {trie.autocomplete('x')}")       # []

    print("\n=== shared prefixes ===")
    # 'cat', 'car', 'card', 'care' all share the c->a path; only one 'c' node
    # and one 'a' node exist, then the tree branches. That sharing is the whole
    # point of a trie.
    c_node = trie.root.children['c']
    a_node = c_node.children['a']
    print(f"after 'ca', next chars branch to: {sorted(a_node.children.keys())}")
    # ['r', 't']  -- 'r' leads to car/card/care, 't' leads to cat
