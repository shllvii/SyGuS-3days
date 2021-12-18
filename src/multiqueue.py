from functools import reduce
from utils import log
from utils.sortedcollections import SortedDict

class queue:
  def __init__(self, productions) -> None:
    self.productions = productions
    self.queues = SortedDict()
    self.count = 0
  
  def empty(self) -> bool:
    if len(self.queues) == 0:
      return True
    empty = reduce(lambda a, b : a and b, [not bool(item[1]) for item in self.queues.items()])
    return empty
  
  def countNonTerminal(self, prog) -> int:
    count = 0
    for term in prog:
      if type(term) == list:
        count += self.countNonTerminal(term)
      elif term == tuple:
        continue
      elif term in self.productions:
        count += 1
    return count

  def countLength(self, prog) -> int:
    if len(prog) > 1:
      count = 1
    else:
      count = 0
    for term in prog:
      if type(term) == list:
        count += self.countLength(term)
    return count

  def countDepth(self, prog) -> int:
    if len(prog) > 1:
      delta = 1
    else:
      delta = 0
    depth = 0
    for term in prog:
      if type(term) == list:
        depth = max(depth, self.countDepth(term))
    return depth + delta
  
  def getBucket(self, length : int, depth : int, numNonTerminal : int) -> int:
    lengthID = length
    terminalID = numNonTerminal
    depthID = depth
    return (lengthID * 4) + (terminalID * 2) + (depthID)

  def push(self, prog, length : int = -1, numNonTerminal : int = -1, depth : int = -1):
    if length < 0:
      length = self.countLength(prog)
    if numNonTerminal < 0:
      numNonTerminal = self.countNonTerminal(prog)
    if depth < 0:
      depth = self.countDepth(prog)

    bucket = self.getBucket(length, depth, numNonTerminal)
    if not bucket in self.queues:
      self.queues[bucket] = []
    self.queues[bucket].append(prog)

    self.count += 1

  def pop(self):
    for k, v in self.queues.items():
      if bool(v):
        ret = v.pop(0)
        if not bool(v):
          self.queues.pop(k)
        return ret, k
      else:
        self.queues.pop(k)
  
if __name__ == '__main__':
  # remove `log` before testing
  q = queue(None)
  q.push([2], 1, 2, 1)
  q.push([1], 2, 1, 1)
  print(q.empty())
  print(q.pop())
  q.pop()
  print(q.empty())
  
  print(q.getBucket(3, 2, 1))

