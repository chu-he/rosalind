class Node():
    def __init__(self, parent=None):
        self.name = ''
        self.parent = parent
        self.children = []
        self.weight = 1
        self.splits = ''
        
    def __str__(self, indentation=''):
        s = f'{indentation}{self.name if self.name else "(No name)"}  {self.weight}  {self.splits}\n'
        indent_child = indentation + '  '
        for child in self.children:
            s += child.__str__(indentation=indent_child)
        return s
        
    def find_distance(self, name, source):
        #print(f'Finding distance from {self.name} to {name}')
        if self.name == name:
            return 0
            
        distances = []
        # When travelling to a child, add the child's weight
        for child in self.children:
            if child == source:
                pass
            else:
                distances.append(child.weight + child.find_distance(name, self))
                
        # When travelling to a parent, add own weight
        if self.parent and self.parent != source:
            distances.append(self.weight + self.parent.find_distance(name, self))
        
        if len(distances) == 0: return 99999
        
        return min(distances)
        
    def calculate_size(self, ignore=None):
        size = 1 + sum([child.calculate_size(ignore=self) for child in self.children if child != ignore])
        size += self.parent.calculate_size(ignore=self) if self.parent and self.parent != ignore else 0
        return size
        
    def assign_tree_split(self, split, ignore=None):
        self.splits += str(split)
        for child in self.children:
            if child != ignore:
                child.assign_tree_split(split, ignore=self)
        if self.parent and self.parent != ignore:
            self.parent.assign_tree_split(split, ignore=self)

class Graph():
    def __init__(self, graph_text):
        print(f'Building graph from {graph_text}')
        self.root = Node()
        self.current_node = self.root
        self.current_child = Node(parent=self.current_node)
        self.current_node.children.append(self.current_child)
        
        self.node_map = {}
        
        self.all_nodes = [self.current_child]
        
        self.current_name = ''
        
        for char in graph_text:
            
            # Open parentheses - go one level deeper
            if char == '(':
                #print(f'Entering child node')
                self.current_node = self.current_child
                self.current_child = Node(parent=self.current_node)
                self.current_node.children.append(self.current_child)
                self.all_nodes.append(self.current_child)
                
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
                self.all_nodes.append(self.current_child)
                
            # Letter - add to the current name
            elif char.isalpha() or char == '_':
                if self.current_child.name: self.node_map.pop(self.current_child.name)
                self.current_child.name += char
                self.node_map[self.current_child.name] = self.current_child
                #print(f'Name is now {self.current_child.name}')

            # Digit - append to weight
            elif char.isdigit():
                self.current_child.weight *= 10
                self.current_child.weight += int(char)
                
            # Colon will fall here - ignore
            else:
                if char != ':': print(f'Unrecognized character |{char}|')
                pass
                
    def __str__(self):
        return self.root.__str__()
        
    def find_distance(self, a, b):
        node_a = self.node_map[a]
        return node_a.find_distance(b, None)
        
    def get_nodes_lex(self):
        keys = list(self.node_map.keys())
        keys.sort()
        return keys
        
    def get_splits(self, a):
        return self.root.children[0].find_distance(a, None) - 1
        
    def get_all_nodes(self):
        return sorted([child.name for child in self.all_nodes if child.name])
        
    def determine_splits(self):
        nodes = [child for child in self.all_nodes]
        for node in nodes:
            # Pretend to disconnect this node from the tree - how big is it, and the remainder?
            child_tree_size  = node.calculate_size(ignore=node.parent)
            parent_tree_size = node.parent.calculate_size(ignore=node)
            
            #print(f'{node.name} - Tree size {child_tree_size} - Parent Tree size {parent_tree_size}')
            
            if child_tree_size > 1 and parent_tree_size > 1:
                node.assign_tree_split(       split=1, ignore=node.parent)
                node.parent.assign_tree_split(split=0, ignore=node)
                
    def get_splits(self):
        splits = ''
        named_nodes = sorted([child for child in self.all_nodes if child.name], key=lambda x: x.name)
        for split_row in range(len(self.root.splits)):
            splits += ''.join([node.splits[split_row] for node in named_nodes]) + '\n'
        return splits
                

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        data = fp.read().split('\n')
        
    results = []
        
    # Strip the ending semicolon
    graph_text = data[0][:-1]
    
    graph = Graph(graph_text)
    
    #print(graph)
    
    keys = graph.get_nodes_lex()
    
    graph.determine_splits()
    
    #print(graph)
        
    result = graph.get_splits()
    
    print(result)
    
    with open('result.txt', 'w') as fp2:
        fp2.write(result)