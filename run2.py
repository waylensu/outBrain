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
shell(cmd)

#cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} FFM2/FFMStarter.py data/split_train.csv tmp/split_train.ffm'.format(nr_thread=NR_THREAD)
#shell(cmd)

#cmd = 'converters/parallelizer-1s1d.py -s {nr_thread} FFM2/FFMStarter.py data/split_test.csv tmp/split_test.ffm'.format(nr_thread=NR_THREAD)
#shell(cmd)
cmd = 'util/filter.py '
shell(cmd)

cmd="libffm/ffm-transform -i1 tmp/split_test_filter20.ffm  -o1 tmp/split_test_filter20.ffm.out -i2 tmp/click_test_filter20.ffm -o2 tmp/click_test_filter20.ffm.out -p tmp/split_test_filter20.ffm  --auto-stop -k 8 -s 40 tmp/split_train.ffm_filter20 "
shell(cmd)

#
#cmd = 'ensamble/ensamble.py -s {nr_thread} -f 5 tmp/clicks_train.ffm  tmp/clicks_test.ffm tmp/score.txt '.format(nr_thread=NR_THREAD)
#shell(cmd)
#
#cmd='FFM/sort2sub.py tmp/score.txt subm.csv'
#shell(cmd)

cmd='FFM/map.py tmp/split_test_filter20.ffm.out  data/split_test.csv'
shell(cmd)

print('time used = {0:.0f}'.format(time.time()-start))
