#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import numpy as np

from sklearn.linear_model import LogisticRegression


def getX(paths):
    x=[]
    for path in paths:
        with open(path) as inFile:
            row=[]
            for line in inFile:
                row.append(float(line.strip()))
        x.append(row)
    return np.array(x).T

def getY(path):
    with open(path) as inFile:
        next(inFile)
        y=[]
        for line in inFile:
            y.append(int(line.strip().split(',')[2]))
    return np.array(y)

def lr(trainPaths,trainLabels,testPaths,trainOut,testOut):
    model=LogisticRegression()
    xTrain=getX(trainPaths)
    model.fit(xTrain,getY(trainLabels))
    trainScores=model.decision_function(xTrain)
    testScores=model.decision_function(getX(testPaths))
    with open(trainOut,'w') as outFile:
        for trainScore in trainScores:
            outFile.write(str(trainScore)+'\n')
    with open(testOut,'w') as outFile:
        for testScore in testScores:
            outFile.write(str(testScore)+'\n')

def main():
    paths=['tmp/filter20userGbdtk8/','tmp/filter20userGbdt/','FTRL/data/','xgboost/data/out/','pandaOnly/data/']
    trainPaths=map(lambda x:x+'split_test.out',paths)
    testPaths=map(lambda x:x+'click_test.out',paths)
    trainLabels='data/split_test.csv'
    trainOut='lr/tmp/split_test.out'
    testOut='lr/tmp/click_test.out'
    lr(trainPaths,trainLabels,testPaths,trainOut,testOut)

main()
