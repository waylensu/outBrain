#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=10
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

threld=1000
cmd = 'mkdir ffmData/filter{threld} -p'.format(threld=threld)
shell(cmd)

cmd = 'mkdir tmp/filter{threld} -p'.format(threld=threld)
shell(cmd)

workers=[]

cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} util/filterFFM.py,-t,{threld} ffmDataWithTime/split_train.ffm ffmData/filter{threld}/split_train.ffm'.format(nr_thread=NR_THREAD,threld=threld)
worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
workers.append(worker)

cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} util/filterFFM.py,-t,{threld} ffmDataWithTime/split_test.ffm ffmData/filter{threld}/split_test.ffm'.format(nr_thread=NR_THREAD,threld=threld)
worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
workers.append(worker)

cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} util/filterFFM.py,-t,{threld} ffmDataWithTime/click_test.ffm ffmData/filter{threld}/click_test.ffm'.format(nr_thread=NR_THREAD,threld=threld)
worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
workers.append(worker)

for worker in workers:
    worker.communicate()
print("Done! workers")

NR_THREAD=40

cmd="libffm/ffm-transform -i1 ffmData/filter{threld}/split_test.ffm  -o1 tmp/filter{threld}/split_test.out -i2 ffmData/filter{threld}/click_test.ffm -o2 tmp/filter{threld}/click_test.out -p ffmData/filter{threld}/split_test.ffm  --auto-stop -k 8 -s {nr_thread} ffmData/filter{threld}/split_train.ffm".format(nr_thread=NR_THREAD,threld=threld)
shell(cmd)

cmd='util/map.py tmp/filter{threld}/split_test.out  data/split_test.csv'.format(threld=threld)
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
