from typing import *
import pprint
from utils.logger import log
import utils.sexp as sexp

def stripComments(bmFile):
  noComments = '(\n'
  for line in bmFile:
    line = line.split(';', 1)[0]
    noComments += line
  return noComments + '\n)'

def parseInput(name: str):
  benchmarkFile = open(name)
  bm = stripComments(benchmarkFile)
  log(bm)

  # Parse string to python list
  bmExpr = sexp.sexp.parseString(bm, parseAll=True).asList()[0]  
  # pprint.pprint(bmExpr)
  return bmExpr

def getSynFn(bmExpr : List):
  for expr in bmExpr:
    if len(expr) == 0:
      continue
    elif expr[0] == 'synth-fun':
      fnExpr = expr
  return fnExpr, ['define-fun'] + fnExpr[1:4]

def Extend(Stmts, Productions):
  ret = []
  for i in range(len(Stmts)):
    if type(Stmts[i]) == list:
      TryExtend = Extend(Stmts[i], Productions)
      if len(TryExtend) > 0:
        for extended in TryExtend:
          ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
    elif type(Stmts[i]) == tuple:
      continue
    elif Stmts[i] in Productions:
      for extended in Productions[Stmts[i]]:
        ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
  return ret