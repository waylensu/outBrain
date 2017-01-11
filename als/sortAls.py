#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time
import csv
from datetime import datetime
from csv import DictReader
from math import exp, log, sqrt
import sys
import logging
import math
import time

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
csv.field_size_limit(sys.maxsize)

def getMean(als):
    levelSum=0.
    levelCount=0
    with open(als) as inFile:
        for line in inFile:
            uuid,doc,level=line.strip().split(',')
            levelSum+=float(level)
            levelCount+=1
    return levelSum/levelCount


def sortAls(src,als,des,ave):
    table={}
    with open(als) as inFile:
        for line in inFile:
            uuid,doc,level=line.strip().split(',')
            table[uuid+'_'+doc]=level
    with open(src) as inFile:
        with open(des,'w') as outFile:
            for line in inFile:
                uuid,doc,level=line.strip().split(',')
                if not uuid+'_'+doc in table:
                    outFile.write(str(ave)+'\n')
                else:
                    outFile.write(str(table[uuid+'_'+doc])+'\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('prePath', type=str)
    args = vars(parser.parse_args())
    #prePath='als/data/'
    prePath=args['prePath'] 
    ave=getMean(prePath+'als/click_train.als')
    print(ave)
    sortAls('als/data/trainRating.csv',prePath+'als/click_train.als',prePath+'feat/click_train.als',ave)
    sortAls('als/data/testRating.csv',prePath+'als/click_test.als',prePath+'feat/click_test.als',ave)

main()
