#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess
from common import *

def ensamble(train,predict,trainOut,predictOut,folds,nr_thread):
    stackSplit(train,folds)
    cat(folds)
    parallel(predict,folds,nr_thread)
    catTrainOut(train,trainOut)
    average(predictOut,folds)
    #delete(train,predict,folds)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='nr_thread', default=12, type=int) 
    parser.add_argument('-f', dest='folds', default=5, type=int) 
    parser.add_argument('train', type=str)
    parser.add_argument('predict', type=str)
    parser.add_argument('trainOut', type=str)
    parser.add_argument('predictOut', type=str)
    args = vars(parser.parse_args())
    ensamble(args['train'],args['predict'],args['trainOut'],args['predictOout'],args['folds'],args['nr_thread'])

main()
