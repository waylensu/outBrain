#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=10
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

cmd = 'mkdir ffmData/filter20 -p'
shell(cmd)


workers=[]

cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} filter/filterFFM.py dataWithTime/split_train.ffm ffmData/filter20/split_train.ffm'.format(nr_thread=NR_THREAD)
worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
workers.append(worker)

cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} filter/filterFFM.py dataWithTime/split_test.ffm ffmData/filter20/split_test.ffm'.format(nr_thread=NR_THREAD)
worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
workers.append(worker)

cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} filter/filterFFM.py dataWithTime/click_test.ffm ffmData/filter20/click_test.ffm'.format(nr_thread=NR_THREAD)
worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
workers.append(worker)

for worker in workers:
    worker.communicate()
print("Done! workers")

print('time used = {0:.0f}'.format(time.time()-start))
