#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import subprocess

tmpTrainPath='tmp/train'
tmpPredictPath='tmp/train'

def stackSplit(train,folds):
    outs=[]
    for fold in range(folds):
        out=open('{0}.__test__.{1}'.format(tmpTrainPath,fold),'w')
        outs.append(out)

    for ind,line in enumerate(open(train)):
        fold = int((ind/10000)%folds)
        outs[fold].write(line)

    for out in outs:
        out.close()

def cat(folds):
    workers=[]
    for fold in range(folds):
        cmd='cat '
        for foldOut in range(folds):
            if fold != foldOut:
                cmd+=' {0}.__test__.{1}'.format(tmpTrainPath,foldOut)
        cmd+=' >> {0}.__train__.{1}'.format(tmpTrainPath,fold)
        worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        workers.append(worker)
    for worker in workers:
        worker.communicate()

def catTrainOut(trainOut):
    cmd='rm {0}'.format(trainOut)
    subprocess.call(cmd,shell=True)
    cmd='cat '
    for fold in range(folds):
        cmd+='{0}.__test__.{1} '.format(tmpTrainPath,fold)
    cmd+=' >> {0}'.format(trainOut)
    subprocess.call(cmd,shell=True)

def parallel(predict,folds,nr_thread):
    workers=[]
    for fold in range(folds):
        trainPath='{0}.__train__.{1}'.format(tmpTrainPath,fold)
        testPath='{0}.__test__.{1}'.format(tmpTrainPath,fold)
        predictPath='{0}.__predict__.{1}.out'.format(tmpPredictPath,fold)

        cmd="libffm/ffm-transform -i1 {test} -o1 {testOut} -i2 {predict} -o2 {predictOut} -p {test} --auto-stop -k 8 -s {nr_thread} {train} ".format(test=testPath, testOut=testPath+'.out' , predict=predict, predictOut=predictPath,train=trainPath ,nr_thread=nr_thread)
        print (cmd)
        worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        workers.append(worker)
    for worker in workers:
        worker.communicate()


def average(predictOut,folds):
    table=dict()
    for fold in range(folds):
        inFile=open('{0}.__predict__.{1}.out'.format(tmpPredictPath,fold))
        for ind,line in enumerate(inFile):
            table[ind]=table.get(ind,0.)+float(line.strip())
        inFile.close()
    outFile=open(predictOut,'w')
    for k,v in table.items():
        outFile.write(str(v/folds)+'\n')
    outFile.close()

def delete(train,predict,folds):
    for fold in range(folds):
        cmd='rm {train}.__train__.{fold} {train}.__test__.{fold} {predict}.__predict__.{fold} {test}.__test__.{fold}.out {predict}.__test__.{fold}.out '.format(train=tmpTrainPath,predict=tmpPredictPath,fold=fold)
        subprocess.call(cmd, shell=True)
