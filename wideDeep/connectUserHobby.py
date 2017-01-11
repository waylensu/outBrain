#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys

def connect(src,userHobby,des):
    inFile=open(src)
    feat=open(userHobby)
    outFile=open(des,'w')
    for row1,row2 in zip(inFile,feat):
        outFile.write(row1.strip()+','+row2)
    inFile.close()
    feat.close()
    outFile.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', type=str)
    parser.add_argument('userHobby', type=str)
    parser.add_argument('des', type=str)
    args = vars(parser.parse_args())
    connect(args['src'],args['userHobby'],args['des'])

main()
