#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=40
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

inPath=''
outPath='userHobby/data/hole/'

cmd = 'mkdir {outPath} {outPath}ffm/ {outPath}out/ -p'.format(outPath=outPath)
shell(cmd)

cmd = 'userHobby/userHobbyHole.py {outPath}'.format(outPath=outPath)
shell(cmd)

cmd = 'userHobby/normal.py {outPath}'.format(outPath=outPath)
shell(cmd)

cmd = 'userHobby/connect.py ffmData/filter20/click_train.ffm {outPath}new_train.csv {outPath}ffm/click_train.ffm'.format(outPath=outPath)
shell(cmd)

cmd = 'userHobby/connect.py ffmData/filter20/click_test.ffm {outPath}new_test.csv {outPath}ffm/click_test.ffm'.format(outPath=outPath)
shell(cmd)

cmd = 'head -n {num} {outPath}ffm/click_train.ffm > {outPath}ffm/split_train.ffm'.format(num=64556990,outPath=outPath)
shell(cmd)

cmd = 'tail -n {num} {outPath}ffm/click_train.ffm > {outPath}ffm/split_test.ffm'.format(num=22584741,outPath=outPath)
shell(cmd)

cmd="libffm/ffm-transform -i1 {outPath}ffm/split_test.ffm  -o1 {outPath}out/split_test.out -i2 {outPath}ffm/click_test.ffm -o2 {outPath}out/click_test.out -p {outPath}ffm/split_test.ffm  --auto-stop -k 8 -s {nr_thread} {outPath}ffm/split_train.ffm".format(nr_thread=NR_THREAD,outPath=outPath)
shell(cmd)

cmd='util/sort2sub.py {outPath}out/click_test.out {outPath}out/sub.csv'
shell(cmd)

cmd='util/meanAveP.py {outPath}out/split_test.out  data/split_test.csv'
shell(cmd)
print('time used = {0:.0f}'.format(time.time()-start))
