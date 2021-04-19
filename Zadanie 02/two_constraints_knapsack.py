__author__ = 'Matúš Pohančenik'
__credits__ = ["stackoverflow: https://bit.ly/2OlKW35",
               "stackoverflow: https://bit.ly/3ufFCNQ"
               "youtube: https://bit.ly/3dwJpzM"]

import numpy as np

INPUT_FILE_NAME = "predmety.txt"
OUTPUT_FILE_NAME = "out.txt"


def load_data_from_file(file_name: str):
    """
    Function parses the input file.

    :param file_name: file name
    """
    items = dict()  # all items

    with open(file_name, 'r') as file:
        max_count = int(file.readline())  # max capacity of knapsack
        max_weight = int(file.readline())  # max weight of knapsack
        max_fragile_count = int(file.readline())  # max number of fragile items

        for line in file.readlines():
            item = [int(i) for i in line.split()]
            items[item[0]] = item[1:]

    return max_count, max_weight, max_fragile_count, items


def knapsack_problem(n: int, w: int, f: int, items: dict):
    """
    Function creates 3D array of solution.

    :param n: max capacity of knapsack
    :param w: max weight of knapsack
    :param f: max number of fragile items
    :param items: all items
    """
    knapsack = np.zeros((n + 1, w + 1, f + 1), dtype='int')

    for i in range(1, n + 1):
        for w in range(1, w + 1):
            for f in range(1, f + 1):

                item_value = items[i][0]
                item_weight = items[i][1]
                item_fragility = items[i][2]

                if item_weight > w or item_fragility > f:
                    knapsack[i, w, f] = knapsack[i - 1, w, f]
                else:
                    knapsack[i, w, f] = max(knapsack[i - 1, w, f], knapsack[
                        i - 1, w - item_weight, f - item_fragility]
                                            + item_value)

    return knapsack


def get_items_in_knapsack(w: int, f: int, items: dict, knapsack: np.ndarray):
    """
    Function finds which items are in the knapsack.

    :param w: max weight of knapsack
    :param f: max number of fragile items
    :param items: all items
    :param knapsack: all items
    """

    items_in_knapsack = list()  # item numbers in the knapsack

    for i in range(knapsack.shape[0] - 1, 0, -1):

        item_weight = items[i][1]
        item_fragility = items[i][2]

        if knapsack[i - 1, w, f] != knapsack[i, w, f]:
            w -= item_weight
            f -= item_fragility
            items_in_knapsack.append(i)

    return sorted(items_in_knapsack)


def write_data_to_file(file_name: str, data: tuple):
    """
    Function writes data to output file.

    :param file_name: file name
    :param data: output data
    """
    with open(file_name, 'w') as file:
        file.write(str(data[0]) + "\n")  # full knapsack price
        file.write(str(data[1]) + "\n")  # number of items in the knapsack
        file.writelines(str(line) + "\n" for line in data[2])  # items


def main():
    n, w, f, items = load_data_from_file(INPUT_FILE_NAME)
    solution_table = knapsack_problem(n, w, f, items)

    items_in_knapsack = get_items_in_knapsack(w, f, items, solution_table)
    final_weight = solution_table[n, w, f]
    final_count = len(items_in_knapsack)
    fragile_items_in_backpack = [item_num for item_num in items_in_knapsack
                                 if items[item_num][2] == 1]

    print(f"Hodnota naplneného ruksaku: {final_weight}")
    print(f"Počet predmetov v ruksaku: {final_count}")
    print(f"Čísla predmetov v ruksaku: {items_in_knapsack}")
    print(f"Krehké premety v ruksaku: {fragile_items_in_backpack}")

    write_data_to_file(OUTPUT_FILE_NAME,
                       (final_weight, final_count, items_in_knapsack))


if __name__ == '__main__':
    main()
