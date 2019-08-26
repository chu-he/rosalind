from nkew import *

graph = Graph('((dog:4,cat:3):74,robot:98,elephant:58)')
nodes = ['dog', 'cat', 'robot', 'elephant']
for i in range(len(nodes)-1):
    for j in range(i+1, len(nodes)):
        a = nodes[i]
        b = nodes[j]
        print(f'Distance between {a} and {b} is {graph.find_distance(a, b)}')