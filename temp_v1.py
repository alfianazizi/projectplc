#!/usr/bin/python

from gpiozero import CPUTemperature
from time import sleep, strftime, time
from csv import writer
import os
import random

cpu = CPUTemperature()

#Define header for csv log files
header_temp = ['time', 'temperature', 'arus', 'battery']

#Specify direcroty path of sensor log
dirpath = os.path.dirname(os.path.realpath(__file__))
# filename_date = strftime("%Y-%m")
filename_log = dirpath + '/log/' + filename_date + '.csv'
filename_sensor = dirpath + '/log/sensor-now.txt'
<<<<<<< HEAD
updateSensor = 10 #second interval update
=======

#Define interval sensor update
updateSensor = 300 #second interval update
>>>>>>> c32a10fec787863f8f9a733ffc46bcdcca46c552
tt = time() #temp initial timer
tn = time()


print("Logging Temperature")

def get_sensor_data(temperature, current, voltage):
	sensor_data = []
	sensor_data.append(strftime("%Y-%m-%d %H:%M:%S"))
	sensor_data.append(temperature)
	sensor_data.append(current)
	sensor_data.append(voltage)

	return sensor_data

def write_sensor(filename, data):
	with open(filename, 'a') as log:
		file_is_empty = os.stat(filename).st_size == 0
		temp_writer = writer(log, lineterminator='\n')
		if file_is_empty:
			temp_writer.writerow(header_temp)
		temp_writer.writerow(data)

def sensor_now(filename, temp, current, voltage):
	with open(filename, 'w') as now:
		now.write(str(temp) + '\n')
		now.write(str(current) + '\n')
		now.write(str(voltage) + '\n')


while True:
	filename_date = strftime("%Y-%m")
	temp = cpu.temperature
	curr = random.randint(10,80)
	volt = random.randint(60,100)
	sensorData = get_sensor_data(temp, curr, volt)
	t1 = time()
	t2 = time()
	if t1 - tt >= updateSensor:
		write_sensor(filename_log, sensorData)
		tt = time()

	if t2 - tn >= 5:
		sensor_now(filename_sensor, cpu.temperature, curr, volt)
		tn = time()
