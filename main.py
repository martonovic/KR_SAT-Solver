import sys
import os
import glob
import time
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


def run(heur, input1):

    # parse arguments
    full_argments = parseargs(input1)

    # initialize variables:
    (variables, varbsCount, varbs) = getVars(full_argments)

    # this is the random heuristic i.e. randomly predetermining the order of variables to search through
    #variables = random_heuristic(variables)

    arguments = tautology(full_argments)  # remove tautologies, just necessary once.

    # initialization of lists (args & assignments) and boolean (validity_check)
    DPLL = {
        "validity_check": True,
        "arguments": [arguments],
        "assignments": [],
        "backtrack": [],
        "units": [],
        "first_backtrack": 0,
        "backtrack_counter": [],
    }

    sys.setrecursionlimit(10 ** 8)

    # iniitial unit propagation and simplification --> majority of clauses removed
    while any(len(clause) == 1 for clause in DPLL["arguments"][-1]) and DPLL["validity_check"]:
        variables, DPLL["assignments"], DPLL["units"] = unit_propagation(variables, DPLL["arguments"][-1], DPLL["assignments"], DPLL["units"])
        DPLL["arguments"][-1], DPLL["assignments"], DPLL["validity_check"] = simplify(DPLL["arguments"][-1], DPLL["assignments"], DPLL["validity_check"])

    units = DPLL["units"].copy()
    init_assignments = DPLL["assignments"].copy()
    assignments = init_assignments.copy()
    DPLL["units"] = []
    DPLL["assignments"] = []

    # initialize variables again (after first round of simplification):
    (variables1, varbsCount, varbs) = getVars(DPLL["arguments"][-1])

    # start recursive function

    DPLL = s1.solve(DPLL, variables1, heur)

    if not DPLL["validity_check"]:
        message = 'failure'
    else:
        message = 'Success! This formula is satisfiable, with the following assignments: '

    for atoms in DPLL["assignments"]:
        assignments.append(atoms)
    for unit in DPLL["units"]:
        units.append(unit)

    return init_assignments, assignments, message, DPLL["backtrack_counter"], units


if call.sudoku1:
    example = call.sudoku1
    version = 'S1'
elif call.sudoku2:
    example = call.sudoku2
    version = 'S2'
elif call.sudoku3:
    example = call.sudoku3
    version = 'S3'
else:
    example = os.getcwd()
    version = "S1"

if __name__ == "__main__":

    # initialize:
    tests = []
    times = []
    backtracks = []
    units = []
    inits = []
    sudoku_names = []
    cd = os.getcwd()

    for file in glob.glob(example + "/sudoku*.txt"): # ("*.txt") for single file, otherwise directory
        print(file)
        sudoku_name = os.path.basename(file)
        sudoku_names.append(sudoku_name)
        print(sudoku_name)
        # reset time
        last_time = time.time()

        initial_assignments, assignments, message, backtrack_counter, unit_literals = run(version, file)

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
