from utils import translator
from utils.logger import log
from .preprocess import reduce


def generate(*Args):
  ls, args, cond, f_then, f_else, bound = Args 
  def nextgen(fn):
    return generate(ls[1:], fn[1](ls[0], args), *Args[2:]) \
      if fn[0]==0 else fn[1](ls[0], args)

  if not bool(ls): # bound
    return bound(args)
  
  return ['ite', cond(ls[0], args), nextgen(f_then), nextgen(f_else)]

def solve(fnName, fnDef, productions, checker):
  fnDefStr = translator.toString(fnDef, ForceBracket=True)
  def passCheck(prog):
    progStr = translator.toString(prog)
    candidate = fnDefStr[:-1] + ' ' + progStr + fnDefStr[-1]
    counterexample = checker.check(candidate)
    return candidate if counterexample == None else None

  productions = reduce(fnName, productions)

  args = productions["Args"]
  idxs = productions["Literals"]


  try:
    liss = [args[1:], list(zip(args[:-1], idxs[:-1]))]
    arguments = [[args[0]], [args[-1], idxs[-1]]]
    conds = [lambda hd, args: ['<=', hd, args[0]], lambda hd, args: ['<=', args[0], hd[0]]]
    fnthen = [(0, lambda hd, args: args), (1, lambda hd, args: hd[1])]
    fnelse = [(0, lambda hd, args: [hd]), (0, lambda hd, args: args)]
    bounds = [lambda args: args[0], lambda args: args[1]]

    for strategy in zip(liss, arguments, conds, fnthen, fnelse, bounds):
      prog = generate(*strategy)
      candidate = passCheck(prog)
      if candidate != None:
        return candidate
  except:
    log("pattern failed")
  
  return None
  
  


  
    

