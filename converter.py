import numpy as np

b = 16
loc = 'tests/16x16_sudoku/'
file = open('tests/16x16_sudoku/16x16.txt', 'r')

def convert2dimacs(file, location, base=10):
    lines = file.readlines()
    counter = 1
    for line in lines:
        dimacs = []
        line = line.strip()
        n_cols = int(np.sqrt(len(line)))
        n_rows = int(np.sqrt(len(line)))
        sudoku_array = np.asarray([literal for literal in line])
        sudoku_matrix = np.reshape(sudoku_array, (n_rows, n_cols))

        file_name = location + 'sudoku_{}x{}_{:05}.txt'.format(n_rows, n_cols, counter)
        with open(file_name, 'w') as f:
            for i in range(n_rows):
                for j in range(n_cols):
                    if sudoku_matrix[i][j] != '.':
                        if base > 10:
                            tmp_val = int(sudoku_matrix[i][j], base+1)
                            value = ((i+1)*((base+1)**2)) + ((j+1)*(base+1)) + tmp_val
                        else:
                            value = int(str(i+1) + str(j+1) + sudoku_matrix[i][j])
                        dimacs.append('{} 0\n'.format(value))
                        f.write('{} 0\n'.format(value))
        counter += 1

convert2dimacs(file, loc, b)