#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time

NR_THREAD=20
def shell(cmd):
    subprocess.call(cmd,shell=True)
    print("Done! {0}.".format(cmd))

start=time.time()

#cmd = 'mkdir tmp'

#cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} FFM2/FFMStarter.py data/split_train.csv tmp/split_train.ffm'.format(nr_thread=NR_THREAD)
#shell(cmd)

#cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} FFM2/FFMStarter.py data/split_test.csv tmp/split_test.ffm'.format(nr_thread=NR_THREAD)
#shell(cmd)

cmd="libffm/ffm-transform -i1 dataWithTime/split_test.ffm  -o1 dataWithTime/split_test.ffm.out -i2 dataWithTime/click_test.ffm -o2 dataWithTime/click_test.ffm.out -p dataWithTime/split_test.ffm  --auto-stop -k 8 -s 40 dataWithTime/split_train.ffm "
shell(cmd)

#
#cmd = 'ensamble/ensamble.py -s {nr_thread} -f 5 tmp/clicks_train.ffm  tmp/clicks_test.ffm tmp/score.txt '.format(nr_thread=NR_THREAD)
#shell(cmd)
#
#cmd='FFM/sort2sub.py tmp/score.txt subm.csv'
#shell(cmd)

cmd='FFM/map.py dataWithTime/split_test.ffm.out data/split_test.csv'
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
