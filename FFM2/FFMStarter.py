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

# TL; DR, the main training process starts on line: 250,
# you may want to start reading the code from there


##############################################################################
# parameters #################################################################
##############################################################################
withDoc=True
withDocOverlap=True
D=2**25
data_path="/home/wing/DataSet/outBrain/"

#class OneHotEncoder(object):
#    def encode(self,field,feat,level=1):
#        featInd=str(abs(hash('field:{0}:feat:{1}'.format(field,feat))%D))
#        return field,featInd,level

class OneHotEncoder(object):
    def __init__(self):
        self.featTable={}
        self.featCount={}
        self.add=True
    
    def encode(self,field,feat,level=1):
        string=str(field)+'_'+str(feat)
        if not string in self.featTable:
            if self.add:
                self.featTable[string]=len(self.featTable)
                self.featCount[string]=1
            else:
                return field,-1,level
        else:
            self.featCount[string]+=1
        featInd=self.featTable[string]
        return field,featInd,level

def data(path,oneHot):
    for t, row in enumerate(DictReader(open(path))):
        # process id
        disp_id = int(row['display_id'])
        ad_id = int(row['ad_id'])

        # process clicks
        y = 0.
        if 'clicked' in row:
            if row['clicked'] == '1':
                y = 1.
            del row['clicked']

        x = []
        fieldCount=0
        field=fieldCount

        x.append(oneHot.encode(field,row['ad_id']))
        fieldCount+=1
        field=fieldCount

        row = prcont_dict.get(ad_id, [])		
        for ind, val in enumerate(row):
            if ind==0:
                ad_doc_id = int(val)
            x.append(oneHot.encode(field,val))
            field+=1
        fieldCount+=len(row)
        field=fieldCount

        row = event_dict.get(disp_id, [])
        for ind, val in enumerate(row):
            if ind==0:
                uuid_val = val
            if ind==1:
                disp_doc_id = int(val)
            x.append(oneHot.encode(field,val))
            field+=1
        fieldCount+=len(event_header)
        field=fieldCount

        if (ad_doc_id in leak_uuid_dict) and (uuid_val in leak_uuid_dict[ad_doc_id]):
            x.append(oneHot.encode(field,0,1))
        else:
            x.append(oneHot.encode(field,0,0))
        fieldCount+=1
        field=fieldCount

        if withDoc:
            ## build x
            for docType in ['ad','disp']:
                if docType=='ad':
                    row = doc_dict.get(ad_doc_id, [])
                else:
                    row = doc_dict.get(disp_doc_id, [])
                for ind ,val in enumerate(row):
                    if ind>=len(doc_header)-3:
                        for k,v in val.items():
                            x.append(oneHot.encode(field,k,v))
                    else:
                        x.append(oneHot.encode(field,val))
                    field+=1
            fieldCount+=2*len(doc_header)
            field=fieldCount
        
        if withDocOverlap:
            ad_row = doc_dict.get(ad_doc_id, [])
            disp_row = doc_dict.get(disp_doc_id, [])
            for ind in range(2,5):
                level=0
                for col in ad_row[ind]:
                    if col in disp_row[ind]:
                        level+=math.sqrt(float(ad_row[ind][col])*float(disp_row[ind][col]))
                if level>1:
                    level=1
                x.append(oneHot.encode(field,0,level))
                field+=1
            fieldCount+=3
            field=fieldCount

        yield field, t, disp_id, ad_id, x, y


##############################################################################
# start training #############################################################
##############################################################################

start = datetime.now()

# initialize ourselves a learner
#learner = ftrl_proximal(alpha, beta, L1, L2, D, interaction)

logging.info("Content..")
with open(data_path + "promoted_content.csv") as infile:
	prcont = csv.reader(infile)
	prcont_header = next(prcont)[1:]
	prcont_dict = {}
	for ind,row in enumerate(prcont):
		prcont_dict[int(row[0])] = row[1:]
		if ind%100000 == 0:
			logging.info(ind)
	logging.info(len(prcont_dict))
del prcont

