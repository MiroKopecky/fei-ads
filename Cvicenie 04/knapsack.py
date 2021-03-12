def knapsack_problem(w, wt1, wt2, val1, val2, n):

    knapsack = [[0 for _ in range(w + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, w + 1):
            value_1 = value_2 = -1

            if wt1[i - 1] <= w:
                value_1 = val1[i - 1] + knapsack[i - 1][w - wt1[i - 1]]

            if wt2[i - 1] <= w:
                value_2 = val2[i - 1] + knapsack[i - 1][w - wt2[i - 1]]

            knapsack[i][w] = max(value_1, value_2, knapsack[i - 1][w])

    return knapsack[n][w]


def main():
    file = open("./cvicenie4data.txt")
    lines = file.readlines()
    file.close()

    val1, wt1, val2, wt2 = [], [], [], []

    for line in lines:
        current_line = line.split(",")
        val1.append(int(current_line[0]))
        wt1.append(int(current_line[1]))
        val2.append(int(current_line[2]))
        wt2.append(int(current_line[3]))

    w = 2000
    n = len(val1)
    print(knapsack_problem(w, wt1, wt2, val1, val2, n))


if __name__ == "__main__":
    main()
