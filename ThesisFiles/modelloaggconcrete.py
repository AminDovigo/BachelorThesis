#!/usr/bin/env python
# encoding: utf -8

from pyomo.environ import *
from pyomo.opt import SolverFactory

#lettura dei dati

nb=0
nl=0
nd=0
scoreb = []
num_binl = []
signupl = []
shipl = []
hasBooklb = []

def readInput(fi_in):
    with open(fi_in) as fi:
        global nb, nl, nd, scoreb, num_binl, signupl, shipl, hasBooklb
        nb, nl, nd = [int(x) for x in fi.readline().split()]
        scoreb = [int(x) for x in fi.readline().split()]
        num_binl = [0 for x in range(nl)]
        signupl = [0 for x in range(nl)]
        shipl = [0 for x in range(nl)]
        hasBooklb = [[0 for x in range(nb)] for y in range(nl)]
        for l_index, line in enumerate(fi.readlines()):
            libraryID = int(l_index/2) 
            if ((l_index % 2) == 0):
               #num_binl[libraryID] = line.split() 
               num_binl[libraryID], signupl[libraryID], shipl[libraryID] = [int(x) for x in line.split()]
               #print(num_binl[libraryID])
               #print(signupl[libraryID])
               #print(shipl[libraryID])
            else:
                bks = [int(x) for x in line.split()]
                for x in range(num_binl[libraryID]):
                    hasBooklb[libraryID][bks[x]] = 1

def write_output(fi_out, model):
    with open(fi_out, 'w') as fo:
        spc = ' '
        endl = '\n'
        # fo.write('Asdrubale')
        tmp = sum(value(model.y[l]) for l in model.Libraries)
        fo.write(str(int(tmp)) + endl)
        for d in model.Days:
            for l in model.Libraries:
                if(inequality(0.999, model.v[l, d], 1.001)):
                    count = 0
                    books =''
                    for b in model.Books:
                        if (inequality(0.999, model.x[l, b], 1.001)):
                            count += 1
                            books += str(b) + spc
                    #tmp = sum(value(model.x[l, b]) for b in model.Books)
                    fo.write(str(l) + spc + str(count) + endl)
                    fo.write(str(books) + endl)

def obj_rule(model):
    return sum(model.score[b] * model.z[b] for b in model.Books)

def ac_rule(model, l): 
    return sum(model.v[l, d] for d in model.Days) <= model.y[l]
    
def bc_rule(model, l): 
    return sum(model.t[l, d] for d in model.Days) == model.signup[l] * model.y[l]

def cc_rule(model, l, d): 
    if ( d == 0):
        return model.t[l, 0] == model.v[l, 0]
    else:
        return model.t[l, d] - model.t[l, d - 1] <= model.v[l , d]

def dc_rule(model, d): 
    return sum(model.t[l, d] for l in model.Libraries) <= 1

def ec_rule(model, l): 
    #print(sum(model.x[l, b] for b in model.Books)) 
    #print(model.ship[l] * (nd - sum(((d + model.signup[l]) * model.v[l, d]) for d in model.Days))) 
    #print("libreria")
    return sum(model.x[l, b] for b in model.Books) <= model.ship[l] *(nd - sum(((d + model.signup[l]) * model.v[l, d]) for d in model.Days)) 
        
def fc_rule(model, l): 
    return sum(model.x[l, b] for b in model.Books) <= model.y[l] * (nd - model.signup[l]) * model.ship[l]

def gc_rule(model, b): 
    return model.z[b] <= sum(model.x[l, b] for l in model.Libraries)

def hc_rule(model, l):
    return model.y[l] <= sum(model.x[l, b] for b in model.Books)

def bf_rule(model, l, d): 
    if (d >= nd - model.signup[l]):
        return model.v[l, d] == 0
    else:
        return Constraint.Skip

def cf_rule(model, l, b): 
    return model.x[l, b] <= model.hasBook[l, b]

def buildmodel(**kwargs):
    # Model 
    model = ConcreteModel()
    # Set
    model.Libraries = RangeSet(0, nl - 1)
    model.Books = RangeSet(0, nb - 1)
    model.Days = RangeSet(0, nd - 1)
    # Params
    #model.bigM = Param(initialize=1e9)
    model.score = Param(model.Books, initialize = lambda model, b: scoreb[b])
    model.signup = Param(model.Libraries, initialize = lambda model, l: signupl[l])
    model.ship = Param(model.Libraries, initialize = lambda model, l: shipl[l])
    model.hasBook = Param(model.Libraries, model.Books, initialize = lambda model, l,b: hasBooklb[l][b], default = 0 )
    # Variables 
    model.z = Var(model.Books, domain = Binary) #se il libro è stato scelto
    model.x = Var(model.Libraries, model.Books, domain = Binary) #se il libro di quella libreria è stato scannerizzato
    model.y = Var(model.Libraries, domain = Binary) #se libreria fa il signup process
    model.t = Var(model.Libraries, model.Days, domain = Binary) #se la libreria sta impiegando il signup process
    model.v = Var(model.Libraries, model.Days, domain = Binary) #libreria comincia il signup in quel giorno
    # Objective 
    model.obj = Objective(rule=obj_rule, sense=maximize)
    # Constraints
    model.ac = Constraint(model.Libraries, rule=ac_rule)
    model.bc = Constraint(model.Libraries, rule=bc_rule)
    model.cc = Constraint(model.Libraries, model.Days, rule=cc_rule)
    model.dc = Constraint(model.Days, rule=dc_rule)
    model.ec = Constraint(model.Libraries, rule=ec_rule)
    model.fc = Constraint(model.Libraries, rule=fc_rule)
    model.gc = Constraint(model.Books, rule=gc_rule)
    model.hc = Constraint(model.Libraries, rule=hc_rule)
    model.bf = Constraint(model.Libraries, model.Days, rule=bf_rule)
    model.cf = Constraint(model.Libraries, model.Books, rule=cf_rule)
    return model

if __name__ == '__main__':
    import sys
    namefile = sys.argv[1]
    print(namefile)
    readInput(namefile)
    model = buildmodel()
    opt = SolverFactory('cplex_persistent')
    opt.set_instance(model)
    outputfile = namefile[:-4]
    outputfile += "cplex.txt"
    #res = opt.solve(tee=True, logfile = outputfile)
    res = opt.solve(tee=True)
    #solutionfile = namefile[:-4]
    solutionfile = "solution_" + namefile
    write_output(solutionfile, model)
    #for p in model.x:
    #    print("x[{}] = {}".format(p, value(model.x[p])))
    #for p in model.y:
    #    print("y[{}] = {}".format(p, value(model.y[p])))
    #for p in model.z:
    #    print("z[{}] = {}".format(p, value(model.z[p])))
    #for p in model.t:
    #    print("t[{}] = {}".format(p, value(model.t[p])))
    #for p in model.v:
    #    print("v[{}] = {}".format(p, value(model.v[p])))
    for p in model.obj:
        print("obj[{}] = {}".format(p, value(model.obj[p])))
    #with open(outputfile, "a") as f:
        #str = value(model.obj)
    #    for p in model.obj:
    #        print("obj[{}] = {}".format(p, value(model.obj[p])), file = f)
