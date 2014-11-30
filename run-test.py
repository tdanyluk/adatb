import os
import sys

"""Run it on test.arff and save the prediction to result.txt"""
if len(sys.argv) == 2 and sys.argv[1] == '-rf':
    os.system('java weka.classifiers.trees.RandomForest -l rf.model -T test.arff -p 0 > result.txt')
else:
    model = 'j48.model'
    if len(sys.argv) == 2:
        model = sys.argv[1]
    os.system('java weka.classifiers.trees.J48 -l %s -T test.arff -p 0 > result.txt'%model)
