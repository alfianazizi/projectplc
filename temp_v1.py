#!/usr/bin/python

from gpiozero import CPUTemperature
from time import sleep, strftime, time
from csv import writer
import os
import random

cpu = CPUTemperature()
header_temp = ['time', 'temperature', 'arus', 'battery']
dirpath = os.path.dirname(os.path.realpath(__file__))
filename_date = strftime("%Y-%m")
# filename_temp = dirpath + '/log/' + filename_date + '-temp.csv'
# filename_current = dirpath + '/log/' + filename_date + '-current.csv'
# filename_voltage = dirpath + '/log/' + filename_date + '-voltage.csv'
filename_log = dirpath + '/log/' + filename_date + '.csv'
filename_sensor = dirpath + '/log/sensor-now.txt'
updateSensor = 10 #second interval update
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

# def write_current(filename,data):
# 	with open(filename, 'a') as log:
# 		file_is_empty = os.stat(filename).st_size == 0
# 		current_writer = writer(log, lineterminator='\n')
# 		if file_is_empty:
# 			current_writer.writerow(header_current)
# 		current_writer.writerow(data)

# def write_voltage(filename,data):
# 	with open(filename, 'a') as log:
# 		file_is_empty = os.stat(filename).st_size == 0
# 		voltage_writer = writer(log, lineterminator='\n')
# 		if file_is_empty:
# 			voltage_writer.writerow(header_voltage)
# 		voltage_writer.writerow(data)

def sensor_now(filename, temp, current, voltage):
	with open(filename, 'w') as now:
		now.write(str(temp) + '\n')
		now.write(str(current) + '\n')
		now.write(str(voltage) + '\n')


while True:
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
