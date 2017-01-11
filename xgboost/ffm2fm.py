#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import re

def ffm2fm(ffm,fm):
    outFile=open(fm,'w')
    for line in open(ffm):
        line,i=re.subn(' \d+:',' ',line)
        outFile.write(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ffm', type=str)
    parser.add_argument('fm', type=str)
    args = vars(parser.parse_args())
    ffm2fm(args['ffm'],args['fm'])

main()
