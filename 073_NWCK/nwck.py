import re

class Node():
    def __init__(self, name='', parent=None):
        self.name = name
        self.children = []
        self.parent = parent
        
    def add_node(self, node_name):
        self.children.append(Node(name=node_name, parent=self))

def parse_tree(tree_text, parent):
    while tree_text:
        print(tree_text)
        match = re.match(r'^(\w+)(.*)$', tree_text)
        if match:
            parent.add_node(match.group(1))
            tree_text = match.group(2)
            print(f'Created child node {match.group(1)}')
            
            if tree_text[0] == ',': tree_text = tree_text[1:]
        else:
        
            match = re.match(r'\((.*)\)(\w+)?', tree_text)
            if match:
                inside = match.group(1)
                
                n = Node()
                if match.group(2):
                    n.name = match.group(2)
                    print(f'Set node name to {n.name}')
                parse_tree(inside, n)

if __name__=='__main__':
    fp = open('dataset.txt', 'r')
    lines = fp.read().split('\n')
    fp.close()
    
    while lines:
        tree_text = lines[0]
        x, y = lines[1].split(' ')
        lines = lines[3:]
        
        tree_root = Node()
        parse_tree(tree_text[:-1], tree_root)
        
        print(tree_text)
        print(x)
        print(y)
        