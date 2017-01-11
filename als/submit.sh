#!/bin/sh
~/Project/spark-2.0.1/bin/spark-submit --master yarn --executor-cores 4 --num-executors 4 --executor-memory 30g sparkAls.py

./bin/hadoop fs -getmerge   /user/wing/Project/outBrain/data/split/click_train.als /home/wing/Project/outBrain/python/als/data/split/als/click_train.als
./bin/hadoop fs -getmerge   /user/wing/Project/outBrain/data/split/click_test.als /home/wing/Project/outBrain/python/als/data/split/als/click_test.als
