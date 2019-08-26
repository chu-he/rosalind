import re

base_pairs = { 'A': 'U',
               'U': ['A', 'G'],
               'C': 'G',
               'G': ['C', 'U'] }
match_map = { }

def find_noncrossing_matchings(s, outermost=False):
    # Do now allow nearby matches
    if len(s) <= 4:
        return 1
    
    global match_map
    if s in match_map:
        #print(f'find_noncrossing_matchings({s}) => {match_map[s]} [CACHED]')
        return match_map[s]
        
    s_orig = s
    
    # Start with 1 (no matches at all)
    matchings = 1
    
    # As long as the string is not empty...
    while s:
        if outermost:
            print(f'Length {len(s)}: {s}')
            
        # Assume the first base is matched with something
        first_base = s[0]
        # Strip the first base from the string
        s = s[1:]
        # Find all eligible matches
        match_bases = base_pairs[first_base]
        match_locations = []
        for match_base in match_bases:
            match_locations.extend([m.start() for m in re.finditer(match_base, s)])
            
        # Do not allow nearby matches
        match_locations = [m for m in match_locations if m >= 3]
        
        if outermost:
            print(f'Match locations: {match_locations}')
        
        # For each of those matches, sum the total number of possibilities
        for match_loc in match_locations:
            
            if outermost:
                print(f'Checking location {match_loc}')
            
            # The total number of possibilities for this match is equal to the
            # number of possibilities of inside matches multiplied by the number
            # of possibilities of outside matches
            inside = s[0:match_loc]
            outside = s[match_loc+1:]
            matchings += find_noncrossing_matchings(inside) * \
                         find_noncrossing_matchings(outside)
            #print(f'Crossing has inside {inside} and outside {outside}')
                         
    match_map[s_orig] = matchings
    
    #print(f'find_noncrossing_matchings({s_orig}) => {matchings}')
    return matchings

if __name__=='__main__':
    fp = open('dataset.txt', 'r')
    n = fp.read().split('\n')[0]
    fp.close()
    
    print(n)
    
    result = find_noncrossing_matchings(n, outermost=True)
    print(result)
    result = str(result % 1000000)
    print(result)
    
    fp2 = open('result.txt', 'w')
    fp2.write(result)
    fp2.close()