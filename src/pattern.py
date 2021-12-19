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

  def search_bool(terms, numOps=2):
    ret = []
    plus = ["['+', " + x + ', ' + y + ']' for x in terms for y in terms if x <= y]
    le = ["['<=', " + x + ', ' + y + ']' for x in terms for y in terms if x != y]
    plus_le = ["['<=', ['+', {0}, {1}], {2}]".format(x, y, z) for x in terms for y in terms for z in terms if x<y and x!=z and y!=z]
    # ret_expr = le + plus_le
    ret_expr = plus_le

    return ["lambda hd, args: " + expr for expr in ret_expr]

  def extends(lst, args, strategies):
    hd_ele = ['hd[{0}]'.format(id) for id in range(len(lst[0]))] if type(lst[0])==tuple else ['hd']
    arg_ele = ['args[{0}]'.format(id) for id in range(len(args))] 
    conds = search_bool(hd_ele + arg_ele, 2)
    fn_0 = ['args']
    fn_1 = ['hd[1]']
    fns = ["(0, lambda hd, args: {0})".format(x) for x in fn_0] \
        + ["(1, lambda hd, args: {0})".format(x) for x in fn_1]
    bounds = ["lambda args: {0}".format(x) for x in arg_ele]
    
    # conds = ["lambda hd, args: ['<=', ['+', args[0], hd[0]], args[2]]"]
    # fns = ['(0, lambda hd, args: args)', '(1, lambda hd, args: hd[1])']
    # bounds = ['lambda args: args[1]']
    
    for cond in conds:
      for fn0 in fns:
        for fn1 in fns:
          for bound in bounds:
            # print((lst, args, cond, fn0, fn1, bound))
            strategies.append((lst, args, eval(cond), eval(fn0), eval(fn1), eval(bound)))
            
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
    liss = [args[1:], list(zip(args[:-1], idxs[0:len(args)-1]))]#, list(zip(args[:-1], idxs[0:len(args)-1]))]
    arguments = [[args[0]], [args[-1], *idxs[len(args)-1:]]]#, [args[-1], *idxs[len(args)-1:]]]
    conds = [lambda hd, args: ['<=', hd, args[0]], lambda hd, args: ['<=', args[0], hd[0]]]#, lambda hd, args: ['<=', ['+', args[0], hd[0]], args[2]]]
    fnthen = [(0, lambda hd, args: args), (1, lambda hd, args: hd[1])]#, (0, lambda hd, args: args)]
    fnelse = [(0, lambda hd, args: [hd]), (0, lambda hd, args: args)]#, (1, lambda hd, args: hd[1])]
    bounds = [lambda args: args[0], lambda args: args[1]]#, lambda args: args[1]]

    strategies = list(zip(liss, arguments, conds, fnthen, fnelse, bounds))

    # extends(liss[0], arguments[0], strategies)
    extends(liss[1], arguments[1], strategies)

    for strategy in filter( \
        lambda s: ((not len(s[0]) > 18) or (s[3][0] + s[4][0] > 0)) \
              and ((not len(args)-len(idxs) < 1) or (type(s[0][0]) == tuple)) \
              # and (not type(strategy[5](strategy[1])) == tuple) \
        , strategies):
      prog = generate(*strategy)
      candidate = passCheck(prog)
      return candidate
  except:
    log("pattern failed")
    return None
  
  return None