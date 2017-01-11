#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import logging
import re

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
csv.field_size_limit(sys.maxsize)
data_path="/home/wing/DataSet/outBrain/"

def loadLeak():
    logging.info("Leakage file..")
    leak_uuid_dict= {}
    with open(data_path+"leak.csv") as infile:
        doc = csv.reader(infile)
        next(doc)
        leak_uuid_dict = {}
        for ind, row in enumerate(doc):
            doc_id = row[0]
            leak_uuid_dict[doc_id] = set(row[1].split(' '))
            if ind%100000==0:
                logging.info("Leakage file : "+ str(ind))
            #logging.info(len(leak_uuid_dict))
        del doc
    return leak_uuid_dict

def loadPrcont():
    logging.info("Content..")
    with open(data_path + "promoted_content.csv") as infile:
        prcont = csv.reader(infile)
        prcont_dict = {}
        for ind,row in enumerate(prcont):
            prcont_dict[row[0]] = row[1]
            if ind%100000 == 0:
                logging.info(ind)
        logging.info(len(prcont_dict))
    del prcont
    return prcont_dict

def loadEvent():
    logging.info("Events..")
    uuid_set=set()
    with open(data_path + "events.csv") as infile:
        events = csv.reader(infile)
        next(events)
        event_dict = {}
        for ind,row in enumerate(events):
            event_dict[row[0]] = row[1] 
            uuid_set.add(row[1])
            if ind%100000 == 0:
                logging.info("Events : "+ str(ind))
        logging.info(len(event_dict))
    del events
    return uuid_set,event_dict


def chgLeak(csvFile,src,des,event_dict,prcont_dict,leak_uuid_dict):
    csvFile=open(csvFile)
    inFile=open(src)
    outFile=open(des,'w')
    header=next(csvFile)
    for csvRow,inRow in zip(csv.reader(csvFile),inFile):
        disp_id=csvRow[0]
        ad_id=csvRow[1]
        uuid=event_dict[disp_id]
        ad_doc_id=prcont_dict[ad_id]
        if (ad_doc_id in leak_uuid_dict) and (uuid in leak_uuid_dict[ad_doc_id]):
            flag=1
        else:
            flag=0
        outRow=re.sub(' 11:10:\d',' 11:10:{flag}'.format(flag=flag),inRow)
        outFile.write(outRow)
    csvFile.close()
    inFile.close()
    outFile.close()

def main():
    uuid_set,event_dict=loadEvent()
    prcont_dict=loadPrcont()
    leak_uuid_dict=loadLeak()
    chgLeak('data/click_train.csv','ffmData/filter100/click_train.ffm','ffmData/filter100Leak/click_train.ffm',event_dict,prcont_dict,leak_uuid_dict)
    chgLeak('data/click_test.csv','ffmData/filter100/click_test.ffm','ffmData/filter100Leak/click_test.ffm',event_dict,prcont_dict,leak_uuid_dict)

main()
