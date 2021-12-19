from .optimize import Opt
from .multiqueue import queue
from .preprocess import reduce
from utils import log
from utils import Extend
import utils.translator as translator

def solve(fnName, fnDef, productions, checker):
  try:
    productions = reduce(fnName, productions)
    Opt.productions = productions
    
    startSym = 'Start'  # starting symbol

    bfsQueue = queue(productions)
    bfsQueue.push([startSym], 0, 1, 0)
    
    hashSet = set([Opt.reduceHash([startSym])])
    count = 0
    while (not bfsQueue.empty()):
      key, prog = bfsQueue.pop()

      count += 1

      exts = Extend(prog, productions)

      if(len(exts) == 0):  # Nothing to extend
        # use Force Bracket = True on function definition. MAGIC CODE. DO NOT MODIFY THE ARGUMENT ForceBracket = True.
        fnDefStr = translator.toString(fnDef, ForceBracket=True)
        progStr = translator.toString(prog)

        # insert Program just before the last bracket ')'
        candidate = fnDefStr[:-1] + ' ' + progStr + fnDefStr[-1]
        log("candidate", candidate, level=0)
        counterexample = checker.check(candidate)

        if(counterexample == None):  # No counter-example
          log('Got answer {0}'.format(count), level=1)
          return candidate

      for ext in exts:
        hsh, bad = Opt.reduceHash(ext)
        if (not bad) and (not hsh in hashSet):
          bfsQueue.push(ext)
          hashSet.add(hsh)
        # else:
        #   print("bad", ext)
  except:
    log("damn", level=1)
    return None

  assert("No answer")