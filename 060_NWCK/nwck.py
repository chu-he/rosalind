class Node():
    def __init__(self, parent=None):
        self.name = ''
        self.parent = parent
        self.children = []
        
    def __str__(self, indentation=''):
        s = indentation + (self.name if self.name else '(No name)') + '\n'
        indent_child = indentation + '  '
        for child in self.children:
            s += child.__str__(indentation=indent_child)
        return s
        
    def find_distance(self, name, source):
        print(f'Finding distance from {self.name} to {name}')
        if self.name == name:
            return 0
        neighbors = self.children.copy()
        if self.parent: neighbors.append(self.parent)
        if source in neighbors: neighbors.remove(source)
        
        if len(neighbors) == 0: return 999
        
        return 1 + min([n.find_distance(name, self) for n in neighbors])

class Graph():
    def __init__(self, graph_text):
        print(f'Building graph from {graph_text}')
        self.root = Node()
        self.current_node = self.root
        self.current_child = Node(parent=self.current_node)
        self.current_node.children.append(self.current_child)
        
        self.node_map = {}
        
        self.current_name = ''
        
        for char in graph_text:
            
            # Open parentheses - go one level deeper
            if char == '(':
                #print(f'Entering child node')
                self.current_node = self.current_child
                self.current_child = Node(parent=self.current_node)
                self.current_node.children.append(self.current_child)
                
            # Close parentheses - go one level up
            elif char == ')':
                #print(f'Returning to parent node')
                self.current_child = self.current_node
                self.current_node = self.current_node.parent
                
            # Comma - finish working on the current child, and create a new one
            elif char == ',':
                #print(f'Completed node {self.current_child.name}, creating new')
                self.current_child = Node(parent=self.current_node)
                self.current_node.children.append(self.current_child)
                
            # Letter - add to the current name
            else:
                if self.current_child.name: self.node_map.pop(self.current_child.name)
                self.current_child.name += char
                self.node_map[self.current_child.name] = self.current_child
                #print(f'Name is now {self.current_child.name}')
                
    def __str__(self):
        return self.root.__str__()
        
    def find_distance(self, a, b):
        node_a = self.node_map[a]
        return node_a.find_distance(b, None)
                

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        data = fp.read().split('\n')
        
    results = []
        
    while data:
        # Strip the ending semicolon
        graph_text = data[0][:-1]
        a, b = data[1].split(' ')
        
        graph = Graph(graph_text)
        distance = graph.find_distance(a, b)
        
        print(graph)
        print(distance)
        
        results.append(distance)
        
        data = data[3:]
        
    result = ' '.join([str(x) for x in results])
    print(result)
    
    with open('result.txt', 'w') as fp2:
        fp2.write(result)