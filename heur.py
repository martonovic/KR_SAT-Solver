from dependencies import *

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

def sudo_heruistic(assignments, base=10):
    if base == 16:
        assignments = [str_base(x, base+1) for x in assignments]
    next_literal = assignments[-1]
    return next_literal
