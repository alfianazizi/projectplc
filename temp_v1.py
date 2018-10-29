#!/usr/bin/python

from gpiozero import CPUTemperature
from time import sleep, strftime, time
from csv import writer
import os
import random

cpu = CPUTemperature()
header_temp = ['time', 'temperature']
dirpath = os.path.dirname(os.path.realpath(__file__))
filename_date = strftime("%Y-%m")
filename_temp = dirpath + '/log/' + filename_date + '-temp.csv'
filename_current = dirpath + '/log/' + filename_date + '-current.csv'
filename_voltage = dirpath + '/log/' + filename_date + '-voltage.csv'
filename_sensor = dirpath + '/log/sensor-now.txt'
updateSensor = 120 #second interval update
tt = time() #temp initial timer
tn = time()

print("Logging Temperature")

def get_temp_data():
	temp_data = []
	temp_data.append(strftime("%Y-%m-%d %H:%M:%S"))
	temp_data.append(cpu.temperature)

	return temp_data

def write_temp(filename,data):
	with open(filename, 'a') as log:
		file_is_empty = os.stat(filename).st_size == 0
		temp_writer = writer(log, lineterminator='\n')
		if file_is_empty:
			temp_writer.writerow(header_temp)
		temp_writer.writerow(data)

def write_current(filename,data):
	with open(filename, 'a') as log:
		file_is_empty = os.stat(filename).st_size == 0
		current_writer = writer(log, lineterminator='\n')
		if file_is_empty:
			current_writer.writerow(header_current)
		current_writer.writerow(data)

def write_voltage(filename,data):
	with open(filename, 'a') as log:
		file_is_empty = os.stat(filename).st_size == 0
		voltage_writer = writer(log, lineterminator='\n')
		if file_is_empty:
			voltage_writer.writerow(header_voltage)
		voltage_writer.writerow(data)

def sensor_now(filename, temp, current, voltage):
	with open(filename, 'w') as now:
		now.write(temp + '\n')
		now.write(current + '\n')
		now.write(voltage + '\n')

while True:
	temp = get_temp_data()
	t1, t2 = time()
	
	if t1 - tt >= updateSensor:
		write_temp(filename_temp, temp)
		write_current(filename_current, curr)
		write_voltage(filename_voltage ,volt)
		tt = time()

	if t2 - tn >= 5:
		sensor_now(filename_sensor, cpu.temperature, random.randint(10,80), random.randint(60,100))
		tn = time()
