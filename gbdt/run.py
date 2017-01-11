#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)

import subprocess, sys, os, time

NR_THREAD = 40
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start = time.time()


cmd='mkdir gbdt/tmp -p'
shell(cmd)

cmd='gbdt/ffm2gbdt.py ffmData/Filter100/click_train.ffm gbdt/tmp/clickTrainDen.txt gbdt/tmp/clickTrainSpr.txt'
shell(cmd)

cmd='gbdt/ffm2gbdt.py ffmData/Filter100/click_test.ffm gbdt/tmp/clickTestDen.txt gbdt/tmp/clickTestSpr.txt'
shell(cmd)

cmd='gbdt/gbdt  -t 30 -s {nr_thread} gbdt/tmp/clickTestDen.txt gbdt/tmp/clickTestSpr.txt gbdt/tmp/clickTrainDen.txt gbdt/tmp/clickTrainSpr.txt gbdt/tmp/clickTestOut.txt gbdt/tmp/clickTrainOut.txt'.format(nr_thread=NR_THREAD)
shell(cmd)

cmd='gbdt/connect.py ffmData/Filter100/click_train.ffm gbdt/tmp/clickTrainOut.txt gbdt/tmp/connTrain.ffm'
shell(cmd)

cmd='gbdt/connect.py ffmData/Filter100/click_test.ffm gbdt/tmp/clickTestOut.txt gbdt/tmp/connTest.ffm'
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
