import sys
import json
import re
import StringIO

categs = [
    'recreation',
    'culture_politics',
    'science_technology',
    'arts_entertainment',
    'business',
    'computer_internet',
    'health',
    'gaming',
    'sports',
    'religion',
    'law_crime'
    ]

yearPattern = re.compile(r'(?:^|[^0-9])((?:19|20|21)[0-9]{2})(?=$|[^0-9])')
inYearPattern = re.compile(r'(?:^|[^a-zA-Z])in ((?:19|20|21)[0-9]{2})(?=$|[^0-9])', re.IGNORECASE)
forYearPattern = re.compile(r'(?:^|[^a-zA-Z])for ((?:19|20|21)[0-9]{2})(?=$|[^0-9])', re.IGNORECASE)
ofYearPattern = re.compile(r'(?:^|[^a-zA-Z])of ((?:19|20|21)[0-9]{2})(?=$|[^0-9])', re.IGNORECASE)

words = [
    'if',
    '1',
    'about',
    'then',
    'easy',
    'hi',
    'his',
    'recipe',
    'food',
    'homemade',
    'living',
    'cookie',
    'family',
    'kitchen',
    'baking',
    'fashion',
    'today',
    'betting'
    ]

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def parseLine(line):
    a = line.strip('\n').split('\t')
    for i in range(0,len(a)):
        a[i] = a[i].strip('\'"').replace('""','"')
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
        if i == 0:
            outf.write('@ATTRIBUTE url_year NUMERIC\n')
        elif i == 2:
            outf.write('@ATTRIBUTE title_year NUMERIC\n')
            outf.write('@ATTRIBUTE title_year_in NUMERIC\n')
            outf.write('@ATTRIBUTE title_year_for NUMERIC\n')
            outf.write('@ATTRIBUTE title_year_of NUMERIC\n')
            for w in words:
                outf.write('@ATTRIBUTE json_word_%s NUMERIC\n'%w)
            pass
        elif i == 3:
            for c in categs:
                outf.write('@ATTRIBUTE categ_%s NUMERIC\n'%c)
        elif i == 4:
            pass
        else:
            outf.write('@ATTRIBUTE %s %s\n'%(attributeNames[i], attributeTypes[i]))
    outf.write('@ATTRIBUTE label {0,1}\n')
    outf.write('@DATA\n')
    a = firstDataRow
    while not( len(a) == 0 or (len(a) == 1 and a[0] == '')):
        assert len(a) == nCols
        for i in range(0,nCols):
            if i == 0:
                year = yearPattern.findall(a[0])+['?']
                outf.write("%s, "%year[0])
            elif i == 2:
                io = StringIO.StringIO(a[i])
                data = json.load(io)
                io.close()
                title = ''
                if 'title' in data:
                    title = data['title']
                if title == None:
                    title = ''
                year = yearPattern.findall(title)+['?']
                inYear = inYearPattern.findall(title)+['?']
                forYear = forYearPattern.findall(title)+['?']
                ofYear = ofYearPattern.findall(title)+['?']
                outf.write("%s, %s, %s, %s, " % (year[0],inYear[0], forYear[0], ofYear[0]))
                _json = a[i].lower()
                for w in words:
                    w = w.lower()
                    outf.write('%d, '%_json.count(w))
            elif i == 3:
                for c in categs:
                    if c == a[i]:
                        outf.write('%s, '%a[4])
                    elif a[i] in categs:
                        outf.write('0, ')
                    else:
                        outf.write('?, ')
            elif i == 4:
                pass
            else:
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
