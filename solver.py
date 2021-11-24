from simplification import *
from heur import *

def solve(tree: dict, variables: list, heur: str):
#def solve(arguments, assignments, variables, backtrack, backtrack_counter, simplified_arguments, units, first_backtrack):

    tree["validity_check"] = True
    # simplify formula and check if it's unsatisfiable with chosen assignments
    tree["arguments"].append([])
    tree["arguments"][-1], tree["assignments"], tree["validity_check"] = simplify(tree["arguments"][-2], tree["assignments"], tree["validity_check"])
    print('[INFO - ASSIGNMENTS]', '  number of assignments:', len(tree["assignments"]))
    tree["all_assignments"].extend(tree["assignments"].copy())
    # this is just unit propagation
    while any(len(clause) == 1 for clause in tree["arguments"][-1]) and tree["validity_check"]:
        variables, tree["assignments"], tree["units"] = unit_propagation(variables, tree["arguments"][-1], tree["assignments"], tree["units"])
        tree["arguments"][-1], tree["assignments"], tree["validity_check"] = simplify(tree["arguments"][-1], tree["assignments"], tree["validity_check"])
    tree["all_assignments"].extend(tree["assignments"].copy())
    # if no arguments left, then the formula is satisfied
    if not tree["arguments"][-1] and tree["validity_check"]:
        return tree

    if len(tree["assignments"]) == len(variables) and not tree["validity_check"] and abs(tree["assignments"][-1]) not in tree["backtrack"]:
        tree["assignments"][-1] = -tree["assignments"][-1]
        tree["all_assignments"].append(-tree["assignments"][-1].copy())
        tree["recursion_depth"] += 1
        solve(tree, variables, heur)
        return tree

    if heur == 'S2':
        varbs = [x for x in variables if (x not in tree["assignments"] and -x not in tree["assignments"])]
        next_lit = moms_heuristic(varbs, 2, tree["arguments"][-1])
    elif heur == 'S3':
        varbs = [x for x in variables if (x not in tree["assignments"] and -x not in tree["assignments"])]
        next_lit = jw1_heuristic(varbs, tree["arguments"][-1])
    elif heur == 'S4':
        varbs = [x for x in variables if (x not in tree["assignments"] and -x not in tree["assignments"])]
        next_lit = DLIS_heuristic(varbs, tree["arguments"][-1])
    elif heur == 'S5':
        varbs = [x for x in variables if (x not in tree["assignments"] and -x not in tree["assignments"])]
        next_lit = sudo_heruistic(tree["init_assignments"] + tree["assignments"], varbs, base=16)
    else:
        for var in variables:
            if var not in tree["assignments"] and -var not in tree["assignments"]:
                next_lit = var

    # if formula is still satisfiable, then add next assignment from list and go to next level in recursion
    if tree["validity_check"]:

        tree["assignments"].append(next_lit)
        tree["all_assignments"].append(next_lit)
        tree["recursion_depth"] += 1
        solve(tree, variables, heur)   

    # otherwise, backtrack...
    else:
        print('[INFO - UNIT PROPAGATION]', '  number of units propagated:', len(tree["units"]))
        # bigger backtracking steps can be taken IF the last assignments made have been either backtracked on
        # OR if the assignments were made through unit propagation
        while (len(tree["assignments"]) > 1 and abs(tree["assignments"][-1]) in tree["backtrack"]) or \
                (len(tree["assignments"]) > 1 and abs(tree["assignments"][-1]) in tree["units"]):
            # this is necessary to see if backtracking leads to a variable which has already been backtracked on
            # if so, then it can be removed from assignments and another step backwards can be taken
            while len(tree["assignments"]) > 1 and abs(tree["assignments"][-1]) in tree["backtrack"]:
                del tree["backtrack"][tree["backtrack"].index(abs(tree["assignments"][-1]))]
                del tree["assignments"][-1]
            # this is to remove the most recently added unit literals, makes testing quicker
            while len(tree["assignments"]) > 1 and abs(tree["assignments"][-1]) in tree["units"]:
                del tree["units"][tree["units"].index(abs(tree["assignments"][-1]))]
                del tree["assignments"][-1]

        # this is the main backtracking bit. Flip the last assignment and add to list of backtracked variables
        # also remove last clause simplification step i.e. go to previous list of clauses
        tree["backtrack"].append(abs(tree["assignments"][-1]))
        tree["assignments"][-1] = -tree["assignments"][-1]
        tree["all_assignments"].append(-tree["assignments"][-1])
        del tree["arguments"][-1]

        if tree["first_backtrack"] == abs(tree["assignments"][-1]):
            return tree

        # if everything has been backtracked on, formula is unsatisfiable --> exits function
        if len(tree["assignments"]) == 1 and len(tree["backtrack"]) == 1 and abs(tree["assignments"][0]) in tree["backtrack"]:
            tree["first_backtrack"] = tree["backtrack"][0]

        tree["backtrack_counter"].append(tree["backtrack"][-1])
        print('[INFO - BACKTRACKING]  nr. backtracks:', len(tree["backtrack_counter"]))
        tree["recursion_depth"] += 1
        solve(tree, variables, heur)

    return tree
