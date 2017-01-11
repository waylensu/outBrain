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

def predict(srcPath,desPath,model):
    testData = sc.textFile(srcPath).map(lambda l: l.split(',')).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2]))).map(lambda p: (p[0], p[1]))
    out = model.predictAll(testData)
    lines = out.map(toCSVLine)
    lines.saveAsTextFile(desPath)

def toCSVLine(data):
    return ','.join(str(d) for d in data)

#def main():
#    conf=SparkConf()
#    sc=SparkContext(conf=conf)
#        sc.addPyFile("sparseOperation.py")
#        spark = SparkSession \
#        .builder \
#        .appName("Python Spark SQL basic example") \
#        .getOrCreate()

hdfsPrePath='/user/wing/Project/outBrain/data/'
#data = sc.textFile(hdfsPrePath+"pageTrain.csv")
data = sc.textFile(hdfsPrePath+"pageSplitTrainRating.csv")
ratings = data.map(lambda l: l.split(',')).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))
rank = 10
numIterations = 10
model = ALS.train(ratings, rank, numIterations)
predict(hdfsPrePath+'trainRating.csv',hdfsPrePath+'split/click_train.als',model)
predict(hdfsPrePath+'testRating.csv',hdfsPrePath+'split/click_test.als',model)
#predict(hdfsPrePath+'trainRating.csv',hdfsPrePath+'click_train.als',model)
#predict(hdfsPrePath+'testRating.csv',hdfsPrePath+'click_test.als',model)

main()
