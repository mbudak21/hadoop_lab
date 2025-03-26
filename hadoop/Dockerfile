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

# Get jdk, ssh, and other dependencies
RUN apt update && \
    apt install openjdk-11-jdk wget ssh openssh-server pdsh cron -y && \
    mkdir /var/run/sshd

# Get hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xvzf hadoop-$HADOOP_VERSION.tar.gz -C /opt/ && \
    rm hadoop-$HADOOP_VERSION.tar.gz

# Configure ssh
RUN ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

# Configure hadoop
WORKDIR $HADOOP_HOME
RUN echo "export JAVA_HOME=$JAVA_HOME" >> ./etc/hadoop/hadoop-env.sh
COPY core-site.xml hdfs-site.xml yarn-site.xml ./etc/hadoop/

COPY loop_jobs.sh run_job.sh entrypoint.sh mapper.py reducer.py ./
RUN chmod +x loop_jobs.sh run_job.sh entrypoint.sh mapper.py reducer.py

# Configure cron
# RUN echo "* * * * * root /opt/hadoop-3.3.6/run_job.sh >> /opt/hadoop-3.3.6/cron_log.txt 2>&1" > /etc/cron.d/hadoop_job
# RUN chmod 0644 /etc/cron.d/hadoop_job

# # Start cron service on container start
# RUN echo "cron" >> /opt/hadoop-3.3.6/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD ["bash"]