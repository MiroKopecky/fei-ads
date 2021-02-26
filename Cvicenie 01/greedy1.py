file = open('cvicenie1data.txt', 'r')

matrix_rows = int(file.readline())
matrix_columns = int(file.readline())

start_number = min([int(i) for i in file.readline().split()])

Lines = file.readlines()
matrix = [[int(num) for num in line.split()] for line in Lines]

row_sum = start_number
for line in matrix:
    min_number = min(line, key=lambda x: abs((x + row_sum)))
    row_sum += min_number

print("Suma: {}".format(row_sum))
print("DONE")
