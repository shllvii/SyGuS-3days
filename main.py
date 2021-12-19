import sys
from typing import *

from src import search
from src import pattern
from src import construct
from src import synthBV
from utils.logger import log
from utils.scripts import *
import utils.translator as translator

if __name__ == '__main__':
  bmExpr = parseInput(sys.argv[1])
  checker, constraints = translator.ReadQuery(bmExpr)
  fnExpr, fnDef = getSynFn(bmExpr)

  logicType = bmExpr[0][1];
#   if (logicType == 'BV'):
#     ans = synthBV.solve(fnDef, constraints)
#     result = checker.check(ans)
#     if (result == None):
# #     log("BV OK", level=1)
#       print(ans)
  
  log("fnExpr(", len(fnExpr), "): ", fnExpr)


  symTypes = {product[0]:product[1] for product in fnExpr[4]}
  productions = {product[0]:product[2] for product in fnExpr[4]}  

  ans = construct.solve(fnExpr[1], fnDef, productions, constraints, checker)
  # ans = None
  if ans == None:
    ans = pattern.solve(fnExpr[1], fnDef, productions, checker)
    if ans != None:
      log("pattern gives the answer", level=1)
    else:
      ans = search.solve(fnExpr[1], fnDef, productions, checker)

  print(ans)
