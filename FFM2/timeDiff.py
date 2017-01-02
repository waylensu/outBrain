#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
from datetime import datetime
import time
import logging
import math

logging.info("Documents meta file..")                                          
doc_dict={}

timeArray=time.strptime("2016-06-14 00:00:00", "%Y-%m-%d %H:%M:%S")
timeStamp=int(time.mktime(timeArray))
maxTime=timeStamp
minTime=timeStamp

sigma=math.log(2)/(2*365*24*60*60)
#math.exp(-sigma*x)

data_path="/home/wing/DataSet/outBrain/"
with open(data_path+"documents_meta.csv") as infile:                           
    docs=csv.reader(infile)                                                    
    next(docs)
    for ind,row in enumerate(docs):                                            
        doc_id=int(row[0])                                                     
        if not row[3] == '':                                                       
            timeArray=time.strptime(row[3], "%Y-%m-%d %H:%M:%S")
            if timeArray.tm_year>=2017 or timeArray.tm_year<1940:
                print(ind,row[3])
            else:
                timeStamp=int(time.mktime(timeArray))
                if timeStamp>maxTime:
                    maxTime=timeStamp
                elif timeStamp<minTime:
                    minTime=timeStamp


print (maxTime,minTime)
print (time.localtime(maxTime),time.localtime(minTime))
