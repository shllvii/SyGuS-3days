import pprint
from utils import translator

from utils.logger import log


handleException=True
funcName = ''
arg_list = []

def includeFunc(term):
  if type(term) == list:
    if term[0] == funcName:
      return True
    else:
      for x in term[1:]:
        if includeFunc(x):
          return True
  return False

def isFunc(term):
  return type(term) == list and term[0] == funcName

def isAssign(term):
  return type(term) == list and term[0] == '=' and isFunc(term[1])

def illegal(fnDef, constraints):
  def illegalOne(constraint):
    if not type(constraint) == list:
      return False
    op = constraint[0]
    badOps = ['=>']
    if op in badOps:
      return True
    numInclude, numIs = 0, 0
    for term in constraint[1:]:
      if illegalOne(term): 
        return True
      if includeFunc(term):
        numInclude += 1
      if isFunc(term):
        numIs += 1
    if numIs > 0 and numInclude > 1:
      return True
    elif numIs == 1 and op != '=':
      return True
    else:
      return False

  if fnDef[3][0] == 'BitVec':
    return True
  for _, constraint in constraints:
    if illegalOne(constraint):
      return True
  return False

def extractArgs(fnDef):
  global arg_list 
  arg_list = [x[0] for x in fnDef[2]]

def modifyConstraints(constraints):
  def extractVals(constraint):
    term = constraint[1]
    if type(term[1]) == tuple:
      return ['or', ['not', ['=', arg_list[0], term[1]]], ['=', [funcName, *arg_list], constraint[2]]]
    else:
      return constraint
  return [extractVals(constraint) if constraint[0]=='=' else constraint for _, constraint in constraints]

def flattenConstraints(constraints):
  def flattenWithOp(constraint, opTarget):
    op = constraint[0]
    ret = []
    if op == opTarget:
      for term in constraint[1:]:
        ret += flattenWithOp(term, op)
    else:
      ret.append(constraint)
    return ret

  def flattenConstraint(constraint):
    op = constraint[0]
    opSet = ['and', 'or']
    ret = [op]
    if op in opSet:
      for term in constraint[1:]:
        ret += flattenWithOp(term, op)
      return ret
    else:
      return constraint

  return [flattenConstraint(constraint) for constraint in constraints]

def mergeConstraints(constraints): 
  if (len(constraints) > 1):
    return ['and'] + [constraint for constraint in constraints]
  else:
    return constraints[0]

def extractAssign(expr):
  ret = []
  def traverse(expr, lis):
    if type(expr) != list:
      return
    if isAssign(expr):
      ret.append((expr, lis))
    else:
      noFunc = [term for term in expr[1:] if not includeFunc(term)]
      new_lis = lis + noFunc if expr[0] == "and" else \
                lis + [['not', term] for term in noFunc]
      for term in expr[1:]:
        if includeFunc(term):
          traverse(term, new_lis)

  traverse(expr, [])
  return ret

def construct(assigns):
  def getAssign(assign):
    return assign[2]

  def getCond(cond):
    if type(cond) == list:
      if len(cond) >= 3 and type(cond[2]) == tuple and cond[2][1] == 5:
        return getCond([cond[0], ['+', cond[1], cond[1]], (cond[2][0], 10)])
      if cond[0] == '>':
        return ['and', ['>=', cond[1], cond[2]], ['not', ['=', cond[1], cond[2]]]]
      if cond[0] == '<':
        return ['and', ['<=', cond[1], cond[2]], ['not', ['=', cond[1], cond[2]]]]
      if cond[0] == 'and' or cond[0] == 'or':
        def split(op, terms):
          if len(terms) == 1:
            return getCond(terms[0])
          else:
            return [op, getCond(terms[0]), split(op, terms[1:])]
          
        return [cond[0], getCond(cond[1])] + split(cond[0], cond[2:])
      else:
        return [cond[0]] + [getCond(x) for x in cond[1:]]
    else:
      return cond

  def getCondAssign(assign, cond):
    return getAssign(assign)
  
  def andAll(conds):
    if len(conds) > 1:
      return ['and'] + conds
    else:
      return conds[0]

  if len(assigns) == 1:
    assign, cond = assigns[0] 
    return getCondAssign(assign, cond)
  else:
    assign, conds = assigns[0] 
    cond = andAll(conds)
    return ['ite', getCond(cond), getAssign(assign), construct(assigns[1:])]

def solve(fnName, fnDef, productions, constraints, checker):
  fnDefStr = translator.toString(fnDef, ForceBracket=True)
  def passCheck(prog):
    progStr = translator.toString(prog)
    candidate = fnDefStr[:-1] + ' ' + progStr + fnDefStr[-1]
    counterexample = checker.check(candidate)
    return candidate if counterexample == None else None

  global funcName
  funcName = fnName

  try:
    if illegal(fnDef, constraints):
      return None
    else:
      log('Solved by \'construct\'', level=1)
    extractArgs(fnDef)
    modified = modifyConstraints(constraints)
    flattened = flattenConstraints(modified)
    constraints = mergeConstraints(flattened)
    pprint.pprint(constraints)
    assigns = extractAssign(constraints)
    pprint.pprint(assigns)
    prog = construct(assigns)
    pprint.pprint(prog)
    ans = passCheck(prog)
    return ans
  except :
    log("construct failed", level=1)
    return None
  return None

