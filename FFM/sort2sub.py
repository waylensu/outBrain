#!/usr/bin/env python2
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import pandas as pd

def sub(score,subPath):
    proFile=open(score)
    pro=[float(line.strip()) for line in proFile]
    test=pd.read_csv('/home/wing/DataSet/outBrain/clicks_test.csv')
    test['likelihood']=pro
    test.sort_values(['display_id','likelihood'], inplace=True, ascending=False)
    subm = test.groupby('display_id').ad_id.apply(lambda x: " ".join(map(str,x))).reset_index()
    subm.to_csv(subPath, index=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('score', type=str)
    parser.add_argument('sub', type=str)
    args = vars(parser.parse_args())
    sub(args['score'],args['sub'])

main()
