import os

"""Create a model based on train.arff"""
os.system('java weka.classifiers.meta.AdaBoostM1 -P 100 -S 1 -I 100 -W weka.classifiers.trees.DecisionStump -t train.arff -d j48.model')
