#!/usr/bin/env python2
#coding=utf8
from __future__ import (division,absolute_import,print_function,unicode_literals)
import argparse, csv, sys
import pandas as pd
import numpy as np

dtypes = {'ad_id': np.float32, 'clicked': np.int8}

train = pd.read_csv("../../input/clicks_train.csv", usecols=['ad_id','clicked'], dtype=dtypes)

ad_likelihood = train.groupby('ad_id').clicked.agg(['count','sum','mean']).reset_index()
M = train.clicked.mean()
#del train

ad_likelihood['likelihood'] = (ad_likelihood['sum'] + 12*M) / (12 + ad_likelihood['count'])

test = pd.read_csv("../../input/clicks_test.csv")
test = test.merge(ad_likelihood, how='left')
test.likelihood.fillna(M, inplace=True)
test['likelihood'].to_csv('data/click_test_out.txt',index=False)


train = train.merge(ad_likelihood, how='left')
train.likelihood.fillna(M, inplace=True)
train['likelihood'].to_csv('data/click_train_out.txt',index=False)
#test.sort_values(['display_id','likelihood'], inplace=True, ascending=False)
#subm = test.groupby('display_id').ad_id.apply(lambda x: " ".join(map(str,x))).reset_index()
#subm.to_csv("subm.csv", index=False)
