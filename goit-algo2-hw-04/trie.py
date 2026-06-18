class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.value = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def put(self, word: str, value) -> None:
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.is_end = True
        node.value = value

    def _words(self, node=None, prefix=""):
        if node is None:
            node = self.root
        if node.is_end:
            yield prefix
        for char, child in node.children.items():
            yield from self._words(child, prefix + char)
