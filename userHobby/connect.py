#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys

def connect(srcFFM,featPath,desFFM,startField=27,startInd=1200000):
    srcFFMFile=open(srcFFM)
    featFile=open(featPath)
    desFFMFile=open(desFFM,'w')
    for src,feats in zip(srcFFMFile,featFile):
        line=src.strip()
        for ind,feat in enumerate(feats.strip().split(',')):
            line+=' {field}:{index}:{value}'.format(field=startField+ind,index=startInd+ind,value=feat)
        line+='\n'
        desFFMFile.write(line)
    srcFFMFile.close()
    featFile.close()
    desFFMFile.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcFFM', type=str)
    parser.add_argument('featPath', type=str)
    parser.add_argument('desFFM', type=str)
    args = vars(parser.parse_args())
    connect(args['srcFFM'],args['featPath'],args['desFFM'])

main()
