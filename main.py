import sys
from typing import *

from baseline import top_down
from utils.logger import log
from utils.scripts import *
import utils.translator as translator

if __name__ == '__main__':
  bmExpr = parseInput(sys.argv[1])
  checker = translator.ReadQuery(bmExpr)
  fnExpr, fnDef = getSynFn(bmExpr)

  log("fnExpr(", len(fnExpr), "): ", fnExpr)


  symTypes = {product[0]:product[1] for product in fnExpr[4]}
  productions = {product[0]:product[2] for product in fnExpr[4]}  

  ans = top_down.solve(fnDef, productions, checker)

  print(ans)
