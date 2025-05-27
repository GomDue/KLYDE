#!/bin/bash

# 데이터 노드 디렉토리 초기화
rm -rf /opt/hadoop/data/dataNode/*

# 권한 설정
chown -R hadoop:hadoop /opt/hadoop/data/dataNode
chmod 755 /opt/hadoop/data/dataNode

# 데이터노드 실행
hdfs datanode
