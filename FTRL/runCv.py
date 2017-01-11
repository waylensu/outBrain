#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=20
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

cmd = 'mkdir FTRL/tmp -p'
shell(cmd)

cmd = 'mkdir FTRL/data -p'
shell(cmd)

#cmd = 'FTRL/ensamble/ensamble.py -s {nr_thread} -f 5 ffmData/Filter100/click_train.ffm  ffmData/Filter100/click_test.ffm FTRL/data/click_train_out.txt FTRL/data/click_test_out.txt '.format(nr_thread=NR_THREAD)
#shell(cmd)

cmd = 'FTRL/FTRLStarter.py ffmData/filter100/split_train.ffm ffmData/filter100/split_test.ffm FTRL/tmp/split_test_cv.out ffmData/filter100/click_test.ffm FTRL/tmp/click_test_cv.out'
shell(cmd)

cmd='util/map.py FTRL/tmp/split_test_cv.out  data/split_test.csv'
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
