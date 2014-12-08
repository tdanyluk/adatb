import sys
import re

def parseLine(line):
    a = line.strip('\n').split('\t')
    for i in range(0,len(a)):
        a[i] = a[i].strip('\'"').replace('""','"')
    return a

def main():
    if len(sys.argv) != 2:
        print "usage: python words.py train.tsv"
        sys.exit(1)
    inFileName = sys.argv[1]   
    inf = open( inFileName , "r" )
    s = inf.readline()
    attributeNames = parseLine(s);
    nCols = len(attributeNames)
    s = inf.readline()
    a = parseLine(s)
    wordMap = [{},{}]
    nonalnum = re.compile(r'\W+')
    num = [0,0]
    while not( len(a) == 0 or (len(a) == 1 and a[0] == '')):
        assert len(a) == nCols
        _json = a[2].lower()
        label = int(a[26])
        num[label] = num[label]+1
        words = list(set(nonalnum.split(_json)))
        for w in words:
            if w in wordMap[label]:
                wordMap[label][w] += 1
            else:
                wordMap[label][w] = 1
        s = inf.readline()
        a = parseLine(s)
    inf.close()
    ratioAndOccuranceMap = {}
    for i in [0,1]:
        for w in wordMap[i]:
            if not(w in ratioAndOccuranceMap):
                ratioAndOccuranceMap[w] = [0, 0]
            ratioAndOccuranceMap[w][1] += wordMap[i][w]
    for w in ratioAndOccuranceMap:
        for i in [0,1]:
            if not (w in wordMap[i]):
                wordMap[i][w] = 1
        a0 = wordMap[0][w]/float(num[0])
        a1 = wordMap[1][w]/float(num[1])
        ratioAndOccuranceMap[w][0] = max(a0,a1) / min(a0,a1)
        if max(a0,a1) == a0:
            ratioAndOccuranceMap[w][0] = -ratioAndOccuranceMap[w][0] 
    outFileName = ''
    if inFileName.endswith('.tsv'):
        outFileName = inFileName[0:-4] + '.words'
    else:
        outFileName = inFileName + '.words'
    outf = open( outFileName , "w+" )
    for item in sorted(ratioAndOccuranceMap.items(), key=lambda x: abs(x[1][1]),  reverse=True):
        if abs(item[1][0]) > 1.5 and item[1][1] > 1000:
            outf.write('%s: %s, %s\n'%(item[0], item[1][0], item[1][1]))
    outf.close()
    
if __name__ == "__main__":
    main()
