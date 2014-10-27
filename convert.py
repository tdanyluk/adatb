import sys

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def parseLine(line):
    a = line.strip('\n').split('\t')
    for i in range(0,len(a)):
        a[i] = a[i].strip('"').replace("'",'"').replace(',',';')
    return a

def main():
    if len(sys.argv) != 3:
        print "usage: python convert.py input.tsv test={0,1}"
        sys.exit(1)
    inFileName = sys.argv[1]
    test = sys.argv[2] == '1'
    outFileName = ''
    if inFileName.endswith('.tsv'):
        outFileName = inFileName[0:-4] + '.arff'
    else:
        outFileName = inFileName + '.arff'
    inf = open( inFileName , "r" )
    outf = open( outFileName , "w+" )
    s = inf.readline()
    attributeNames = parseLine(s);
    nCols = len(attributeNames)
    print "Number of attributes: %d"%nCols
    attributeTypes = []
    s = inf.readline()
    firstDataRow = parseLine(s);
    assert len(firstDataRow) == nCols
    for i in range(0,nCols):
        if isfloat(firstDataRow[i]):
            attributeTypes.append('NUMERIC')
        else:
            attributeTypes.append('STRING')
    outf.write('@RELATION relation1\n')
    N = nCols-1
    if test:
        N = nCols
    for i in range(0,N):
        if not i in [0,2,3]:
            outf.write('@ATTRIBUTE %s %s\n'%(attributeNames[i], attributeTypes[i]))
    outf.write('@ATTRIBUTE label {0,1}\n')
    outf.write('@DATA\n')
    a = firstDataRow
    while not( len(a) == 0 or (len(a) == 1 and a[0] == '')):
        assert len(a) == nCols
        for i in range(0,nCols):
            if attributeTypes[i] == 'STRING':
                a[i] = "'" + a[i] + "'"
            if not i in [0,2,3]:
                outf.write(a[i])
                if i != nCols-1:
                    outf.write(', ')
        if test:
            outf.write(', ?')
        outf.write('\n')
        s = inf.readline()
        a = parseLine(s)
    inf.close()
    outf.close()
    
if __name__ == "__main__":
    main()
