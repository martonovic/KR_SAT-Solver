import glob
import os


def concat(rules, location, destination):
    file_loc = os.path.join(os.getcwd(), location)
    os.chdir(file_loc)

    # read in all txt files
    files = glob.glob(os.path.join('sudoku*.txt'))

    # find the index of the sudoku rules
    rules_index = files.index(rules)

    # create new sudoku_test (rules + puzzle) for each puzzle
    for index_file, this_file in enumerate(files):
        if this_file != rules:
            with open(os.path.join(destination, "sudoku_test{}.txt").format(index_file), "wb") as outfile:
                with open(files[rules_index], "rb") as rules:
                    outfile.write(rules.read())
                with open(this_file, "rb") as infile:
                    outfile.write(infile.read())


concat('sudoku-rules-16x16.txt', 'tests/16x16_sudoku/', 'out')
