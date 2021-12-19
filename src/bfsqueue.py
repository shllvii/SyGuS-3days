import heapq

class queue:
  class queueItem:
    def __init__(self, key, value):
      self.key = key
      self.value = value
    def __lt__(self, other): 
      return self.key < other.key
    def asTuple(self):
      return self.key, self.value

   
  def __init__(self, productions) -> None:
    self.productions = productions
    self.queue = []
    self.count = 0
  
  def empty(self) -> bool:
    return not bool(self.queue)
  
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
    heapq.heappush(self.queue, queue.queueItem(bucket, prog))

    self.count += 1

  def pop(self):
    return heapq.heappop(self.queue).asTuple()
  
if __name__ == '__main__':
  q = queue(None)
  q.push([2], 1, 2, 1)
  q.push([1], 2, 1, 1)
  print(q.empty())
  print(q.pop())
  q.pop()
  print(q.empty())
  
  print(q.getBucket(3, 2, 1))

