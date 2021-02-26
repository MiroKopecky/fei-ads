import numpy as np


def shuffle_along_axis(a, axis):
    idx = np.random.rand(*a.shape).argsort(axis=axis)
    return np.take_along_axis(a, idx, axis=axis)


file = open('cvicenie1data.txt', 'r')

matrix_rows = int(file.readline())
matrix_columns = int(file.readline())
Lines = file.readlines()
matrix = np.array([[int(num) for num in line.split()] for line in Lines])

row_sum = 0
summed_numbers = []
iterations = 0
while True:
    iterations += 1
    for line in matrix:
        min_num = min(line, key=lambda x: abs((x + row_sum)))
        summed_numbers.append(min_num)
        row_sum += min_num

    if iterations >= 100000:
        break
    if row_sum != 0:
        np.random.shuffle(matrix)
        row_sum = 0
        summed_numbers.clear()
    else:
        break


print("Počet iteracii: {}".format(iterations))
print("Suma: {}".format(sum(summed_numbers)))
# print("Suma: {}".format(row_sum))
print("DONE")
