#!/bin/bash
if [ "$1" = "-g" ]
then
echo .1.3.6.1.2.1.25.1.7.1
echo gauge
cat /home/pi/projectplc/log/sensor-now.txt | head -1
fi
exit 0
