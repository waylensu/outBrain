#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)

import subprocess, sys, os, time

NR_THREAD = 40
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start = time.time()
'''
cmd='./ffm2gbdt.py ../FFM2/data/splitTrain.txt data/splitTrainDen.txt data/splitTrainSpr.txt'
shell(cmd)

cmd='./ffm2gbdt.py ../FFM2/data/splitTest.txt data/splitTestDen.txt data/splitTestSpr.txt'
shell(cmd)

cmd='./gbdt  -t 30 -s {nr_thread} data/splitTestDen.txt data/splitTestSpr.txt data/splitTrainDen.txt data/splitTrainSpr.txt data/splitTestOut.txt data/splitTrainOut.txt'.format(nr_thread=NR_THREAD)
shell(cmd)
'''

cmd='./connect.py ../FFM2/data/splitTrain.txt data/splitTrainOut.txt data/connTrain.ffm'
shell(cmd)

cmd='./connect.py ../FFM2/data/splitTest.txt data/splitTestOut.txt data/connTest.ffm'
shell(cmd)

cmd='../libffm/ffm-transform -k 8 -s {nr_thread} -p data/connTest.ffm --auto-stop -i1 data/connTest.ffm -o1 data/connTestOut data/connTrain.ffm > ffm.log'.format(nr_thread=NR_THREAD)
shell(cmd)

cmd='../FFM/map.py data/connTestOut /home/wing/DataSet/outBrain/split_testSample.csv'
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
