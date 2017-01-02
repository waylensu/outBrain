#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import re


countPath='FFM2/count.csv'
threld=20
countTable={}
for line in open(countPath):
    k,v=line.strip().split(',')
    countTable[int(k)]=int(v)

src=['dataWithTime/split_train.ffm','dataWithTime/split_test.ffm','dataWithTime/click_test.ffm']
des=['tmp/split_train_filter20.ffm','tmp/split_test_filter20.ffm','tmp/click_test_filter20.ffm']

for s,d in zip(src,des):
    inFile=open(s)
    outFile=open(d,'w')
    for line in inFile:
        cols=line.split(' ')
        outLine=cols[0]
        for col in cols[1:]:
            feat=int(re.search(':(\d*):',col).group(1))
            if countTable[feat]>threld:
                outLine+=' '+col
        outLine+='\n'
        outFile.write(outLine)
    inFile.close()
    outFile.close()

