file = open('dataset.txt', 'r')
data = file.read().split('\n')
file.close()

n = int(data[0])
adj_list = [[int(k) for k in x.split(' ')] for x in data[1:]]

def debugPrint(adj, group):
    for i in range(len(adj)):
        print '%3d %8s %s' % (i, adj[i], group[i])

# Create an adjacency list such that for each i, 
# A[i] describes all nodes adjacent to it
adj = [[] for i in range(n)]
    
for pair in adj_list:
    a = pair[0]-1
    b = pair[1]-1
    
    if a not in adj[b]:
        adj[b].append(a)
    if b not in adj[a]:
        adj[a].append(b)
        

# Find all distinct groups
# Initialize - all nodes have no group
group = [None for i in range(n)]

# As long as some node has no group:
#   Assign a group to that node
#   Assign that group to every node it is adjacent to
# Groups serves as both a group marker and a counter of the
# number of groups
def recursiveGroupFill(adj, group, groupNum, i):
    group[i] = groupNum
    for k in adj[i]:
        if group[k] == None:
            group = recursiveGroupFill(adj, group, groupNum, k)
    return group

groups = 0
while None in group:
    groups += 1
    
    i = group.index(None)
    group = recursiveGroupFill(adj, group, groups, i)
    
# We now have k groups, so we need k-1 edges to connect all of them
result = groups-1
print result

outfile = open('result.txt', 'w')
outfile.write(str(result))
outfile.close()
