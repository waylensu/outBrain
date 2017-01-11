#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=20
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

inPath='ffmData/filter20userGbdt/'
outPath='FTRL/data/'

cmd = 'mkdir FTRL/tmp -p'
shell(cmd)

cmd = 'mkdir FTRL/data -p'
shell(cmd)


cmd = 'FTRL/FTRLStarter.py {inPath}split_train.ffm {inPath}split_test.ffm {outPath}split_test.out {inPath}click_test.ffm {outPath}click_test.out'.format(inPath=inPath,outPath=outPath)
shell(cmd)

'''
cmd='util/meanAveP.py {outPath}split_test.out  data/split_test.csv'.format(outPath=outPath)
shell(cmd)
'''

print('time used = {0:.0f}'.format(time.time()-start))

