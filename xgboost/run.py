#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=40
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

#inPath='ffmData/filter20hole/'
inPath='userHobby/data/hole/ffm/'
outPath='xgboost/data/hole/ffm/'
cmd = 'mkdir {outPath} -p'.format(outPath=outPath)
shell(cmd)

cmd = 'xgboost/connect.py {inPath}split_train.ffm xgboost/data/gbdtFeat/split_train.csv {outPath}split_train.ffm'.format(inPath=inPath,outPath=outPath)
shell(cmd)

cmd = 'xgboost/connect.py {inPath}split_test.ffm xgboost/data/gbdtFeat/split_test.csv {outPath}split_test.ffm'.format(inPath=inPath,outPath=outPath)
shell(cmd)

cmd = 'xgboost/connect.py {inPath}click_test.ffm xgboost/data/gbdtFeat/click_test.csv {outPath}click_test.ffm'.format(inPath=inPath,outPath=outPath)
shell(cmd)

inPath='xgboost/data/hole/ffm/'
outPath='xgboost/data/hole/out'
cmd = 'mkdir {outPath} -p'.format(outPath=outPath)
shell(cmd)

cmd="libffm/ffm-transform -i1 {inPath}split_test.ffm  -o1 {outPath}split_test.out -i2 {inPath}click_test.ffm -o2 {outPath}click_test.out -p {inPath}split_test.ffm  --auto-stop -k 8 -s {nr_thread} {inPath}split_train.ffm".format(nr_thread=NR_THREAD,inPath=inPath,outPath=outPath)
shell(cmd)

cmd='util/sort2sub.py {outPath}click_test.out {outPath}sub.csv'.format(outPath=outPath)
shell(cmd)

cmd='util/meanAveP.py {outPath}split_test.out  data/split_test.csv'.format(outPath=outPath)
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
