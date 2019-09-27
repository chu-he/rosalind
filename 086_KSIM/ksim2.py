import datetime
    
#TEST_MODE = True
TEST_MODE = False

class Possibility:
    def __init__(self, start_index):
        self.start_index = start_index
        
        self.pattern_index = 0
        self.edit_distance = 0
        self.match_length = 0
        self.ends_in_gap = False
        
        global TEST_MODE
        if TEST_MODE:
            self.a = []
            self.b = []
        
    def done(self):
        global pattern_size
        return self.pattern_index == pattern_size
        
    def good(self):
        global max_edit
        return self.edit_distance <= max_edit
        
    def copy(self):
        other = Possibility(self.start_index)
        other.pattern_index = self.pattern_index
        other.edit_distance = self.edit_distance
        other.match_length = self.match_length
        other.ends_in_gap = self.ends_in_gap
        
        global TEST_MODE
        if TEST_MODE:
            other.a = self.a[:]
            other.b = self.b[:]
            
        return other
        
    def __str__(self):
        return f'{self.start_index} | Edit: {self.edit_distance} | Match: {self.match_length} | {"".join(self.a)} x {"".join(self.b)}'
    
def motifs(a, b, k):
    global TEST_MODE
    print(f'{len(a)} - {len(b)}')
    
    global pattern_size
    pattern_size = len(a)
    
    global max_edit
    max_edit = k
    
    possibilities = []
    result = set()
    
    def evaluate(new_p, result, new_possibilities):
        if new_p.done():
            if new_p.good():
                result.add( (new_p.start_index+1, new_p.match_length) )
        else:
            if new_p.good():
                new_possibilities.append(new_p)
            else:
                if TEST_MODE:
                    print(f'Exceeded edit distance limit: {str(new_p)}')
                    
    def append_gaps(new_p, result, new_possibilities):
        # Don't append more gaps if the previous possibility already ended in gaps
        if new_p.ends_in_gap:
            return
            
        global TEST_MODE
        
        new_p = new_p.copy()
        
        while new_p.edit_distance+1 <= max_edit and not new_p.done():
            new_p.edit_distance += 1
            
            if TEST_MODE:
                new_p.a.append(a[new_p.pattern_index])
                new_p.b.append('-')
                
            new_p.pattern_index += 1
            new_p.ends_in_gap = True
            evaluate(new_p, result, new_possibilities)
            
            new_p = new_p.copy()
    
    last_i = 0
    t = datetime.datetime.now()
    for i, b_ch in enumerate(b):
    
        if i % 1 == 0:
            last_i = i
            tn = datetime.datetime.now()
            print(f'{i} - {tn - t}')
            t = tn
            
        if TEST_MODE:
            print(f'\n{i}')
            
        new_possibilities = []
        
        # Start a new possibility here
        p = Possibility(i)
        possibilities.append(p)
        
        # Modify old possibilities
        for p in possibilities:
            # Leading gaps
            append_gaps(p, result, possibilities)
            
            # Match at current character
            new_p = p.copy()
            new_p.edit_distance += (0 if a[new_p.pattern_index] == b_ch else 1)
            new_p.match_length += 1
            
            if TEST_MODE:
                new_p.a.append(a[new_p.pattern_index])
                new_p.b.append(b_ch)
                
            new_p.pattern_index += 1
            new_p.ends_in_gap = False
            evaluate(new_p, result, new_possibilities)
            
            # Gap in a
            new_p = p.copy()
            new_p.edit_distance += 1
            new_p.match_length += 1
            
            if TEST_MODE:
                new_p.a.append('-')
                new_p.b.append(b_ch)
                
            new_p.ends_in_gap = False
            evaluate(new_p, result, new_possibilities)
                    
        possibilities = new_possibilities
        
        if TEST_MODE:
            for p in possibilities:
                print(str(p))
    
    return result
            
        
def write_result(result):
    with open('result.txt', 'w') as fp:
        fp.write(result)

if __name__=="__main__":
    with open('dataset.txt', 'r') as fp:
        k, s, t = fp.read().split('\n')
        
    k = int(k)
       
    substrings = motifs(s, t, k)
    
    result = '\n'.join([f'{r} {l}' for r, l in substrings])
    print(result)
    
    write_result(result)