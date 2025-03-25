#!/bin/bash

wget "http://flask_app:5000/fetch?type=$SENSOR_TYPE" -O ./input.txt

# move data to HDFS
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /tmp/input
$HADOOP_HOME/bin/hdfs dfs -put -f ./input.txt /tmp/input/

# Run Hadoop streaming
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /tmp/input/input.txt \
    -output /tmp/output \
    -mapper ./mapper.py \
    -reducer ./reducer.py \
    -file mapper.py \
    -file reducer.py

# Keep the container alive
tail -f /dev/null
