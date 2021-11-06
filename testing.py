import os


def create_output(assignments, sudoku_name, difficulty_level, version):  # pass difficulty_level as string
    current_path = os.getcwd()
    directory = difficulty_level
    newpath = os.path.join(current_path, directory, version)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(newpath)
    filename = '{}_out.txt'.format(sudoku_name)
    with open(filename, 'w') as f:
        for assignment in assignments:
            f.write('{} 0\n'.format(assignment))

    return newpath


def collect_test_results(assignments, sudoku_name, difficulty_level, initial_assignments, backtrack_counter, units,
                         now_time):
    filename = 'test_results_file.txt'
    with open(filename, 'w') as f:
        f.write('-----------------------------------------------------------\n')
        f.write('Difficulty: \n'.format(difficulty_level))
        f.write('{}\n'.format(sudoku_name))
        f.write('Number of initial assignments: {}\n'.format(initial_assignments))
        f.write('Number of assignments: {}\n'.format(assignments))
        f.write('Number of backtracks: {}\n'.format(backtrack_counter))
        f.write('Number of unit literals: {}\n'.format(units))
        f.write('Processing time in seconds: {}\n'.format(now_time))