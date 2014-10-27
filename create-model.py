import os

"""Create a model based on train.arff"""
os.system('java weka.classifiers.trees.J48 -t train.arff -d j48.model')
