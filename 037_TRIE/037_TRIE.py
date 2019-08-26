nIndex = 1

class Node:
    def __init__(self):
        global nIndex
        
        # A list of EDGES that lead to this node's child nodes
        self.childEdges = []
        
        # This node's index
        self.value = nIndex
        nIndex += 1
        
        ###print ' Node created with index %d' % self.value
    
class Edge:
    def __init__(self, v, d):
        # This edge's value
        self.chr = v
        
        # The NODE that this edge leads to
        self.dest = d
        
        ###print 'Edge created with value %s leading to node %d' % (self.chr, self.dest.value)
        
def buildTrie(node, s):
    ch = s[0]
    rest = s[1:]
    
    gotoNode = None
    # If ch is already an edge, move to that destination node
    for edge in node.childEdges:
        if edge.chr == ch:
            gotoNode = edge.dest
            
    # Otherwise, create that node
    if gotoNode == None:
        n = Node()
        e = Edge(ch, n)
        node.childEdges.append(e)
        gotoNode = n
        
    if rest != '': buildTrie(gotoNode, rest)
    
def printTrie(node, str):
    for edge in node.childEdges:
        str += '%d %d %s\n' % (node.value, edge.dest.value, edge.chr)
        str = printTrie(edge.dest, str)
    return str

file = open('dataset.txt', 'r')
data = file.read().split('\n')
file.close()

root = Node()

for s in data:
    buildTrie(root, s)
    
result = printTrie(root, '')
print result

outfile = open('result.txt', 'w')
outfile.write(result)
outfile.close()