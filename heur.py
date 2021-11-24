from collections import *
import random
import numpy as np

def random_heuristic(variables):
    random.shuffle(variables)
    for varb in variables:
        if random.random() > 0.5:
            variables[variables.index(varb)] = -varb
    print(variables)
    return variables


def f(clauses, literal):
    smallest_clauses_size = len(min(clauses, key=len))
    number_of_occurances = 0
    for clause in clauses:
        if len(clause) == smallest_clauses_size:
            if literal in clause: # or -literal in clause:
                number_of_occurances += 1
    return number_of_occurances


def moms_heuristic(atoms, k, clauses):  # atoms = argments?, k=2
    max_val = 0
    chosen_literal = None
    for atom in atoms:
        function_res = (f(clauses, atom) + f(clauses, -atom))*(2**k) + (f(clauses, atom) * f(clauses, -atom))
        if function_res > max_val:
            max_val = function_res
            chosen_literal = atom
    return chosen_literal


def jw1_heuristic(literals, clauses):
    j_value = {}
    for literal in literals:
        j_value[literal] = 0
        for clause in clauses:
            if literal in clause:
                j_value[literal] += 2 ** (-len(clause))

    chosen_literal = max(j_value, key=j_value.get)

    return chosen_literal


def DLIS_heuristic(clauses, varbs):
    neg_count = defaultdict(int)
    pos_count = defaultdict(int)

    for clause in clauses:
        for literal in clause:
            if literal < 0:
                neg_count[literal] += 1
            else:
                pos_count[literal] += 1

    pos_chosen_literal = None
    neg_chosen_literal = None

    for x in sorted(pos_count, key=pos_count.get, reverse=True):
        if x in varbs:
            pos_chosen_literal = x
    for y in sorted(neg_count, key=neg_count.get, reverse=True):
        if y in varbs:
            neg_chosen_literal = y

    if pos_chosen_literal and neg_chosen_literal:
        if pos_count[pos_chosen_literal] > neg_count[neg_chosen_literal]:
            return pos_chosen_literal
        else:
            return neg_chosen_literal
    elif (pos_chosen_literal and not neg_chosen_literal):
        return pos_chosen_literal
    else:
        return neg_chosen_literal


def sudo_heruistic(assignments, varbs, base=9):
    if base > 10:
        tmp_assignments = [str(np.base_repr(abs(x), base+1)) for x in assignments]
    else:
        tmp_assignments = [str(abs(w)) for w in assignments]

    row_count = [[i[0] for i in tmp_assignments].count(str(y)) for y in range(1, base+1)]
    col_count = [[j[1] for j in tmp_assignments].count(str(z)) for z in range(1, base+1)]

    row_min = min(row_count)
    col_min = min(col_count)

    row_val_inds = sorted(zip(row_count, range(base)))
    col_val_inds = sorted(zip(col_count, range(base)))

    rand_select = list(range(1, base + 1))
    random.shuffle(rand_select)

    if row_min < col_min:
        for k in row_val_inds:
            for l in col_val_inds:
                for m in rand_select:
                    chosen_lit = int(str(k[1]+1) + str(l[1]+1) + str(m))

                    if chosen_lit in varbs:
                        if random.random() > 0.5: chosen_lit = -chosen_lit
                        return chosen_lit

    else:
        for l in col_val_inds:
            for k in row_val_inds:
                for m in rand_select:
                    chosen_lit = int(str(k[1]+1) + str(l[1]+1) + str(m))

                    if chosen_lit in varbs:
                        if random.random() > 0.5: chosen_lit = -chosen_lit
                        return chosen_lit
