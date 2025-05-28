#!/bin/bash

# NameNode가 처음 실행될 경우 포맷
if [ ! -d "/opt/hadoop/data/nameNode/current" ]; then
    echo "[INFO] Formatting NameNode..."
    hdfs namenode -format
fi

# NameNode 백그라운드로 실행
echo "[INFO] Starting NameNode..."
$HADOOP_HOME/bin/hdfs namenode &

# NameNode가 올라올 때까지 대기
sleep 5

# SafeMode 해제 시도
echo "[INFO] Leaving SafeMode..."
$HADOOP_HOME/bin/hdfs dfsadmin -safemode leave

# /data 디렉토리 생성 및 권한 설정
echo "[INFO] Creating /data directory in HDFS..."
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /data
$HADOOP_HOME/bin/hdfs dfs -chmod 777 /data

# 포그라운드 유지
tail -f /dev/null
