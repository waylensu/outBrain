#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import re


def filter(src,des,threld):
    countPath='FFM2/count.csv'
    mapTable={}
    for line in open(countPath):
        k,v=line.strip().split(',')
        if int(v)>threld:
            mapTable[int(k)]=len(mapTable)
    print(len(mapTable))

    inFile=open(src)
    outFile=open(des,'w')
    for line in inFile:
        cols=line.strip().split(' ')
        outLine=cols[0]
        for col in cols[1:]:
            if not re.search(':(\d*):',col):
                print(col)
                print(line)
                exit()
            feat=int(re.search(':(\d*):',col).group(1))
            if feat in mapTable:
                reCol=re.sub(':\d*:',':{0}:'.format(mapTable[feat]),col)
                outLine+=' '+reCol
        outLine+='\n'
        outFile.write(outLine)
    inFile.close()
    outFile.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='threld', default=20, type=int)
    parser.add_argument('src', type=str)
    parser.add_argument('des', type=str)
    args = vars(parser.parse_args())
    filter(args['src'],args['des'],args['threld'])

main()
