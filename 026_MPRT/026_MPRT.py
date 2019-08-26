import urllib

file = open('dataset.txt', 'r')
data = file.read()
file.close()

proteins = data.split()

for p in proteins:
    url = "http://www.uniprot.org/uniprot/"+p+".fasta"
    print url
    response = urllib.urlopen(url)
    text = response.read()
    print ''
    print p
    print url
    print text