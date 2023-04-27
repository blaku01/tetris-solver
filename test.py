import cplex

cpx = cplex.Cplex("tetris.lp")

print(cpx.variables.get_cols())