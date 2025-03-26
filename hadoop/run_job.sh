#!/bin/bash

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/opt/hadoop-3.3.6
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin
cd $HADOOP_HOME

# Parameters (use ENV vars or defaults)
SENSOR_TYPE=${SENSOR_TYPE:-TemperatureSensor}

echo "Running as user: $(whoami)"
echo "Current directory: $(pwd)"
echo "PATH is: $PATH"


echo "Fetching data of type $SENSOR_TYPE"
wget flask_app:5000/fetch?type=$SENSOR_TYPE -O /tmp/input.txt
INPUT_LINES=$(wc -l < /tmp/input.txt)

echo "Home: $HADOOP_HOME"
# Remove output dir in HDFS 
# Wait until HDFS is ready
until hdfs dfs -test -e /; do
  echo "HDFS not yet ready. Waiting..."
  sleep 5
done

# For extra caution, force leaving safe mode
hdfs dfsadmin -safemode leave

# Now remove the old output dir
hdfs dfs -rm -r -f /tmp/output || echo "Remove failed: $?"

# Copy data to HDFS
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /tmp/input
$HADOOP_HOME/bin/hdfs dfs -put -f /tmp/input.txt /tmp/input/

$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-input /tmp/input \
-output /tmp/output \
-mapper $HADOOP_HOME/mapper.py \
-reducer $HADOOP_HOME/reducer.py \
-file $HADOOP_HOME/mapper.py \
-file $HADOOP_HOME/reducer.py

# Copy output to local
rm -rf /tmp/local_output
$HADOOP_HOME/bin/hdfs dfs -get /tmp/output /tmp/local_output

{
    echo "Input length: $INPUT_LINES lines"
    echo "File created on: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
    cat /tmp/local_output/part-00000
} > $HADOOP_HOME/output.txt

#mv /tmp/local_output/part-00000 ./output.txt
