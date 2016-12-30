header=['ad_id','doc_id','camp_id','adv_id','uuid', 'document_id', 'platform', 'geo_location', 'loc_country', 'loc_state', 'loc_dma','year','month','day','hour','weekday']
docHeader=['source_id','publisher_id','publish_year','publish_month','publish_day','publish_hour','publish_weekday','doc_categories','doc_topics','doc_entities']
adHeader=map(lambda x:'ad'+x,docHeader)
header+=['leak']+docHeader+adHeader+['overlap_srcid','overlap_pubid','overlap_time','overlap_cate','overlap_topic','overlap_entity']
print len(header)
f=open('sortedAbsW.txt')
N=43
table=[]
for i in range(N):
    table.append([0,0,0,10])
    
for ind,line in enumerate(f):
    tmp=line.strip().split('\t')
    field=int(tmp[0])
    val=float(tmp[2])
    if val<0.2:
        print (ind)
        break
    table[field][0]+=val
    table[field][1]+=1
    if val>table[field][2]:
        table[field][2]=val
    if val<table[field][3]:
        table[field][3]=val


with open("chgedW.txt",'w') as outFile:
    for ind,t in enumerate(table):
        if t[1]!=0:
            outFile.write("%s\t%s\t\t\t\t\t\t\t%s\t%s\t%s\t%s\n"%(ind,header[ind],t[0]/t[1],t[1],t[2],t[3]))
        else:
            outFile.write("%s\t%s\t\t\t\t\t\t\t%s\t%s\t%s\t%s\n"%(ind,header[ind],t[0],t[1],t[2],t[3]))
