import sys
import testing as tst
from simplification import *
from preprocessing import *
import S1 as s1
import S2 as s2
import S3 as s3
import argparse

# here are the arguments that you want to give to the program from the terminal/command line
parser = argparse.ArgumentParser(description='sudoku SAT solver')
parser.add_argument('-S1', '--sudoku1', metavar='', help='input puzzle')
parser.add_argument('-S2', '--sudoku2', metavar='', help='input puzzle')
parser.add_argument('-S3', '--sudoku3', metavar='', help='input puzzle')

call = parser.parse_args()


def main(version, input1):

    # parse arguments
    full_argments = parseargs(input1)

    # initialize variables:
    (variables, varbsCount, varbs) = getVars(full_argments)

    # this is the random heuristic
    #variables = random_heuristic(variables)

    argments = tautology(full_argments)  # remove tautologies, just necessary once.

    # initialization of lists (args & assignments) and boolean (validity_check)
    validity_check = True
    assments = []
    backtrack = []
    units = []
    first_backtrack = 0
    backtrack_counter = []

    sys.setrecursionlimit(10 ** 8)

    while any(len(clause) == 1 for clause in argments) and validity_check:
        variables, assments, units = unit_propagation(variables, argments, assments, units)
        argments, assments, validity_check = simplify(argments, assments, validity_check)
    init_units = units.copy()
    print(units)
    del units
    units = []
    argies = argments.copy()
    # initialize variables again (after first round of :
    (variables1, varbsCount, varbs) = getVars(argments)
    init_assignments = assments.copy()
    assments = []

    # start recursive function
    if version == 'S1':
        assments, backtrack_counter, units = s1.solve(argies, assments, variables1, backtrack, backtrack_counter, argments, units, first_backtrack)
    elif version == 'S2':
        assments, backtrack_counter, units = s2.solve(argies, assments, variables1, backtrack, backtrack_counter, argments, units, first_backtrack)
    elif version == 'S3':
        assments, backtrack_counter, units = s3.solve(argies, assments, variables1, backtrack, backtrack_counter, argments, units, first_backtrack)

    if not validity_check:
        message = 'failure'
    else:
        message = 'Success! This formula is satisfiable, with the following assignments: '

    for atoms in init_assignments:
        assments.append(atoms)
    for unit in init_units:
        units.append(unit)

    return init_assignments, assments, message, backtrack_counter, units


if call.sudoku1:
    example = call.sudoku1
    version = 'S1'
elif call.sudoku2:
    example = call.sudoku2
    version = 'S2'
elif call.sudoku3:
    example = call.sudoku3
    version = 'S3'

if __name__ == "__main__":
    import os
    import glob
    import time

    # initialize:
    tests = []
    times = []
    backtracks = []
    units = []
    inits = []
    sudoku_names = []
    cd = os.getcwd()

    for file in glob.glob(example + "/*.txt"): # ("*.txt") for single file, otherwise directory
        print(file)
        sudoku_name = os.path.basename(file)
        sudoku_names.append(sudoku_name)
        print(sudoku_name)
        # reset time
        last_time = time.time()

        initial_assignments, assignments, message, backtrack_counter, unit_literals = main(version, file)

        path = tst.create_output(assignments, sudoku_name, example, version)

        # measure time
        now_time = time.time() - last_time

        # record results and dependent variables
        tests.append(len(assignments))
        backtracks.append(len(backtrack_counter))
        inits.append(len(initial_assignments))
        units.append(len(unit_literals))
        times.append(now_time)

        print(message, sorted(assignments, reverse=True))
        print('Number of initial assignments:', len(initial_assignments))
        print('Number of assignments:', len(assignments))
        print('Number of backtracks:', len(backtrack_counter))
        print('Number of unit literals:', len(unit_literals))
        print("--- %s seconds ---" % (now_time))

        os.chdir(cd)

    os.chdir(path)
    tst.collect_test_results(tests, sudoku_names, example, inits, backtracks, units,
                         times)
    print(tests)
    print(times)
    print(backtracks)
    print(inits)
    print(units)
