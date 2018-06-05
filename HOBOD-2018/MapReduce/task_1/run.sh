#!/usr/bin/env bash

OUT_DIR="hob_201820_task_1_17_March"
NUM_REDUCERS=8

hdfs dfs -rm -r -skipTrash ${OUT_DIR} > /dev/null

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="hob_201820_task_1_17_March_step1" \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -files mapper.py,reducer.py \
    -mapper mapper.py \
    -reducer reducer.py \
    -input /data/wiki/en_articles \
    -output ${OUT_DIR} > /dev/null

hdfs dfs -text ${OUT_DIR}/* | sort -n -k2 -r | head -10

hdfs dfs -rm -r -skipTrash ${OUT_DIR} > /dev/null