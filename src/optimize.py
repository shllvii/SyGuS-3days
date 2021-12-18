from z3.z3 import Bool

class Opt:
  productions = []
  def determined(prog) -> bool:
    ret = True
    if type(prog) == list:
      for i in range(1, len(prog)):
        ret = ret and Opt.determined(prog[i])
    else:
      if prog in Opt.productions:
        ret = False
    return ret

  def flatten(term, op : str):
    ret = []
    retBool = False
    if type(term) == list:
      if term[0] == op:
        for i in range(len(term)):
          lis, bo = Opt.flatten(term[i], op)
          retBool = retBool or bo
          ret.extend(lis)
      else:
        val, bo = Opt.reduceHash(term)
        retBool = retBool or bo
        ret.append(val)
    else:
      val, bo = Opt.reduceHash(term)
      retBool = retBool or bo
      ret.append(val)
    return ret, retBool

  def reduceHash(prog) -> tuple:
    hash_ret = 0
    retBool = False
    if type(prog) == list:
      if len(prog) > 1:
        if prog[0] in ["+", "*", "and", "or"]:
          hash_list = []
          for i in range(1, len(prog)):
            lis, bo = Opt.flatten(prog[i], prog[0])
            retBool = retBool or bo
            hash_list.extend(lis)
          hash_list.sort()
          hash_ret = hash(str([prog[0]] + hash_list))

        else:
          exp = []
          for i in range(1, len(prog)):
            val, bo = Opt.reduceHash(prog[i])
            retBool = retBool or bo
            exp.append(val)
          op = prog[0]
          hash_list = [op] + exp
          hash_ret = hash(str(hash_list))

          if op in ["<", "<=", ">", ">=", "="] and Opt.determined(prog[1]) and Opt.determined(prog[2]) and exp[0] == exp[1]:
            retBool = True
          if op in ["ite"] and Opt.determined(prog[2]) and Opt.determined(prog[3]) and exp[1] == exp[2]:
            retBool = True 
      else:
        hash_ret, retBool = Opt.reduceHash(prog[0])
    elif type(prog) == tuple:
      hash_ret, retBool = hash(str(prog)), False
    else:
      hash_ret, retBool = hash(prog), False
    return hash_ret, retBool

if __name__ == "__main__":
  print(Opt.reduceHash(["+", "x", ["+", "y", ["*", "z", "a"]]]))
  print(Opt.reduceHash(["+", ["+", "x", ["*", "a", "z"]], "y"]))