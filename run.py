#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=20
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()
'''
cmd = 'mkdir tmp'
shell(cmd)

cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} FFM2/FFMStarter.py ~/DataSet/outBrain/clicks_train.csv tmp/clicks_train.ffm'.format(nr_thread=NR_THREAD)
shell(cmd)

cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} FFM2/FFMStarter.py ~/DataSet/outBrain/clicks_test.csv tmp/clicks_test.ffm'.format(nr_thread=NR_THREAD)
shell(cmd)
'''

cmd = 'ensamble/ensamble.py -s {nr_thread} -f 5 tmp/clicks_train.ffm  tmp/clicks_test.ffm tmp/score.txt '.format(nr_thread=NR_THREAD)
shell(cmd)

cmd='FFM/sort2sub.py tmp/score.txt subm.csv'
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
