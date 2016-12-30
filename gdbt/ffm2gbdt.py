#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)


#fileNames=['splitTrain','splitTest']

#dens=map(lambda x:'data/'+x+'Den.txt',fileNames)
#sprs=map(lambda x:'data/'+x+'Spr.txt',fileNames)
#ffms=map(lambda x:'../FFM2/data/'+x+'.txt',fileNames)

#maxFeat=13447004

def ffm2gbdt(ffm,den,spr):
#for ind,(ffm,den,spr) in enumerate(zip(ffms,dens,sprs)):
    denFile=open(den,'w')
    sprFile=open(spr,'w')
    for line in open(ffm):
        cols=line.strip().split(' ')
        denFile.write(cols[0])
        sprFile.write(cols[0])

        denFeats=[]
        sprFeats=[]
        for col in cols[1:]:
            field,index,value=col.split(':')
            if int(field)>=12:
                denFeats.append(int(float(value)*1000))
            else:
                sprFeats.append(int(index)+1)

        #for sparse data
        for feat in sprFeats:
            sprFile.write(' '+str(feat))
        sprFile.write('\n')
        #for dense data
        for feat in denFeats:
            denFile.write(' '+str(feat))
        denFile.write('\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ffm', type=str)
    parser.add_argument('den', type=str)
    parser.add_argument('spr', type=str)
    args = vars(parser.parse_args())
    ffm2gbdt(args['ffm'],args['den'],args['spr'])

main()
