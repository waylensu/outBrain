#!/usr/bin/env python2
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import pandas as pd

def map(proPath,testPath):
    #proFile=open('../FFM2/dataDoc/splitTestOut.txt')
    proFile=open(proPath)
    pro=[float(line.strip()) for line in proFile]
    #test=pd.read_csv('/home/wing/DataSet/outBrain/split_testSample.csv')
    test=pd.read_csv(testPath)
    test['likelihood']=pro
    test.sort_values(['display_id','likelihood'], inplace=True, ascending=False)
    score = test.groupby('display_id').clicked.apply(lambda x: 1./float(sum([(ind+1)*val for ind,val in enumerate(x)])) ).reset_index()
    print (score['clicked'].mean())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pro', type=str)
    parser.add_argument('test', type=str)
    args = vars(parser.parse_args())
    map(args['pro'],args['test'])

main()