logging.info("Events..")
with open(data_path + "events.csv") as infile:
    events = csv.reader(infile)
    next(events)
    #event_header = ['uuid', 'document_id', 'platform', 'geo_location', 'loc_country', 'loc_state', 'loc_dma','timestamp']
    event_header = ['uuid', 'document_id', 'platform', 'geo_location', 'loc_country', 'loc_state', 'loc_dma']
    event_dict = {}
    for ind,row in enumerate(events):
        tlist = row[1:3] + row[4:6]
        loc = row[5].split('>')
        if len(loc) == 3:
            tlist.extend(loc[:])
        elif len(loc) == 2:
            tlist.extend( loc[:]+[' '])
        elif len(loc) == 1:
            tlist.extend( loc[:]+[' ',' '])
        else:
            tlist.append([' ',' ',' '])	
        #tlist.append(int(row[3])/1000)
            #timeStamp=datetime.fromtimestamp((int(row[3])+1465876799998)/1000)
        event_dict[int(row[0])] = tlist[:] 
        if ind%100000 == 0:
            logging.info("Events : "+ str(ind))
    logging.info(len(event_dict))
del events

if withDoc or withDocOverlap:
    logging.info("Documents meta file..")
    doc_dict={}
    with open(data_path+"documents_meta.csv") as infile:
        docs=csv.reader(infile)
        next(docs)
        #doc_header=['source_id','publisher_id','pub_time','doc_categories','doc_topics','doc_entities']
        doc_header=['source_id','publisher_id','doc_categories','doc_topics','doc_entities']
        for ind,row in enumerate(docs):
            doc_id=int(row[0])
            tlist=row[1:3]
            tlist.extend([{},{},{}])
            doc_dict[doc_id]=tlist[:]
    del docs

    logging.info("Documents categories file..")
    with open(data_path+"documents_categories.csv") as infile:
        doc_cate=csv.reader(infile)
        next(doc_cate)
        for ind,row in enumerate(doc_cate):
            doc_id=int(row[0])
            doc_dict[doc_id][-3][row[1]]=row[2]
    del doc_cate

    logging.info("Documents topics file..")
    with open(data_path+"documents_topics.csv") as infile:
        doc_topic=csv.reader(infile)
        next(doc_topic)
        for ind,row in enumerate(doc_topic):
            doc_id=int(row[0])
            doc_dict[doc_id][-2][row[1]]=row[2]
    del doc_topic

    logging.info("Documents entities file..")
    with open(data_path+"documents_entities.csv") as infile:
        doc_entities=csv.reader(infile)
        next(doc_entities)
        for ind,row in enumerate(doc_entities):
            doc_id=int(row[0])
            doc_dict[doc_id][-1][row[1]]=row[2]
    del doc_entities

logging.info("Leakage file..")
leak_uuid_dict= {}
#"""
with open(data_path+"leak.csv") as infile:
	doc = csv.reader(infile)
	next(doc)
	leak_uuid_dict = {}
	for ind, row in enumerate(doc):
		doc_id = int(row[0])
		leak_uuid_dict[doc_id] = set(row[1].split(' '))
		if ind%100000==0:
		    logging.info("Leakage file : "+ str(ind))
	logging.info(len(leak_uuid_dict))
del doc
#"""	
oneHot=OneHotEncoder()

def data2ffm(src,des):
#for src,des in zip(srcFile,desFile):
    with open(des,'w') as outfile:
        for field,t,disp_id,ad_id,x,y in data(src,oneHot):
            line=str(int(y))+' '
            length=field
            for feat in x:
                if feat[1]!=-1:
                    line+='%s:%s:%s '%(str(feat[0]),str(feat[1]),str(feat[2]))
            line+='\n'
            if t%1000000 == 0:
                logging.info("Processed : "+str(t))
            outfile.write(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', type=str)
    parser.add_argument('des', type=str)
    args = vars(parser.parse_args())
    data2ffm(args['src'],args['des'])

#main()
countPath='count.csv'
src=['../data/split_train.csv','../data/split_test.csv','../../input/clicks_test.csv']
des=['../data/split_train.ffm','../data/split_test.ffm','../data/clicks_test.ffm']
for s,d in zip(src,des):
    data2ffm(s,d)

exit()
with open(countPath,'w') as infile:
    for k,v in oneHot.featCount.items():
        infile.write('{0},{1}\n'.format(k,v))
