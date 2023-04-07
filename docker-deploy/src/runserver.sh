#!/bin/bash
while [ "1"=="1" ]
do
    taskset -c 0,1 python3 /newRoot/matchEngine/server.py
    sleep 1
done
