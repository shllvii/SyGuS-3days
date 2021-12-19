n = 50
value = 50
idxs = [str(i) for i in range(n+1)] + [str(value)]
idxs_str = " ".join(idxs)
args = ['x'+ str(i) for i in range(1, n+1)] + ["k"]

args_str = ' '.join(args)
print(args_str)

args_list_str = ' '.join(["(" + x + " Int" + ")" for x in args])
print(args_list_str)

args_decl_str = '\n'.join(['(declare-var ' + x + ' Int)' for x in args])
print(args_decl_str)

def seq_gen(lis):
  if len(lis) == 2:
    return '(< ' + lis[0] + ' ' + lis[1] + ')'
  return '(and (< ' + lis[0] + ' ' + lis[1] + ') ' + seq_gen(lis[1:]) + ')'

seq_str = seq_gen(args[:-1])
print(seq_str)

def rbound(x):
  return "(> (+ k " + x + ") " + str(value) + ")"
def lbound(x):
  return "(< (+ k " + x + ") " + str(value) + ")"

func_call_str = '(findIdx ' + args_str + ')'
print(func_call_str)

def constraintx(lx=None, rx=None, idx=None):
  ret = '(constraint (=> ' + seq_str + ' (=>'
  pre = ''
  if lx == None:
    pre = rbound(rx)
  elif rx == None:
    pre = lbound(lx)
  else:
    pre = '(and ' + lbound(lx) + ' ' + rbound(rx) + ')'
  
  ret += ' ' + pre + ' '
  pro = '(= ' + func_call_str + ' ' + str(idx) + ')'
  ret += ' ' + pro + ')))\n'
  return ret

constraints = constraintx(None, args[0], 0)
for idx in idxs[1:-1]:
  constraints += constraintx(lx=args[int(idx)-1], rx=args[int(idx)] if int(idx)  < n else None, idx=idx)

with open('array_search_plus.sl', 'w') as f:
  f.write('(set-logic LIA)\n')
  f.write('(synth-fun findIdx (' + args_list_str +') Int ((Start Int ( ' + idxs_str + ' ' + args_str + ' (+ Start Start) (ite BoolExpr Start Start))) (BoolExpr Bool ((< Start Start) (<= Start Start) (> Start Start) (>= Start Start)))))\n')
  f.write(args_decl_str + '\n')  
  f.write(constraints)
  f.write('(check-synth)')

  



