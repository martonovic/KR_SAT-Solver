import os, glob
import converter


def concat(rules, location, destination):
    file_loc = os.path.join(os.getcwd(), location)
    os.chdir(file_loc)

    if not os.path.isdir(os.path.join(file_loc, destination)):
        os.makedirs(os.path.join(file_loc, destination))

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


b = 9
loc = 'tests/damnhard/'
file = open(loc + 'damnhard.txt', 'r')
converter.convert2dimacs(file, loc, b)

concat('sudoku-rules-9x9.txt', 'tests/damnhard/', 'out')
