#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import re
import subprocess


def checkTest(trainPath,testPath,oldTestPath):
    cmd='cp {0} {1}'.format(testPath,oldTestPath)
    subprocess.call(cmd,shell=True)
    maxInd=0
    for i,line in enumerate(open(trainPath)):
        if i<64556999-1000:
            continue
        cols=line.strip().split(' ')
        for col in cols[1:]:
            ind=int(col.split(':')[0])
            maxInd=ind if ind>maxInd else maxInd
    print(maxInd)
    outFile=open(testPath,'w')
    for line in open(oldTestPath):
        cols=line.strip().split(' ')
        outFile.write(cols[0])
        for col in cols[1:]:
            tmp=int(col.split(':')[0])
            if tmp<=maxInd:
                outFile.write(' '+col)
        outFile.write('\n')
    outFile.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('train', type=str)
    parser.add_argument('test', type=str)
    parser.add_argument('test_old', type=str)
    args = vars(parser.parse_args())
    checkTest(args['train'],args['test'],args['test_old'])
    #checkTest('xgboost/tmp/split_train.fm','xgboost/tmp/split_test.fm','xgboost/tmp/split_test_old.fm')

main()
