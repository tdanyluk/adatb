import sys

def main():
    res = open( "result.txt" , "r" )
    test = open( "test.arff" , "r" )
    out = open( "submit.csv" , "w+" )
    s = ''
    while s != '=== Predictions on test set ===\n':
        s = res.readline()
    s = ''
    while s != '@DATA\n':
        s = test.readline()

    res.readline()
    res.readline()
    r = res.readline()
    s = test.readline()
    out.write('urlid,label\n')
    while r != '\n':
        a = r.split(':')
        pred = 0
        if a[1][0] == '1':
            pred = 1
        a = s.split(',')
        _id = int(a[0])
        out.write("%s,%s\n"%(_id,pred))
        r = res.readline()
        s = test.readline()
    res.close()
    test.close()
    out.close()
if __name__ == "__main__":
    main()
