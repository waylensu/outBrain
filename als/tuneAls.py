#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
from numpy import array                                               
from pyspark import SparkConf,SparkContext                            
from pyspark.sql import SparkSession
from pyspark.mllib.linalg import Vectors                              
from pyspark.ml.feature import StringIndexer                          
from pyspark.mllib.linalg import Vectors, SparseVector, DenseVector   
from pyspark.sql import Row
import numpy as np
import csv
import StringIO                                                       
import argparse, csv, sys,subprocess,time
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

# Load and parse the data

# Evaluate the model on training data

def eval(ratings,model):
    testdata = ratings.map(lambda p: (p[0], p[1]))
    predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
    ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
    MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
    return MSE

hdfsPrePath='/user/wing/Project/outBrain/data/'
trainRating=sc.textFile(hdfsPrePath+'pageSplitTrainRating.csv').map(lambda l: l.split(',')).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2]))).cache()
testRating=sc.textFile(hdfsPrePath+'splitTestRating.csv').map(lambda l: l.split(',')).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2]))).cache()
#rank = 6
#numIterations = 9
#model = ALS.train(trainRating, rank, numIterations)
#print(eval(trainRating,model),eval(testRating,model))

for numIterations in [10,12]:
    for rank in [20]:
        model = ALS.train(trainRating, rank, numIterations)
        print(numIterations,rank,eval(trainRating,model),eval(testRating,model))
