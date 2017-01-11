#!/usr/bin/env python3
#coding=utf8
# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Example code for TensorFlow Wide & Deep Tutorial using TF.Learn API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tempfile
from six.moves import urllib

import pandas as pd
import tensorflow as tf
import math
import csv

flags = tf.app.flags
FLAGS = flags.FLAGS

flags.DEFINE_string("model_dir", "", "Base directory for output models.")
flags.DEFINE_string("model_type", "wide_n_deep",
                    "Valid model types: {'wide', 'deep', 'wide_n_deep'}.")
flags.DEFINE_integer("train_steps", 200, "Number of training steps.")
flags.DEFINE_string(
    "train_data",
    "",
    "Path to the training data.")
flags.DEFINE_string(
    "test_data",
    "",
    "Path to the test data.")

X_COLUMNS = ['ad_id','ad_doc_id','campaign_id','advertiser_id','uuid', 'document_id', 'platform', 'geo_location', 'loc_country', 'loc_state', 'loc_dma','leak','ad_src_id','ad_pub_id','ad_pub_time','disp_src_id','disp_pub_id','disp_pub_time','categories_overlap','topics_overlap','entities_overlap','user_src_id','user_pub_id','user_categories','user_topics','user_entities']

LABEL_COLUMN = ["label"]

COLUMNS=LABEL_COLUMN+X_COLUMNS
CATEGORICAL_COLUMNS = ['ad_id','ad_doc_id','campaign_id','advertiser_id','uuid', 'document_id', 'platform', 'geo_location', 'loc_country', 'loc_state', 'loc_dma','leak','ad_src_id','ad_pub_id','disp_src_id','disp_pub_id']
CONTINUOUS_COLUMNS = list(set(X_COLUMNS)-set(CATEGORICAL_COLUMNS))


def build_estimator(model_dir):
  bucketTable={}
  featDict={}
  with open("wideDeep/data/count.csv") as counter:
    for row in csv.reader(counter):
      bucketTable[row[0]]=int(row[1])
      featDict[row[0]]=tf.contrib.layers.sparse_column_with_integerized_feature(column_name=row[0], bucket_size=int(row[1]))
  featDict["leak"] = tf.contrib.layers.sparse_column_with_integerized_feature(column_name="leak",bucket_size=2)
  #featDict["leak"]=tf.contrib.layers.sparse_column_with_integerized_feature(column_name="leak", bucket_size=2)
  for col in CONTINUOUS_COLUMNS:
    featDict[col]=tf.contrib.layers.real_valued_column(col)
  embedCol = ['ad_id','ad_doc_id','campaign_id','advertiser_id','uuid', 'document_id', 'geo_location', 'loc_country', 'loc_state', 'loc_dma','ad_src_id','ad_pub_id','disp_src_id','disp_pub_id']
  wide_columns = list(featDict.values())
  deep_columns = [featDict[x] for x in CONTINUOUS_COLUMNS]+[tf.contrib.layers.embedding_column(featDict[x], dimension=int(math.log(bucketTable[x]))) for x in embedCol]+[tf.contrib.layers.one_hot_column(featDict["leak"]),tf.contrib.layers.one_hot_column(featDict["platform"])]
  if 0:
    pass
  else:
    m = tf.contrib.learn.DNNLinearCombinedClassifier(
        model_dir=model_dir,
        linear_feature_columns=wide_columns,
        dnn_feature_columns=deep_columns,
        dnn_hidden_units=[100, 50])
  return m


def input_fn(df):
  """Input builder function."""
  # Creates a dictionary mapping from each continuous feature column name (k) to
  # the values of that column stored in a constant Tensor.
  continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
  # Creates a dictionary mapping from each categorical feature column name (k)
  # to the values of that column stored in a tf.SparseTensor.
  categorical_cols = {
      k: tf.SparseTensor(
          indices=[[i, 0] for i in range(df[k].size)],
          values=df[k].values,
          shape=[df[k].size, 1])
      for k in CATEGORICAL_COLUMNS}
  # Merges the two dictionaries into one.
  feature_cols = dict(continuous_cols)
  feature_cols.update(categorical_cols)
  # Converts the label column into a constant Tensor.
  label = tf.constant(df["label"].values)
  # Returns the feature columns and the label.
  return feature_cols, label


