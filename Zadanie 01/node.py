__author__ = 'Matúš Pohančenik'


class Node:
    """
    A class to represent a tree node.

    Attributes:
        left : left child
        right: right child
        word: word
    """

    def __init__(self, word: str):
        """
        Constructs all the necessary attributes for the node object
        """
        self.left = None
        self.right = None
        self.word = word

    def search(self, word, number_of_compares=0):
        """
        Function searches for the given word
        """
        number_of_compares += 1

        if self.word < word:
            number_of_compares = self.right.search(word, number_of_compares)
        elif self.word > word:
            number_of_compares = self.left.search(word, number_of_compares)

        return number_of_compares
