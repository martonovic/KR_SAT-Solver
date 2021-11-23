from collections import *
import random

def random_heuristic(variables):
    random.shuffle(variables)
    flip = 1
    for varb in variables:
        if flip == 1:
            variables[variables.index(varb)] = -varb
        flip = -flip
    random.shuffle(variables)

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


def DLIS_heuristic(clauses):
    neg_count = defaultdict(int)
    pos_count = defaultdict(int)

    for clause in clauses:
        for literal in clause:
            if literal < 0:
                neg_count[literal] += 1
            else:
                pos_count[literal] += 1


    neg_chosen_literal = max(neg_count, key=neg_count.get)
    pos_chosen_literal = max(pos_count, key=pos_count.get)

    if pos_count[pos_chosen_literal] > neg_count[neg_chosen_literal]:
        return pos_chosen_literal
    else:
        return neg_chosen_literal

def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

def str_base(number, base):
    while number > 0:
        number, digit = divmod(number, base)
        yield digit_to_char(digit)

def sudo_heruistic(assignments, variables, base=9):
    if base > 10:
        tmp_assignments = [str_base(abs(x), base+1) for x in assignments]
    else:
        tmp_assignments = [str(abs(w)) for w in assignments]

    row_count = [[i[0] for i in tmp_assignments].count(str(y)) for y in range(1, base+1)]
    col_count = [[j[1] for j in tmp_assignments].count(str(z)) for z in range(1, base+1)]

    row_min = min(row_count)
    col_min = min(col_count)

    if row_min < col_min:
        row_ind = row_count.index(row_min)
        col_val_inds = sorted(zip(col_count,range(base)))

        for k in col_val_inds:
            rand_select = list(range(1, base + 1))
            random.shuffle(rand_select)
            for l in rand_select:
                chosen_lit = int(str(row_ind+1) + str(k[1]+1) + str(l))
                if chosen_lit in variables:
                    if random.random() > 0.5: chosen_lit = -chosen_lit
                    print(chosen_lit)
                    break
            if chosen_lit in variables: break


    else:
        col_ind = col_count.index(col_min)
        row_val_inds = sorted(zip(row_count,range(base)))

        for k in row_val_inds:
            rand_select = list(range(1, base + 1))
            random.shuffle(rand_select)
            for l in rand_select:
                chosen_lit = int(str(k[1]+1) + str(col_ind+1) + str(l))
                if chosen_lit in variables:
                    if random.random() > 0.5: chosen_lit = -chosen_lit
                    print(chosen_lit)
                    break
            if chosen_lit in variables: break


    return chosen_lit
