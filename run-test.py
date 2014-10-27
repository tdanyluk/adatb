import os

"""Run it on test.arff and save the prediction to result.txt"""
os.system('java weka.classifiers.trees.J48 -l j48.model -T test.arff -p 0 > result.txt')