FROM ubuntu:latest

ENV HADOOP_VERSION=3.3.6
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop-$HADOOP_VERSION
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin

RUN apt update && \
    apt install openjdk-11-jdk wget ssh pdsh -y

RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xvzf hadoop-$HADOOP_VERSION.tar.gz -C /opt/ && \
    rm hadoop-$HADOOP_VERSION.tar.gz


WORKDIR $HADOOP_HOME

RUN echo "export JAVA_HOME=$JAVA_HOME" >> ./etc/hadoop/hadoop-env.sh

RUN ./bin/hdfs dfs -mkdir -p /tmp/input

RUN wget -O data-00.txt http://metaphorpsum.com/paragraphs/20/40 && \
    mv data-00.txt /tmp/input/

COPY mapper.py reducer.py ./


RUN ./bin/hadoop jar ./share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /tmp/input/ -output /tmp/output \
    -mapper mapper.py -reducer reducer.py \
    -file mapper.py -file reducer.py


CMD ["bash"]