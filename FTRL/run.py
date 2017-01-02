#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=20
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

cmd = 'mkdir tmp'

cmd = 'ensamble/ensamble.py -s {nr_thread} -f 5 ../dataWihtTime/clicks_train.ffm  ../dataWihtTime/clicks_test.ffm data/clicks_train_out.txt data/clicks_test_out.txt '.format(nr_thread=NR_THREAD)
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
