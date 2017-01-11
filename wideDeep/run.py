#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=40
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

'''
cmd="wideDeep/wideDeepStart.py"
shell(cmd)

cmd="wideDeep/normal.py"
shell(cmd)
'''

cmd="wideDeep/connectUserHobby.py wideDeep/data/click_train.csv userHobby/data/new_train.csv wideDeep/dataUser/click_train.csv"
shell(cmd)

cmd="wideDeep/connectUserHobby.py wideDeep/data/click_test.csv userHobby/data/new_test.csv wideDeep/dataUser/click_test.csv"
shell(cmd)

cmd = 'head -n {num} wideDeep/dataUser/click_train.csv > wideDeep/dataUser/split_train.csv'.format(num=64556990)
shell(cmd)

cmd = 'tail -n {num} wideDeep/dataUser/click_train.csv > wideDeep/dataUser/split_test.csv'.format(num=22584741)
shell(cmd)

cmd = 'wideDeep/wide_n_deep_tutorial.py'

print('time used = {0:.0f}'.format(time.time()-start))
