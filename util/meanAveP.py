#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import pandas as pd

def meanAveP(pro,test):
    test['likelihood']=pro
    newTest=test.sort_values(['display_id','likelihood'], ascending=False)
    score = newTest.groupby('display_id').clicked.apply(lambda x: 1./float(sum([(ind+1)*val for ind,val in enumerate(x)])) ).reset_index()
    print (score['clicked'].mean())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pro', type=str)
    parser.add_argument('test', type=str)
    args = vars(parser.parse_args())

    proFile=open(args['pro'])
    pro=[float(line.strip()) for line in proFile]
    test=pd.read_csv(args['test'])
    meanAveP(pro,test)
    proFile.close()

if __name__=='__main__':
    main()
