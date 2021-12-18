from z3.z3 import Product

from utils import translator

from .preprocess import reduce

def getMaxN(str) -> int:
  maxGen.name = str
  return int(str[3:])

class maxGen:

  def generate(n, mx, args):
    if n == 1:
      return mx
    else:
      if mx == -1:
        a, b, nx = args[0], args[1], 2
      else:
        a, b, nx = mx, args[0], 1
      return ['ite', ['<=', a, b], maxGen.generate(n-1, b, args[nx:]), maxGen.generate(n-1, a, args[nx:])]
    return None

  def solve(fnName, fnDef, productions, checker):
    # n = getMaxN(fnName)
    productions = reduce(maxGen.name, productions)
    args = productions['Arg']
    n = len(args)
    prog = maxGen.generate(n, -1, args)
    fnDefStr = translator.toString(fnDef, ForceBracket=True)
    progStr = translator.toString(prog)
    candidate = fnDefStr[:-1] + ' ' + progStr + fnDefStr[-1]
    counterexample = checker.check(candidate)
    assert(counterexample==None)
    return candidate