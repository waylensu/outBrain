#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=40
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

cmd = 'mkdir tmp/filter100 -p'
shell(cmd)


#workers=[]
#
#cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} util/filterFFM.py ffmDataWithTime/split_train.ffm ffmData/Filter100/split_train.ffm'.format(nr_thread=NR_THREAD)
#worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#workers.append(worker)
#
#cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} util/filterFFM.py ffmDataWithTime/split_test.ffm ffmData/Filter100/split_test.ffm'.format(nr_thread=NR_THREAD)
#worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#workers.append(worker)
#
#cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} util/filterFFM.py ffmDataWithTime/click_test.ffm ffmData/Filter100/click_test.ffm'.format(nr_thread=NR_THREAD)
#worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#workers.append(worker)
#
#for worker in workers:
#    worker.communicate()
#print("Done! workers")

cmd="libffm/ffm-transform -i1 ffmData/filter100/split_test.ffm  -o1 tmp/filter100/split_test.out -i2 ffmData/filter100/click_test.ffm -o2 tmp/filter100/click_test.out -p ffmData/filter100/split_test.ffm  --auto-stop -k 8 -s {nr_thread} ffmData/filter100/split_train.ffm".format(nr_thread=NR_THREAD)
shell(cmd)

cmd='util/map.py tmp/filter100/split_test.out  data/split_test.csv'
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
