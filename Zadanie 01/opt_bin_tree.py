__author__ = 'Matúš Pohančenik'

import sys
import numpy as np
from node import Node
from collections import OrderedDict
from dummy_node import DummyNode

FILE_NAME = "../dictionary.txt"


def load_data_from_file(file_name: str):
    """
    Function parses the input file with words.

    :param file_name: file name
    """
    words = dict()

    with open(file_name) as file:
        for line in file.readlines():
            (val, key) = line.split()
            words[key] = int(val)

    return OrderedDict(sorted(words.items()))


def calculate_probabilities(words: OrderedDict):
    """
    Function calculates probabilities of keys.

    :param words: ordered dictionary of words
    """
    p = dict()  # probabilities of keys
    q = dict()  # probabilities of dummy keys
    tmp_dummy_words = list()
    dummy_words = dict()  # dummy words
    key_words = dict()  # key words
    all_frequencies_sum = sum(words.values())
    dummy_key_freq = 0
    k_iter = 0

    for word, frequency in words.items():
        if frequency <= 50_000:
            dummy_key_freq += frequency
            tmp_dummy_words.append(word)
        else:
            p[k_iter + 1] = frequency / all_frequencies_sum
            key_words[k_iter + 1] = word

            q[k_iter] = dummy_key_freq / all_frequencies_sum
            dummy_words[k_iter] = tmp_dummy_words.copy()
            tmp_dummy_words.clear()
            dummy_key_freq = 0
            k_iter += 1

    q[k_iter] = dummy_key_freq / all_frequencies_sum
    dummy_words[k_iter] = tmp_dummy_words

    return p, q, key_words, dummy_words


def create_tables(p: dict, q: dict, n: int):
    """
    Function creates cost and root tables. Algorithm taken
    from the book 'Introduction to algorithms' section 15.5.

    :param p: probabilities of keys
    :param q: probabilities of dummy keys
    :param n: number of keys
    """
    e = np.zeros([n + 1, n])  # cost table
    w = np.zeros([n + 1, n])  # table of intermediate calculation
    root = np.zeros([n, n], dtype='int')  # root table

    for i in range(1, n + 1):
        e[i, i - 1] = q[i - 1]
        w[i, i - 1] = q[i - 1]

    for l in range(1, n):
        for i in range(1, n - l + 1):
            j = i + l - 1
            e[i, j] = sys.float_info.max
            w[i, j] = w[i, j - 1] + p[j] + q[j]
            for r in range(i, j + 1):
                t = e[i, r - 1] + e[r + 1, j] + w[i, j]
                if t < e[i, j]:
                    e[i, j] = t
                    root[i, j] = r

    return e, root


def build_tree(root_table: np.ndarray, key_words: dict, dummy_words: dict):
    """
    Function builds optimal binary search tree

    :param root_table: root table
    :param key_words: dictionary of key words
    :param dummy_words: dictionary of dummy words
    """
    root_index = root_table[1, len(root_table) - 1]
    root_node = Node(key_words[root_index])
    stack = [(root_node, 1, len(root_table) - 1)]

    while stack:
        node, row, col = stack.pop()
        root_index = root_table[row, col]

        if root_index < col:
            node.right = Node(key_words[root_table[root_index + 1, col]])
            stack.append((node.right, root_index + 1, col))
        else:
            node.right = DummyNode(dummy_words[root_index])

        if row < root_index:
            node.left = Node(key_words[root_table[row, root_index - 1]])
            stack.append((node.left, row, root_index - 1))
        else:
            node.left = DummyNode(dummy_words[root_index - 1])

    return root_node


def pocet_porovnani(obs_tree: Node, word: str):
    print(f'Počet porovnaní pre slovo \"{word}\" je {obs_tree.search(word)}.')


def main():
    if len(sys.argv) == 2:
        word_to_search = sys.argv[1]
    else:
        word_to_search = input("Napíšte slovo, ktoré chcete hľadať: ")

    words = load_data_from_file(FILE_NAME)
    key_prob, dummy_prob, key_words, dummy_words = calculate_probabilities(
        words)
    cost_table, root_table = create_tables(key_prob, dummy_prob,
                                           len(dummy_prob))

    obs_tree = build_tree(root_table, key_words, dummy_words)
    pocet_porovnani(obs_tree, word_to_search)
    print('--END--')


if __name__ == '__main__':
    main()
