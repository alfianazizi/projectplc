#!/usr/bin/python

from gpiozero import MCP3008
import Adafruit_DHT as dht
from time import sleep, strftime, time
from csv import writer
import os
import random

#Define DHT Type
DHT_TYPE = dht.DHT22

#Define DHT PIN
DHT_PIN = 23 

#Define sensor channel in MCP3008
current_pin = 0
voltage_pin = 1

#Read value of ADC reading
current_channel= MCP3008(current_pin)
voltage_channel = MCP3008(voltage_pin)

#Define header for csv log files
header_temp = ['time', 'temperature', 'arus', 'battery']

#Specify direcroty path of sensor log
dirpath = os.path.dirname(os.path.realpath(__file__))
filename_date = strftime("%Y-%m")
filename_log = dirpath + '/log/' + filename_date + '.csv'
filename_sensor = dirpath + '/log/sensor-now.txt'

#Define interval sensor update
updateSensor = 300 #second interval update
tt = time() #temp initial timer
tn = time()

print("Logging Temperature")


def get_temperature(dhttype, pin):
	humi, temp = dht.read_retry(dhttype, dhtpin)
	return temp

def get_current():
	

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

def main():
	try:
		while True:
			sensorData = get_sensor_data(temp, curr, volt)
			t1 = time()
			t2 = time()
			if t1 - tt >= updateSensor:
				write_sensor(filename_log, sensorData)
				tt = time()

			if t2 - tn >= 5:
				sensor_now(filename_sensor, cpu.temperature, curr, volt)
				tn = time()



	#if keyboard interrupt pressed
	except KeyboardInterrupt:
		print("Program Stopped")

if __name__ == "__main__":
	main()