#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys

D=2**25

def connect(srcFFM,gbdtFeat,desFFM,startField=25):
    srcFFMFile=open(srcFFM)
    gbdtFeatFile=open(gbdtFeat)
    desFFMFile=open(desFFM,'w')
    for src,gbdt in zip(srcFFMFile,gbdtFeatFile):
        line=src.strip()
        for ind,feat in enumerate(gbdt.strip().split()[1:]):
            featInd=abs(hash('gbdtFeat:'+str(ind)+':'+str(feat))%D)
            line+=' {field}:{index}:1'.format(field=startField+ind,index=featInd)
        line+='\n'
        desFFMFile.write(line)
    srcFFMFile.close()
    gbdtFeatFile.close()
    desFFMFile.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcFFM', type=str)
    parser.add_argument('gbdtFeat', type=str)
    parser.add_argument('desFFM', type=str)
    args = vars(parser.parse_args())
    connect(args['srcFFM'],args['gbdtFeat'],args['desFFM'])

main()
