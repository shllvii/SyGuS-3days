import sys
from typing import *

from src import search
from src import pattern
from src import construct
from utils.logger import log
from utils.scripts import *
import utils.translator as translator

if __name__ == '__main__':
  bmExpr = parseInput(sys.argv[1])
  checker, constraints = translator.ReadQuery(bmExpr)
  fnExpr, fnDef = getSynFn(bmExpr)

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
