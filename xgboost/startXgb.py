#!/usr/bin/env python3
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import re
import xgboost as xgb
from util.meanAveP import meanAveP

def startXgb(trainPath,testPath,predictPath,trainFeatPath,testFeatPath,predictFeatPath,testOutPath,predictOutPath):

    dtrain = xgb.DMatrix(trainPath)
    dtest = xgb.DMatrix(testPath)
    dpredict = xgb.DMatrix(predictPath)
    params={}
    params = {
                #'booster':'gbtree',
                'objective':'binary:logistic',
                'eta':0.5,
                #'max_depth':10,
                'subsample':0.8,
                'min_child_weight':5,
                'colsample_bytree':0.8,
                'scale_pos_weight':1,
                'eval_metric':'auc',
                #'gamma':0,            
                'lambda':300
    }

    watchlist=[(dtrain,'train'),(dtest,'val')]
    model = xgb.train(params, dtrain, num_boost_round=200,evals=watchlist)


    trainFeat=model.predict(dtrain,ntree_limit=30,pred_leaf=True)
    testFeat=model.predict(dtest,ntree_limit=30,pred_leaf=True)
    predictFeat=model.predict(dpredict,ntree_limit=30,pred_leaf=True)

    testOut=model.predict(dtest)
    predictOut=model.predict(dpredict)

    np.savetxt(trainFeatPath, trainFeat,fmt="%d", delimiter=",")
    np.savetxt(testFeatPath, testFeat ,fmt="%d", delimiter=",")
    np.savetxt(predictFeatPath, predictFeat ,fmt="%d", delimiter=",")
    np.savetxt(testOutPath, testOut ,fmt="%f", delimiter="")
    np.savetxt(predictOutPath, predictOut ,fmt="%f", delimiter="")

#    np.savetxt('xgboost/data/gbdtFeat/split_train.csv', trainFeat, delimiter=",")
#    np.savetxt('xgboost/data/gbdtFeat/split_test.csv', testFeat , delimiter=",")
#    np.savetxt('xgboost/data/gbdtFeat/click_test.csv', predictFeat , delimiter=",")
#    np.savetxt('xgboost/data/out/split_test.out', testOut , delimiter="")
#    np.savetxt('xgboost/data/out/click_test.out', predictOut , delimiter="")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('train', type=str)
    parser.add_argument('test', type=str)
    parser.add_argument('predict', type=str)
    parser.add_argument('trainFeat', type=str)
    parser.add_argument('testFeat', type=str)
    parser.add_argument('predictFeat', type=str)
    parser.add_argument('testOut', type=str)
    parser.add_argument('predictOut', type=str)
    args = vars(parser.parse_args())
    startXgb(args['train'],args['test'],args['testOut'],args['trainFeat'],args['testFeat'],args['predictFeat'],args['testOut'],args['predictOut'])

main()
