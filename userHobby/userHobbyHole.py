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

def loadDoc():
    logging.info("Documents meta file..")
    doc_dict={}
    with open(data_path+"documents_meta.csv") as infile:
        docs=csv.reader(infile)
        next(docs)
        doc_header=['source_id','publisher_id','doc_categories','doc_topics','doc_entities']
        for ind,row in enumerate(docs):
            doc_id=row[0]
            tlist=row[1:3]
            tlist.extend([{},{},{}])
            doc_dict[doc_id]=tlist[:]
    del docs
    logging.info("Documents categories file..")
    with open(data_path+"documents_categories.csv") as infile:
        doc_cate=csv.reader(infile)
        next(doc_cate)
        for ind,row in enumerate(doc_cate):
            doc_id=row[0]
            doc_dict[doc_id][-3][row[1]]=row[2]
    del doc_cate
    logging.info("Documents topics file..")
    with open(data_path+"documents_topics.csv") as infile:
        doc_topic=csv.reader(infile)
        next(doc_topic)
        for ind,row in enumerate(doc_topic):
            doc_id=row[0]
            doc_dict[doc_id][-2][row[1]]=row[2]
    del doc_topic
    logging.info("Documents entities file..")
    with open(data_path+"documents_entities.csv") as infile:
        doc_entities=csv.reader(infile)
        next(doc_entities)
        for ind,row in enumerate(doc_entities):
            doc_id=row[0]
            doc_dict[doc_id][-1][row[1]]=row[2]
    del doc_entities
    return doc_dict

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

def getUserDict(doc_dict,uuid_set,event_dict,prcont_dict):
    uuid_dict={}
    with open(data_path+'page_views.csv') as pages:
        next(pages)
        for row in csv.reader(pages):
            uuid=row[0]
            if uuid not in uuid_set:
                continue
            doc_id=row[1]
            doc=doc_dict[doc_id]
            user=uuid_dict.get(uuid,[{},{},{},{},{},0])
            for i in range(2):
                user[i][doc[i]]=user[i].get(doc[i],0)+1
            user[5]+=1
            for i in range(2,5):
                for k,v in doc[i].items():
                    user[i][k]=user[i].get(k,0)+float(v)
            uuid_dict[uuid]=user
    with open(data_path+'clicks_train.csv') as train:
        next(train)
        for disp_id,ad_id,clicked in csv.reader(train):
            if clicked=='0':
                continue
            uuid=event_dict[disp_id]
            doc_id=prcont_dict[ad_id]
            doc=doc_dict[doc_id]
            user=uuid_dict.get(uuid,[{},{},{},{},{},0])
            for i in range(2):
                user[i][doc[i]]=user[i].get(doc[i],0)+1
            user[5]+=1
            for i in range(2,5):
                for k,v in doc[i].items():
                    user[i][k]=user[i].get(k,0)+float(v)
            uuid_dict[uuid]=user
    return uuid_dict

def createFeat(src,des,doc_dict,uuid_dict,event_dict,prcont_dict,hole=False):
    inFile=open(src)
    next(inFile)
    outFile=open(des,'w')
    for row in csv.reader(inFile):
        disp_id=row[0]
        ad_id=row[1]
        if disp_id not in event_dict:
            outFile.write('0,0,0,0,0\n')
            continue
        uuid=event_dict[disp_id]
        if (uuid not in uuid_dict) or (ad_id not in prcont_dict):
            outFile.write('0,0,0,0,0\n')
            continue
        ad_doc_id=prcont_dict[ad_id]
        user=uuid_dict[uuid]
        if ad_doc_id not in doc_dict:
            outFile.write('0,0,0,0,0\n')
            continue
        feats=[]
        ad_doc=doc_dict[ad_doc_id]
        for i in range(2):
            if ad_doc[i] in user[i]:
                if hole:
                    feats.append(user[i][ad_doc[i]]-1)
                else:
                    feats.append(user[i][ad_doc[i]])
            else:
                feats.append(0)
        for i in range(2,5):
            feat=0
            for k,v in ad_doc[i].items():
                if k in user[i]:
                    if hole and row[2]=='1':
                        feat+=math.sqrt((float(user[i][k])-float(ad_doc[i][k]))*float(ad_doc[i][k]))
                    else:
                        feat+=math.sqrt(float(user[i][k])*float(ad_doc[i][k]))
            feats.append(feat)
        outFile.write(','.join([str(x) for x in feats])+'\n')
    outFile.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('outPath', type=str)
    args = vars(parser.parse_args())
    outPath=args['outPath']
outPath='userHobby/data/hole2/'
train='data/click_train.csv'
test='data/click_test.csv'
trainFeat=outPath+'new_train_nonormal.csv'
testFeat=outPath+'new_test_nonormal.csv'

uuid_set,event_dict=loadEvent()
doc_dict=loadDoc()
prcont_dict=loadPrcont()
uuid_dict=getUserDict(doc_dict,uuid_set,event_dict,prcont_dict)
createFeat(train,trainFeat,doc_dict,uuid_dict,event_dict,prcont_dict,True)
createFeat(test,testFeat,doc_dict,uuid_dict,event_dict,prcont_dict,False)

main()
