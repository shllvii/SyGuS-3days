from utils.logger import log
from utils.scripts import Extend
import utils.translator as translator

def solve(fnDef, productions, checker):
  log(fnDef)
  log(productions)
  startSym = 'Start'  # starting symbol
  bfsQueue = [[startSym]]  # Top-down
  progSet = set([str(startSym)])

  ans = []
  while(len(bfsQueue) != 0):
    prog = bfsQueue.pop(0)
    log("extend", prog)
    exts = Extend(prog, productions)
    if(len(exts) == 0):  # Nothing to extend
      # use Force Bracket = True on function definition. MAGIC CODE. DO NOT MODIFY THE ARGUMENT ForceBracket = True.
      fnDefStr = translator.toString(fnDef, ForceBracket=True)
      progStr = translator.toString(prog)

      # insert Program just before the last bracket ')'
      candidate = fnDefStr[:-1] + ' ' + progStr + fnDefStr[-1]
      log(candidate)
      counterexample = checker.check(candidate)

      if(counterexample == None):  # No counter-example
        ans = candidate
        log('Got answer\n')
        break

    for ext in exts:
      extStr = str(ext)
      if not extStr in progSet:
        bfsQueue.append(ext)
        progSet.add(extStr)
  return ans