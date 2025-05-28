#!/bin/bash

# DataNode의 데이터 디렉토리 초기화
echo "[INFO] Cleaning DataNode directory..."
rm -rf /opt/hadoop/data/dataNode/*

# 권한 설정
echo "[INFO] Setting permissions for DataNode directory..."
chown -R hadoop:hadoop /opt/hadoop/data/dataNode
chmod 755 /opt/hadoop/data/dataNode

# DataNode 실행
echo "[INFO] Starting DataNode..."
hdfs datanode &

# HDFS 클러스터 상태 점검 및 복구 시도
echo "[INFO] Checking HDFS cluster health..."
$HADOOP_HOME/bin/hdfs fsck / -files -blocks -locations

# 클러스터 상태 복구 시도
echo "[INFO] Attempting to recover missing blocks..."
$HADOOP_HOME/bin/hdfs dfsadmin -recoverBlocks

# 포그라운드 유지
tail -f /dev/null
