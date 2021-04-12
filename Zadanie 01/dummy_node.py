__author__ = 'Matúš Pohančenik'


class DummyNode:
    """
    A class to represent a tree dummy node.

    Attributes:
        words: set of dummy words
    """

    def __init__(self, words: []):
        """
        Constructs all the necessary attributes for the dummy node object
        """
        self.words = set(words)

    def search(self, word, number_of_compares=0):
        # if word in self.words:
        #    return number_of_compares + 1
        # return None

        return number_of_compares + 1
