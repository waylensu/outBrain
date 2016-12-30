import numpy as np
from datetime import datetime
import sys
print("Processed : ", datetime.now())

test = "data10per/splitTest.txt"
testPro = "data10per/splitTestOut.txt"

testFile=open(test)
testProFile=open(testPro)
#testFile.readline()
#testProFile.readline()
ys=[]
pros=[]
for line in testFile:
    ys.append(int(line.split(' ')[0]))

for line in testProFile:
    pros.append(float(line.strip()))

length=1000000
ones=np.zeros((length))
zeros=np.zeros((length))

for y,pro in zip(ys,pros):
    if y==1:
        ones[int(pro*length)]+=1
    else:
        zeros[int(pro*length)]+=1

bestScore=0
bestThrel=0
score=sum(ones)
for threl in range(length):
    score-=ones[threl]
    score+=zeros[threl]
    if score>bestScore:
        bestScore=score
        bestThrel=threl

print("Best Threl is %s,Best Score is %s."%(float(bestThrel)/length,float(bestScore)/len(ys)))
print("Processed : ", datetime.now())

