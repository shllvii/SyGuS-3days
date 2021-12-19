from utils.pyparsing import Literal


def reduce(fnName, productions):
  new_prods = {}
  args = []
  literals = []
  lge, lg = False, False
  lgeRHS, lgRHS = None, None
  
  for k, v in productions.items():
    opset = set()
    new_v = []
    for cand in v:
      # print(cand)
      if type(cand) == list:
        if cand[0] in opset:
          continue 
        elif (cand[0] == '<=') or (cand[0] == '>=') :
          cand[0] = '<='
          lge, lgeRHS = True, cand
        elif (cand[0] == '<' ) or (cand[0] == '>'):
          cand[0] = '<'
          lg, lgRHS = True, cand
        elif cand[0] == 'bvadd':
          new_v.insert(0, cand)
        else:
          opset.add(cand[0])
          new_v.append(cand)
      else:
        new_v.append(cand)
        if not type(cand) == tuple:
          args.append(cand)
        else:
          literals.append(cand)
    
    if lge:
      new_v.append(lgeRHS)
    if lg:
      new_v.append(lgRHS)
    new_prods[k] = new_v
  
  new_prods['Args'] = args
  new_prods['Literals'] = literals

  


  # print(fnName, new_prods)
  return new_prods
