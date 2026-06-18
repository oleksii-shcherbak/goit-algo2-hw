from trie import Trie


class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")
        return sum(1 for w in self._words() if w.endswith(pattern))

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # suffix checks
    assert trie.count_words_with_suffix("e") == 1    # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1    # banana
    assert trie.count_words_with_suffix("at") == 1   # cat

    # prefix checks
    assert trie.has_prefix("app") == True   # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True   # banana
    assert trie.has_prefix("ca") == True    # cat

    # invalid input
    try:
        trie.count_words_with_suffix(123)
        assert False, "should raise"
    except TypeError:
        pass

    try:
        trie.has_prefix(None)
        assert False, "should raise"
    except TypeError:
        pass

    print("All assertions passed.")
