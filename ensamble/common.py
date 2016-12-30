#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import subprocess

def stackSplit(train,folds):
    outs=[]
    for fold in range(folds):
        out=open('{0}.__test__.{1}'.format(train,fold),'w')
        outs.append(out)

    for ind,line in enumerate(open(train)):
        fold = int((ind/10000)%folds)
        outs[fold].write(line)

    for out in outs:
        out.close()

def cat(des,folds):
    workers=[]
    for fold in range(folds):
        cmd='cat '
        for foldOut in range(folds):
            if fold != foldOut:
                cmd+=' {0}.__test__.{1}'.format(des,foldOut)
        cmd+=' >> {0}.__train__.{1}'.format(des,fold)
        worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        workers.append(worker)
    for worker in workers:
        worker.communicate()

def parallel(train,predict,folds,nr_thread):
    workers=[]
    for fold in range(folds):
        trainPath='{0}.__train__.{1}'.format(train,fold)
        testPath='{0}.__test__.{1}'.format(train,fold)
        predictPath='{0}.__.{1}'.format(predict,fold)

        cmd="libffm/ffm-transform -i1 {test} -o1 {testOut} -i2 {predict} -o2 {predictOut} -p {test} --auto-stop -k 4 -s {nr_thread} {train} ".format(test=testPath, testOut=testPath+'.out' , predict=predictPath, predictOut=predictPath+'.out',train=trainPath ,nr_thread=nr_thread)
        print (cmd)
        worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        workers.append(worker)
    for worker in workers:
        worker.communicate()


def average(predict,score,folds):
    table=dict()
    for fold in range(folds):
        inFile=open('{0}.__.{1}.out'.format(predict,fold))
        for ind,line in enumerate(inFile):
            table[ind]=table.get(ind,0.)+float(line.strip())
        inFile.close()
    outFile=open(score,'w')
    for k,v in table.items():
        outFile.write(str(v/folds)+'\n')
    outFile.close()

def delete(train,predict,folds):
    for fold in folds:
        cmd='rm {train}.__train__.{fold} {train}.__test__.{fold} {predict}.__.{fold}'.format(train=train,predict=predict,fold=fold)
        subprocess.call(cmd, shell=True)
