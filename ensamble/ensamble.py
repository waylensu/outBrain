#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess
from common import *

def ensamble(train,predict,score,folds,nr_thread):
    stackSplit(train,folds)
    cat(train,folds)
    parallel(train,predict,folds,nr_thread)
    average(predict,score,folds)
    delete(train,predict,folds)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='nr_thread', default=12, type=int) 
    parser.add_argument('-f', dest='folds', default=5, type=int) 
    parser.add_argument('train', type=str)
    parser.add_argument('predict', type=str)
    parser.add_argument('score', type=str)
    args = vars(parser.parse_args())
    ensamble(args['train'],args['predict'],args['score'],args['folds'],args['nr_thread'])


main()