def train_and_eval():
  """Train and evaluate the model."""
  train_file_name='wideDeep/dataUser/split_train.csv'
  test_file_name='wideDeep/dataUser/split_test.csv'
  predict_file_name='wideDeep/dataUser/click_test.csv'
  df_train = pd.read_csv(
  tf.gfile.Open(train_file_name),
  names=COLUMNS,
  skipinitialspace=True,
  engine="python")
  df_test = pd.read_csv(
  tf.gfile.Open(test_file_name),
  names=COLUMNS,
  skipinitialspace=True,
  engine="python")
  df_predict = pd.read_csv(
  tf.gfile.Open(predict_file_name),
  names=COLUMNS,
  skipinitialspace=True,
  engine="python")
  
  
  model_dir = tempfile.mkdtemp() 
  print("model directory = %s" % model_dir)
  
  m = build_estimator(model_dir)
  
  
  rows=2000000
  for i in range(int(len(df_train)/rows)):
    lhs=i*rows
    rhs=(i+1)*rows if (i+1)*rows<len(df_train) else len(df_train)
    m.fit(input_fn=lambda: input_fn(df_train[lhs:rhs]), steps=FLAGS.train_steps)
  
  #results=[]
  outFile=open('wideDeep/tmp/split_test.out','w')
  for i in range(int(len(df_test)/rows)):
    lhs=i*rows
    rhs=(i+1)*rows if (i+1)*rows<len(df_test) else len(df_test)
    for pro in m.predict_proba(input_fn=lambda: input_fn(df_test[lhs:rhs])):
        outFile.write('{0}\n'.format(pro))
  outFile.close()
  
  outFile=open('wideDeep/tmp/click_test.out','w')
  for i in range(int(len(df_test)/rows)):
      lhs=i*rows
      rhs=(i+1)*rows if (i+1)*rows<len(df_predict) else len(df_predict)
      for pro in m.predict_proba(input_fn=lambda: input_fn(df_predict[lhs:rhs])):
          outFile.write('{0}\n'.format(pro))
  outFile.close()
  
  #results = m.evaluate(input_fn=lambda: input_fn(df_test[:100000]), steps=1)
  #for key in sorted(results):
    #print("%s: %s" % (key, results[key]))


def main(_):
  train_and_eval()


if __name__ == "__main__":
  tf.app.run()
#  featDict["ad_pub_time"] = tf.contrib.layers.real_valued_column("ad_pub_time")
#  featDict["disp_pub_time"] = tf.contrib.layers.real_valued_column("disp_pub_time")
#  featDict["categories_overlap"] = tf.contrib.layers.real_valued_column("categories_overlap")
#  featDict["topics_overlap"] = tf.contrib.layers.real_valued_column("topics_overlap")
#  featDict["entities_overlap"] = tf.contrib.layers.real_valued_column("entities_overlap")
#  featDict["user_src_id"] = tf.contrib.layers.real_valued_column("user_src_id")
#  featDict["user_pub_id"] = tf.contrib.layers.real_valued_column("user_pub_id")
#  featDict["user_categories"] = tf.contrib.layers.real_valued_column("user_categories")
#  featDict["user_topics"] = tf.contrib.layers.real_valued_column("user_topics")
#  featDict["user_entities"] = tf.contrib.layers.real_valued_column("user_entities")
#  ad_id = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "ad_id", hash_bucket_size=bucketTable["ad_id"])
#  ad_doc_id = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "ad_doc_id", hash_bucket_size=bucketTable["ad_doc_id"])
#  campaign_id = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "campaign_id", hash_bucket_size=bucketTable["campaign_id"])
#  advertiser_id = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "advertiser_id", hash_bucket_size=bucketTable["advertiser_id"])
#  uuid = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "uuid", hash_bucket_size=bucketTable["uuid"])
#  document_id = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "document_id", hash_bucket_size=bucketTable["document_id"])
#  geo_location = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "geo_location", hash_bucket_size=bucketTable["geo_location"])
#  loc_country= tf.contrib.layers.sparse_column_with_hash_bucket(
#      "loc_country", hash_bucket_size=bucketTable["loc_country"])
#  loc_state = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "loc_state", hash_bucket_size=bucketTable["loc_state"])
#  loc_dma = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "loc_dma", hash_bucket_size=bucketTable["loc_dma"])
#  ad_src_id = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "ad_src_id", hash_bucket_size=bucketTable["ad_src_id"])
#  ad_pub_id = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "ad_pub_id", hash_bucket_size=bucketTable["ad_pub_id"])
#  disp_src_id = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "disp_src_id", hash_bucket_size=bucketTable["disp_src_id"])
#  disp_pub_id = tf.contrib.layers.sparse_column_with_hash_bucket(
#      "disp_pub_id", hash_bucket_size=bucketTable["disp_pub_id"])
