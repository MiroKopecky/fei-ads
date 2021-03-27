def split(data):
    return [int(each) for each in data]


def load_data_from_file(file_name: str):
    with open(file_name) as file:
        data = split(file.readline())

    return data


def play_game(tokens):
    length = len(tokens)
    table = [[0 for _ in range(length)]
             for _ in range(length)]

    for interval in range(length):
        for j in range(interval, length):
            i = j - interval

            if i == length - 1:
                break

            if tokens[i + 1] > tokens[j]:
                x = table[i + 2][j]
            else:
                x = table[i + 1][j - 1]

            if tokens[i] > tokens[j - 1]:
                y = table[i + 1][j - 1]
            else:
                y = table[i][j - 2]

            table[i][j] = max(tokens[i] + x, tokens[j] + y)
    return table[0][length - 1]


def main():
    tokens = load_data_from_file("cvicenie6data.txt")
    max_value = play_game(tokens)
    print(max_value)
    print("---END---")


if __name__ == "__main__":
    main()
