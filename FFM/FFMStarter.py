# -*- coding: utf-8 -*-
"""
Thanks to tinrtgu for the wonderful base script
Use pypy for faster computations.!
"""
import csv
from datetime import datetime
from csv import DictReader
from math import exp, log, sqrt
import sys
import logging
import math

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
csv.field_size_limit(sys.maxsize)

# TL; DR, the main training process starts on line: 250,
# you may want to start reading the code from there


##############################################################################
# parameters #################################################################
##############################################################################

# A, paths
#data_path = "../input/"
data_path = "../../input/"
#des_path = "dataOverlapOHnoDoc2/"
des_path = "dataOverlapOH2/"

splitTrain = data_path+'split_train.csv'               # path to training file
splitTest = data_path+'split_test.csv'                 # path to testing file
clickTest = data_path+'clicks_test.csv'                 # path to testing file
splitTrainPath=des_path+'splitTrain.txt'
splitTestPath=des_path+'splitTest.txt'
clickTestPath=des_path+'clickTest.txt'

srcFile=[splitTrain,splitTest,clickTest]
desFile=[splitTrainPath,splitTestPath,clickTestPath]

withTimeStamp=True
#withDoc=False
withDoc=True
withDocOverlap=True

#D=2**15
#def getInd(featName):
    #return abs(hash(featName)%D)
#featTable={}
#def getInd(featName,val):
#    if not featName in featTable:
#        featTable[featName]={}
#    if not val in featTable[featName]:
#        featTable[featName][val]=len(featTable[featName])
#    return featTable[featName][val]
class OneHotEncoder(object):
    
    def __init__(self):
        self.featTable={}
        self.add=True
    
    def encode(self,field,feat,level=1):
        string=str(field)+'_'+str(feat)
        if not string in self.featTable:
            if self.add:
                self.featTable[string]=len(self.featTable)
            else:
                return field,-1,level
        featInd=self.featTable[string]
        return field,featInd,level

def data(path,oneHot):
    ''' GENERATOR: Apply hash-trick to the original csv row
                   and for simplicity, we one-hot-encode everything

        INPUT:
            path: path to training or testing file
            D: the max index that we can hash to

        YIELDS:
            ID: id of the instance, mainly useless
            x: a list of hashed and one-hot-encoded 'indices'
               we only need the index since all values are either 0 or 1
            y: y = 1 if we have a click, else we have y = 0
    '''

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

        #for key in row[1:]:
            #x.append(oneHot.encode(field,row[key]))
            #field+=1
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
            for ind in range(2):
                if ad_row[ind]==disp_row[ind] and ad_row[ind]!='':
                    x.append(oneHot.encode(field,0,1))
                else:
                    x.append(oneHot.encode(field,0,0))
                field+=1
            diffs=[]
            if ad_row[2]!='' and disp_row[2]!='':
                for ind in range(2,6):
                    diffs.append(int(ad_row[ind])-int(disp_row[ind]))
                timeDiff=(diffs[0]+(diffs[1]+(diffs[2]+float(diffs[3])/24)/30)/12)/5
                if timeDiff>1:
                    timeDiff=1
                elif timeDiff<-1:
                    timeDiff=-1
                if timeDiff>0:
                    x.append(oneHot.encode(field,0,timeDiff))
                else:
                    x.append(oneHot.encode(field,1,-timeDiff))
            field+=1
            for ind in range(7,10):
                level=0
                for col in ad_row[ind]:
                    if col in disp_row[ind]:
                        level+=math.sqrt(float(ad_row[ind][col])*float(disp_row[ind][col]))
                if level>1:
                    level=1
                x.append(oneHot.encode(field,0,level))
                field+=1
            fieldCount+=6
            field=fieldCount

        yield field, t, disp_id, ad_id, x, y
        #yield ad_id, x, y


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
    event_header = ['uuid', 'document_id', 'platform', 'geo_location', 'loc_country', 'loc_state', 'loc_dma']
    if withTimeStamp:
        event_header+=['year','month','day','hour','weekday']
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
        if withTimeStamp:
            timeStamp=datetime.fromtimestamp((int(row[3])+1465876799998)/1000)
            tlist.append(str(timeStamp.year))
            tlist.append(str(timeStamp.month))
            tlist.append(str(timeStamp.day))
            tlist.append(str(timeStamp.hour))
            tlist.append(str(timeStamp.isoweekday()))
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
        docs.next()
        doc_header=['source_id','publisher_id','publish_year','publish_month','publish_day','publish_hour','publish_weekday','doc_categories','doc_topics','doc_entities']
        for ind,row in enumerate(docs):
            doc_id=int(row[0])
            tlist=row[1:3]
            if row[3] == '':
                tlist.extend(['','','','',''])
            else:
                timeStamp=datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S");
                tlist.append(str(timeStamp.year))
                tlist.append(str(timeStamp.month))
                tlist.append(str(timeStamp.day))
                tlist.append(str(timeStamp.hour))
                tlist.append(str(timeStamp.isoweekday()))
            tlist.extend([{},{},{}])
            doc_dict[doc_id]=tlist[:]
    del docs

    logging.info("Documents categories file..")
    with open(data_path+"documents_categories.csv") as infile:
        doc_cate=csv.reader(infile)
        doc_cate.next()
        for ind,row in enumerate(doc_cate):
            doc_id=int(row[0])
            doc_dict[doc_id][-3][row[1]]=row[2]
    del doc_cate

    logging.info("Documents topics file..")
    with open(data_path+"documents_topics.csv") as infile:
        doc_topic=csv.reader(infile)
        doc_topic.next()
        for ind,row in enumerate(doc_topic):
            doc_id=int(row[0])
            doc_dict[doc_id][-2][row[1]]=row[2]
    del doc_topic

    logging.info("Documents entities file..")
    with open(data_path+"documents_entities.csv") as infile:
        doc_entities=csv.reader(infile)
        doc_entities.next()
        for ind,row in enumerate(doc_entities):
            doc_id=int(row[0])
            doc_dict[doc_id][-1][row[1]]=row[2]
    del doc_entities

logging.info("Leakage file..")
leak_uuid_dict= {}
#"""
with open(data_path+"leak_uuid_doc.csv") as infile:
	doc = csv.reader(infile)
	doc.next()
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
for src,des in zip(srcFile,desFile):
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
    oneHot.add=False
