#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time


def normal(srcs,dess):
    maxs=[0]*5
    for src in srcs:
        inFile=open(src)
        for row in csv.reader(inFile):
            for i in range(5):
                feat=float(row[i])
                if feat>maxs[i]:
                    maxs[i]=feat
        inFile.close()
    print(maxs)
    for src,des in zip(srcs,dess):
        outFile=open(des,'w')
        inFile=open(src)
        feats=['0']*5
        for row in csv.reader(inFile):
            for i in range(5):
                feats[i]=str(float(row[i])/maxs[i])
            outFile.write(','.join(feats)+'\n')
        inFile.close()
        outFile.close()

def main():
    normal(['wideDeep/data/click_train.csv','wideDeep/data/click_test.csv'],['wideDeep/data/click_train_normal.csv','wideDeep/data/click_test_normal.csv'])

main()
