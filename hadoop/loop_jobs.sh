#!/bin/bash
set -e

# Runs indefinitely, calling run_job.sh every 60 seconds
while true
do
  echo "Running run_job.sh at $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
  /opt/hadoop-3.3.6/run_job.sh >> /opt/hadoop-3.3.6/loop_jobs.log 2>&1
  echo "Job finished, sleeping..."
  sleep 60
done
