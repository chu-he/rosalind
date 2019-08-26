def get_longest_common_prefix(a, b):
    lcp = ''
    for i in range(1,min(len(a), len(b))+1):
        if a[:i] == b[:i]:
            lcp = a[:i]
        else:
            break
    return lcp

class Node():
    def __init__(self, value=''):
        self.value = value
        self.children = []
        
    def add(self, value):
        print(f'Adding {value} to {self.value}')
        if self.value:
            # If own value is completely contained within the new value,
            # remove matching value and iterate downwards
            if value[:len(self.value)] == self.value:
                print(f' Own value {self.value} contained within {value}')
                value = value[len(self.value):]
                
                self.add_to_child(value)
                
            else:
                # Own value is not completely contained, but a prefix must match
                # Find the longest common prefix
                prefix = get_longest_common_prefix(self.value, value)
                print(f' Prefix {prefix} matches')
                if prefix:
                    suffix = self.value[len(prefix):]
                    new_suffix = value[len(prefix):]
                    print(f' Updating own value to {prefix}, creating children {suffix} and {new_suffix}')
                    # Old suffix child inherits this node's children
                    old_suffix_child = Node(value=suffix)
                    old_suffix_child.children = self.children
                    
                    self.children = []
                    self.children.append(old_suffix_child)
                    self.children.append(Node(value=new_suffix))
                    self.value = prefix
                    
        else:
            # Root
            self.add_to_child(value)
            
    def add_to_child(self, value):
        # Find which (if any) child that has the same first char
        found_child = False
        for child in self.children:
            if not found_child:
                print(f' Checking child {child.value} <--> {value}')
                if child.value and child.value[0] == value[0]:
                    print(f' Adding {value} to child {child.value}')
                    child.add(value)
                    found_child = True
                
        # No children found - create one with the new value
        if not found_child:
            self.children.append(Node(value=value))
            print(f' Creating new child with value {value}')
            
    def get_suffixes(self):
        suffixes = []
        if self.value: suffixes.append(self.value)
        for child in self.children:
            suffixes.extend(child.get_suffixes())
        return suffixes
        
    def display(self, indentation=''):
        print(f'{indentation}{self.value}')
        for child in self.children:
            child.display(indentation=indentation+'  ')
            
    def get_all_substrings(self):
        if self.children:
            substrings = []
            for child in self.children:
                substrings.extend([self.value + x for x in child.get_all_substrings()])
        else:
            substrings = [self.value]

        #print(f'Substrings of {self.value} = {substrings}')
        return substrings

class SuffixTree():
    def __init__(self):
        self.root = Node()
        
    def add(self, value):
        self.root.add(value)
            
    def get_suffixes(self):
        return self.root.get_suffixes()
        
    def display(self):
        self.root.display()
        
    def get_all_substrings(self):
        return self.root.get_all_substrings()

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        s = fp.read()
    
    #s = s[-18:]
    s_original = s
        
    suffix_tree = SuffixTree()
    
    while s:
        print(f'\nROOT adding {s}')
        suffix_tree.add(s)
        s = s[1:]
        #suffix_tree.display()
        
        
    print(s_original)
    suffix_tree.display()
    
    substrings = suffix_tree.get_all_substrings()
    substrings_display = '\n'.join(sorted(substrings,key=len))
    print(substrings_display)
    with open('substrings.txt', 'w') as fp_sub:
        fp_sub.write(substrings_display)
        
    result = '\n'.join(sorted(suffix_tree.get_suffixes(),key=len))
    print(result)
    
    # Double check
    for i in range(0, len(s_original)):
        check_sub = s_original[i:]
        print(f'Checking {check_sub} in substrings')
        assert( check_sub in substrings )
    
    with open('result.txt', 'w') as fp2:
        fp2.write(result)