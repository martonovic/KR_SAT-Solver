def tautology(clauses):
    for literals in clauses:
        for lit in literals:
            if -lit in literals:
                clauses.remove(literals)
                return clauses

    return clauses


def pure_literals(clauses, varbs, assigns):
    for literals in clauses:
        for lit in literals:
            if -lit not in varbs and lit not in assigns:
                assigns.append(lit)
    return assigns


def unit_clauses(clauses, assigns, validity_check):
    varbs = []

    for literals in clauses:
        if len(literals) == 1:
            item = literals[0]
            varbs.append(item)

    for items in varbs:
        if -items in varbs or -items in assigns:
            validity_check = False

    return validity_check


def true_clauses(clauses, assigns, validity_check):
    if validity_check:
        rem_clauses = []
        for literals in clauses:
            if any(item in literals for item in assigns):
                rem_clauses.append(literals)
        for rc in rem_clauses:
            clauses.remove(rc)

    return clauses


def val_check(clauses, validity_check, assigns):
    varbs = []
    for literals in clauses:
        #check for empty clauses
        if not literals:
            validity_check = False
        # check for unit literals
        if len(literals) == 1:
            varbs.append(literals[0])

    #  if pos and neg variables occur together, then false
    for items in varbs:
        if -items in varbs or -items in assigns:
            validity_check = False

    return validity_check


def shorten_clause(clauses, assigns, validity_check):
    if validity_check:
        for literals in clauses:
            keep_lits = []
            if len(literals) > 1:
                for lit in literals:
                    if -lit not in assigns:
                        keep_lits.append(lit)
                if keep_lits:
                    new_clause = [liters for liters in keep_lits]
                else:
                    new_clause = []
                clauses[clauses.index(literals)] = new_clause
    return clauses


def unit_propagation(variables, clauses, assmts, units):
    clauses.sort(key=len)
    n = 0
    while n < len(clauses) and len(clauses[n]) == 1:
        literals = clauses[n]
        if literals[0] not in assmts and -literals[0] not in assmts:
            assmts.append(literals[0])
            if abs(literals[0]) not in units: units.append(abs(literals[0]))
        n += 1

    return variables, assmts, units


# function to simplify CNF with assignments and rules
def simplify(clauses, assigns, validity_check):

    # assign values to pure literals, can be left out: computationally expensive
    #assigns = pure_literals(clauses, varb, assigns)

    # shorten clauses
    clauses1 = shorten_clause(clauses, assigns, validity_check)

    if validity_check:
        validity_check = val_check(clauses1, validity_check, assigns)

    # remove true clauses
    clauses2 = true_clauses(clauses1, assigns, validity_check)

    validity_check = val_check(clauses, validity_check, assigns)

    return clauses2, assigns, validity_check