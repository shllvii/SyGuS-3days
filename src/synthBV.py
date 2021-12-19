import utils.translator as translator

class DecisionTree:
    def insert(self, arg, res):
        node = self.root
        for i in range(0, self.length):
            br = arg & 1
            arg = arg >> 1
            if (len(node) == 0):
                node.append(i)
                node.append([[], []])
            node = node[1][br]
        assert(len(node) == 0)
        node.append(self.length)
        node.append([res])
        
    def __init__(self, length, constraints):
        self.length = length
        self.root = []
        for constr in constraints:
            funcArg = constr[1][1][1][1]
            funcResult = constr[1][2][1]
            self.insert(funcArg, funcResult)
            
def prune(node):
    if (len(node) == 0):
        return []
    elif (len(node[1]) == 1):
        return node
        
    lchild = prune(node[1][0])
    rchild = prune(node[1][1])

    if (len(lchild) != 0 and len(rchild) != 0):
        node[1][0] = lchild
        node[1][1] = rchild
        return node
    elif (len(lchild) == 0):
        return rchild
    elif (len(rchild) == 0):
        return lchild
    
def printType(length):
    return "(BitVec " + str(length)

def genPower(sig, length):
    assert(sig >= 0)
    if (sig == 0):
        # return '#b' + '0' * (length - 1) + '1'
        return '#x' + '0' * 15 + '1'
    return '(shl1 ' + genPower(sig - 1, length) + ')'

def constructValue(value, pos, length):
    if (pos == -1):
        # return '#b' + '0' * (length - 1) + '1'
        return '#x' + '0' * 16
    elif (value & (1 << pos) != 0):
        return '(bvor ' + constructValue(value, pos - 1, length) + ' ' + \
            genPower(pos, length) + ')'
    else:
        return constructValue(value, pos - 1, length)

def genShiftR(shiftW, length):
    if (shiftW == 0):
        return 'x'
    elif (shiftW >= 16):
        return '(shr16 ' + genShiftR(shiftW - 16, length) + ')'
    elif (shiftW >= 4):
        return '(shr4 ' + genShiftR(shiftW - 4, length) + ')'
    else:
        return '(shr1 ' + genShiftR(shiftW - 1, length) + ')'
    
def genPredicate(shiftW, length):
    return '(bvand ' + genShiftR(shiftW, length) + ' ' + \
        '#x' + '0' * 15 + '1' + \
        ')'

def genFunc(length, node, inLength, outLength):
    if (len(node) == 0):
        # return '#b' + '0' * outLength
        return '#x' + '0' * 16
    curLevel = node[0]
    if (len(node[1]) == 1):
        return constructValue(node[1][0], outLength, outLength)
    elif (len(node[1]) == 2):
        return "(if0 " + genPredicate(curLevel, inLength) + ' ' + \
                genFunc(length, node[1][1], inLength, outLength) + ' ' + \
                genFunc(length, node[1][0], inLength, outLength) + \
                ")"

def solve(fnDef, constraints):
    length = fnDef[2][0][1][1][1]
    outLength = fnDef[3][1][1]
    DT = DecisionTree(length, constraints)
    DT.root = prune(DT.root)
    fnDefStr = translator.toString(fnDef, ForceBracket=True)
    return fnDefStr[:-1] + ' ' + \
        genFunc(length, DT.root, length, outLength) + \
        fnDefStr[-1]
