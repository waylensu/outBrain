
#ffms=['splitTrain.txt','splitTest.txt','clickTest.txt']
ffms=['splitTrain.txt','splitTest.txt']
fms=ffms

ffms=map(lambda x:'../FFM2/data/'+x,ffms)
fms=map(lambda x:'data/'+x,fms)

def ffm2sort(x):
    tmp=x.split(':')[1:]
    return int(tmp[0]),float(tmp[1])
#maxFeat=13447004
maxFeat=0

for ind,(ffm,fm) in enumerate(zip(ffms,fms)):
    outFile=open(fm,'w')
    for line in open(ffm):
        cols=line.strip().split(' ')
        outFile.write(cols[0])
        feats=sorted(map(ffm2sort,cols[1:]))
        for feat in feats:
            if ind==0:
                if feat[0]>maxFeat:
                    maxFeat=feat[0]
                outFile.write(' '+':'.join(map(str,feat)))
            else:
                if feat[0]<=maxFeat:
                    outFile.write(' '+':'.join(map(str,feat)))
        outFile.write('\n')

print (maxFeat)
