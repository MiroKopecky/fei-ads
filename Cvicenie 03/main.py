file = open("./data.txt")
Lines = file.readlines()
file.close()

pixel_matrix = [[int(num) for num in line.split()] for line in Lines]
previous_energies_row = list(pixel_matrix[0])

for row in range(1, len(pixel_matrix)):
    pixel_energies_row = pixel_matrix[row]
    energies_results = []

    for col, pixel_energy in enumerate(pixel_energies_row):

        col_left = max(col - 1, 0)
        col_right = min(col + 1, len(pixel_energies_row) - 1)
        col_range = range(col_left, col_right + 1)

        min_energy = pixel_energy + min(
            previous_energies_row[x] for x in col_range)

        energies_results.append(min_energy)

    previous_energies_row = energies_results

print(min(previous_energies_row))
