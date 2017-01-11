#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=40
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

inPath='ffmData/filter20user/'
#inPath='userHobby/data/hole/ffm/'
outPath='xgboost/data/hole/fm/'
cmd = 'mkdir {outPath} -p'.format(outPath=outPath)
shell(cmd)

cmd = 'xgboost/ffm2fm.py {inPath}split_train.ffm {outPath}split_train.fm'.format(inPath=inPath,outPath=outPath)
shell(cmd)

cmd = 'xgboost/ffm2fm.py {inPath}split_test.ffm {outPath}split_test.fm'.format(inPath=inPath,outPath=outPath)
shell(cmd)

cmd = 'xgboost/ffm2fm.py {inPath}click_test.ffm {outPath}click_test.fm'.format(inPath=inPath,outPath=outPath)
shell(cmd)


print('time used = {0:.0f}'.format(time.time()-start))
