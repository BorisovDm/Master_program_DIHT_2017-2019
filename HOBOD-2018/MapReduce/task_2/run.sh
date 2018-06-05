#!/usr/bin/env bash

OUT_DIR="hw_02_task_5_hob201820_16_March"
NUM_REDUCERS=8

hdfs dfs -rm -r -skipTrash ${OUT_DIR}.tmp > /dev/null
hdfs dfs -rm -r -skipTrash ${OUT_DIR} > /dev/null

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="hob_201820_hw_2_task_5_step1" \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -files mapper1.py,reducer1.py \
    -mapper mapper1.py \
    -reducer reducer1.py \
    -input /data/user_events \
    -output ${OUT_DIR}.tmp > /dev/null

yarn jar /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.name="hob_201820_hw_2_task_5_step2" \
    -D mapreduce.job.reduces=$NUM_REDUCERS \
    -files mapper2.py,reducer2.py \
    -mapper mapper2.py \
    -reducer reducer2.py \
    -input ${OUT_DIR}.tmp \
    -output ${OUT_DIR} > /dev/null

#hdfs dfs -cat ${OUT_DIR}/part-00000
hdfs dfs -text ${OUT_DIR}/* | sort -n -k2 -r | head -10

hdfs dfs -rm -r -skipTrash ${OUT_DIR}.tmp > /dev/null
hdfs dfs -rm -r -skipTrash ${OUT_DIR} > /dev/null