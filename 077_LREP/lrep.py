import re

class Node():
    def __init__(self, parent=None, sub=''):
        self.sub = sub
        self.parent = parent
        self.children = []
        
    def __str__(self, indentation=''):
        s = indentation + self.sub + '\n'
        for child in self.children:
            s += child.__str__(indentation=indentation+'  ')
        return s
        
    def get_strings(self):
        if self.children:
            suffixes = []
            for child in self.children:
                suffixes.extend(child.get_strings())
            suffixes.extend([self.sub + x for x in suffixes])
            return suffixes
        else:
            return [self.sub]

class Graph():
    def __init__(self, full_string, graph_lines):
        self.root = None
        self.node_map = {}
        
        for graph_line in graph_lines:
            a, b, location, length = graph_line.split(' ')
            location = int(location)-1
            length   = int(length)
            sub = full_string[location:location+length]
            
            # For finding repeating substrings, we can ignore any endstring
            if '$' not in sub:
            
                # Get parent from the name map
                if a in self.node_map:
                    node_a = self.node_map[a]
                else:
                    node_a = Node()
                    self.node_map[a] = node_a
                    
                # Create child node
                node_b = Node(parent=node_a, sub=sub)
                self.node_map[b] = node_b
                node_a.children.append(node_b)
                    
                # Assign root if unknown
                if self.root is None:
                    self.root = node_a
                
    def get_strings(self):
        return self.root.get_strings()
        
    def __str__(self):
        return self.root.__str__()
        
def find_longest_repeating_with_occurrences(strings, full_string, occurrences):
    for s in strings:
        # Find all occurrences, overlapping
        regex = f'(?={s})'
        match = re.findall(regex, full_string)
        if match:
            num_matches = len(match)
            if num_matches >= occurrences:
                print(f'{s} - {num_matches}')
                return s

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        lines = fp.read().split('\n')
        
    full_string = lines[0]
    occurrences = int(lines[1])
    
    graph = Graph(full_string, lines[2:])
    
    #print(graph)
    
    strings = graph.get_strings()
    # Remove dupes
    strings = list(dict.fromkeys(strings))
    strings.sort(key=len, reverse=True)
    #print('\n'.join(strings))
    
    result = find_longest_repeating_with_occurrences(strings, full_string, occurrences)
    
    print(result)
    
    with open('result.txt', 'w') as fp2:
        fp2.write(result)