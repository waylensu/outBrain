#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys,subprocess,time
import csv
from datetime import datetime
from csv import DictReader
from math import exp, log, sqrt
import sys
import logging
import math
import time

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
csv.field_size_limit(sys.maxsize)
data_path="/home/wing/DataSet/outBrain/"

def loadPrcont():
    logging.info("Content..")
    doc_map={}
    with open(data_path + "promoted_content.csv") as infile:
        prcont = csv.reader(infile)
        prcont_dict = {}
        for ind,row in enumerate(prcont):
            doc_map[row[1]]=len(doc_map)+1
            prcont_dict[row[0]] = row[1]
            if ind%100000 == 0:
                logging.info(ind)
        logging.info(len(prcont_dict))
    del prcont
    return doc_map,prcont_dict

def loadEvent():
    logging.info("Events..")
    uuid_map={}
    with open(data_path + "events.csv") as infile:
        events = csv.reader(infile)
        next(events)
        event_dict = {}
        for ind,row in enumerate(events):
            event_dict[row[0]] = row[1] 
            uuid_map[row[1]]=len(uuid_map)+1
            if ind%100000 == 0:
                logging.info("Events : "+ str(ind))
        logging.info(len(event_dict))
    del events
    return uuid_map,event_dict

def getPage(doc_map,uuid_map):
    pages=open(data_path+'page_views.csv')
    next(pages)
    for row in csv.reader(pages):
        uuid=row[0]
        doc=row[1]
        if (uuid not in uuid_map) or (doc not in doc_map):
            continue
        yield uuid_map[uuid],doc_map[doc],1
    pages.close()


def getTrain(doc_map,uuid_map,event_dict,prcont_dict):
    train=open('data/click_train.csv')
    next(train)
    for row in csv.reader(train):
        yield uuid_map[event_dict[row[0]]],doc_map[prcont_dict[row[1]]],row[2]
    train.close()
    

def getTest(doc_map,uuid_map,event_dict,prcont_dict):
    test=open('data/click_test.csv')
    next(test)
    for row in csv.reader(test):
        yield uuid_map[event_dict[row[0]]],doc_map[prcont_dict[row[1]]],0
    test.close()

def main():
    doc_map,prcont_dict=loadPrcont()
    uuid_map,event_dict=loadEvent()
    with open('als/data/pageRating.csv','w') as outFile:
        for line in getPage(doc_map,uuid_map):
            outFile.write('{0},{1},{2}\n'.format(line[0],line[1],line[2]))
    with open('als/data/trainRating.csv','w') as outFile:
        for line in getTrain(doc_map,uuid_map,event_dict,prcont_dict):
            outFile.write('{0},{1},{2}\n'.format(line[0],line[1],line[2]))
    with open('als/data/testRating.csv','w') as outFile:
        for line in getTest(doc_map,uuid_map,event_dict,prcont_dict):
            outFile.write('{0},{1},{2}\n'.format(line[0],line[1],line[2]))
            

main()
