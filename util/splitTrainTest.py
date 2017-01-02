#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys

srcPath='/home/wing/DataSet/outBrain/'
clickTrainPath=srcPath+'clicks_train.csv'
eventsPath=srcPath+'events.csv'
splitTrainPath='../data/split_train.csv'
splitTestPath='../data/split_test.csv'

train=open(splitTrainPath,'w')
test=open(splitTestPath,'w')

with open(eventsPath) as infile:
    events = csv.reader(infile)
    next(events)
    event_dict={}
    for ind,row in enumerate(events):
        event_dict[row[0]]=int(row[3])


#table={}
with open(clickTrainPath) as infile:
    header=infile.readline()
    train.write(header)
    test.write(header)
    for line in infile:
        disp_id=line.split(',')[0]
        if not disp_id in event_dict:
            print(disp_id)
            continue
        #day=int(event_dict[disp_id]/24*60*60*1000)
        #table[day]=table.get(day,0)+1
        if event_dict[disp_id]>14*24*60*60*1000:
            print('Over 14 days',disp_id)
        if event_dict[disp_id]>12*24*60*60*1000:
            test.write(line)
        else:
            if int(disp_id)%5==0:
                test.write(line)
            else:
                train.write(line)


#print(table)


train.close()
test.close()

    
    
