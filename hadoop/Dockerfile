FROM ubuntu:latest

# Parameters
ENV SENSOR_TYPE=TemperatureSensor
ENV REF_LATITUDE=12.54
ENV REF_LONGITUDE=56.98
ENV REF_RADIUS=1000

# Environment variables
ENV HADOOP_VERSION=3.3.6
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop-$HADOOP_VERSION
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin

# Get jdk, hadoop, and other dependencies
RUN apt update && \
    apt install openjdk-11-jdk wget ssh pdsh -y

RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xvzf hadoop-$HADOOP_VERSION.tar.gz -C /opt/ && \
    rm hadoop-$HADOOP_VERSION.tar.gz


# Configure hadoop
WORKDIR $HADOOP_HOME
RUN echo "export JAVA_HOME=$JAVA_HOME" >> ./etc/hadoop/hadoop-env.sh

COPY entrypoint.sh mapper.py reducer.py ./
RUN chmod +x entrypoint.sh mapper.py reducer.py

ENTRYPOINT ["./entrypoint.sh"]
CMD ["bash"]