def parseargs(inputfile):
    args = []
    file = open(inputfile, "r")
    rules = file.read()
    lines = rules.split('\n')
    for line in lines:
        if line.startswith('c'): continue
        elif line.startswith('p'):
            info = line.split(' ')
            numVarbs = info[2]  # these two could be interesting for evaluating heuristics and hardness
            numClauses = info[3]  # <--
        elif not line.strip(): continue
        else:
            line = line[:-2]
            arg = getLiterals(line)
            args.append(arg)

    return args


def getLiterals(clause):
    if clause:
        literals = clause.split(' ')
        literals = [int(lit) for lit in literals]
    else:
        literals = []
    return literals


def getVars(args):
    #  initialize variables
    varbs = []
    varbsCount = []

    for literals in args:
        for lit in literals:
            # for each literal in a clause, see if the integer has already been added to variable list
            # important to see if a specific value is a pure literal or if there are any unit clauses
            if lit not in varbs:
                varbs.append(lit)
                varbsCount.append(1)
            else:
                varbsCount[varbs.index(lit)] += 1

    variablesList = [abs(variables) for variables in varbs]
    variablesList = list(set(variablesList))
    return variablesList, varbsCount, varbs


