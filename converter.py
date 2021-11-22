import numpy as np

file = open('4x4.txt', 'r')
file2 = open('1000 sudokus.txt', 'r')
file3 = open('top870.sdk.txt', 'r')

def convert2dimacs(file):
    lines = file.readlines()
    counter = 1
    for line in lines:
        dimacs = []
        line = line.strip()
        n_cols = int(np.sqrt(len(line)))
        n_rows = int(np.sqrt(len(line)))
        sudoku_array = np.asarray([literal for literal in line])
        sudoku_matrix = np.reshape(sudoku_array, (n_rows, n_cols))

        file_name = 'sudoku_{}x{}_{:05}.txt'.format(n_rows, n_cols, counter)
        with open(file_name, 'w') as f:
            for i in range(n_rows):
                for j in range(n_cols):
                    if sudoku_matrix[i][j] != '.':
                        value = sudoku_matrix[i][j]
                        dimacs.append('{}{}{} 0\n'.format(i+1,j+1,value))
                        f.write('{}{}{} 0\n'.format(i+1,j+1,value))
        counter += 1