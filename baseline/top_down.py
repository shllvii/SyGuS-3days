from utils import log
from utils import Extend
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
    # log(prog, len(exts), level=1)

    if(len(exts) == 0):  # Nothing to extend
      # use Force Bracket = True on function definition. MAGIC CODE. DO NOT MODIFY THE ARGUMENT ForceBracket = True.
      fnDefStr = translator.toString(fnDef, ForceBracket=True)
      progStr = translator.toString(prog)

      # insert Program just before the last bracket ')'
      candidate = fnDefStr[:-1] + ' ' + progStr + fnDefStr[-1]
      log(candidate, level=1)
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
    if len(progSet) > 50:
      progSet.clear()
  return ans