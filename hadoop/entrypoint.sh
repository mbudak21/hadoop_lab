#!/bin/bash

# wget "http://flask_app:5000/fetch?type=$SENSOR_TYPE" -O ./input.txt

# # move data to HDFS
# $HADOOP_HOME/bin/hdfs dfs -mkdir -p /tmp/input
# $HADOOP_HOME/bin/hdfs dfs -put -f ./input.txt /tmp/input/

# # Run Hadoop streaming
# $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
#     -input /tmp/input/input.txt \
#     -output /tmp/output \
#     -mapper ./mapper.py \
#     -reducer ./reducer.py \
#     -file mapper.py \
#     -file reducer.py

# # Keep the container alive
# tail -f /dev/null

# Setup Java
echo "export JAVA_HOME=$JAVA_HOME" >> etc/hadoop/hadoop-env.sh

# Start SSH daemon
/usr/sbin/sshd

# Start cron
# service cron start

if [ "$NODE_TYPE" == "namenode" ]; then
    echo "==> [namenode] Formatting HDFS..."
    hdfs namenode -format

    echo "==> [namenode] Starting DFS..."
    start-dfs.sh

    echo "==> [namenode] Starting periodic loop jobs..."
    $HADOOP_HOME/loop_jobs.sh &

    # Keep container alive
    tail -f /dev/null

elif [ "$NODE_TYPE" == "datanode" ]; then
    sed -i "s/localhost/$NAMENODE_HOST/" etc/hadoop/core-site.xml
    start-dfs.sh
    tail -f /dev/null

elif [ "$NODE_TYPE" == "resourcemanager" ]; then
    start-yarn.sh
    tail -f /dev/null

elif [ "$NODE_TYPE" == "nodemanager" ]; then
    sed -i "s/localhost/$RESOURCEMANAGER_HOST/" etc/hadoop/yarn-site.xml
    start-yarn.sh
    tail -f /dev/null

else
    echo "Unknown node type!"
fi
