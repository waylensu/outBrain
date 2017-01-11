#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=40
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

cmd = 'als/sortAls.py als/data/pageOnly/'
shell(cmd)

inPath='als/data/pageOnly/feat/'
outPath='als/data/pageOnly/ffm/'

cmd = 'mkdir {outPath} -p'.format(outPath=outPath)
shell(cmd)

cmd = 'head -n {num} {inPath}click_train.als > {inPath}split_train.als'.format(num=64556990,inPath=inPath)
shell(cmd)

cmd = 'tail -n {num} {inPath}click_train.als > {inPath}split_test.als'.format(num=22584741,inPath=inPath)
shell(cmd)

cmd = 'als/connect.py xgboost/data/ffm/split_train.ffm  {inPath}split_train.als {outPath}split_train.ffm'.format(inPath=inPath,outPath=outPath)
shell(cmd)

cmd = 'als/connect.py xgboost/data/ffm/split_test.ffm  {inPath}split_test.als {outPath}split_test.ffm'.format(inPath=inPath,outPath=outPath)
shell(cmd)

cmd = 'als/connect.py xgboost/data/ffm/click_test.ffm  {inPath}split_train.als {outPath}click_test.ffm'.format(inPath=inPath,outPath=outPath)
shell(cmd)


############################################
inPath='als/data/pageOnly/ffm/'
outPath='als/data/pageOnly/out/'

cmd='mkdir {outPath} -p'.format(outPath=outPath) 
shell(cmd)

cmd="libffm/ffm-transform -i1 {inPath}split_test.ffm  -o1 {outPath}split_test.out -i2 {inPath}click_test.ffm -o2 {outPath}click_test.out -p {inPath}split_test.ffm  --auto-stop -k 7 -s {nr_thread} {inPath}split_train.ffm".format(nr_thread=NR_THREAD,inPath=inPath,outPath=outPath)
shell(cmd)

cmd='util/sort2sub.py {outPath}click_test.out {outPath}sub.csv'.format(outPath=outPath)
shell(cmd)

cmd='util/meanAveP.py {outPath}split_test.out  data/split_test.csv'.format(outPath=outPath)
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
