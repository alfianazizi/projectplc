#!/usr/bin/python

# Pin Allocation:
# Relay 1 : GPIO18
# Relay 2 : GPIO27
# DHT : GPIO22


from gpiozero import MCP3008
from time import sleep, strftime, time
from csv import writer
import os
import random
import Adafruit_DHT as dht
import Adafruit_MCP3008
import I2C_LCD_driver
import averagedata

# Software SPI configuration for MCP3008:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


#Define array of analog read value
global values
values = [0]*8

#Define DHT Type
DHT_number = dht.DHT22

#Define DHT PIN
DHT_input_pin = 22 


#Define header for csv log files
header_temp = ['time', 'temperature', 'arus', 'battery']

#Specify direcroty path of sensor log
dirpath = os.path.dirname(os.path.realpath(__file__))
filename_sensor = dirpath + '/log/sensor-now.txt'

#Define interval sensor update
updateSensor = 300 #second interval update
tlog = time() #temp initial timer
tnow = time()
tread = time()

def get_temperature(dhttype, pin):
	humi, temp = dht.read_retry(dhttype, dhtpin)
	return temp

def get_voltage()
	

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



print("Logging Temperature")
def main():
	voltage_analog = [0]*4
	voltage_volt = [0]*4
	for i in range (8):
		analogData_ch[i] = averagedata.averageData(10, 10, 'Analog Values Channel ' + str(i))
	tempData = averagedata.averageData(10, 10, 'Temperature Values')
	try:
		while True:
			t1 = time()
			t2 = time()
			t3 = time()
			filename_date = strftime("%Y-%m")
			filename_log = dirpath + '/log/' + filename_date + '.csv'

			#read all analog pin from mcp3008 with interval of 1 second
			if t3 - tread >= 1:
				for i in range(8):
					values[i] = mcp.read_adc(i)
					analogData_ch[i].updateData(values[i])
				temp_read = get_temperature(DHT_number, DHT_input_pin)
				tread = time()

			#get voltage analog value then convert to actual voltage
			for i in range(4):
				voltage_analog[i] = analogData_ch[i].runningAverage()
				voltage_volt[i] = (voltage_analog[i] / 1023) * 16.5

			#get DHT22 temperature
			tempData.updateData(temp_read)
			temp = tempData.runningAverage()
			print('\nAverage Temperature: ' + str(temp))
			
			sensorData = get_sensor_data(temp, curr, volt)
			if t1 - tlog >= updateSensor:
				write_sensor(filename_log, sensorData)
				tlog = time()

			if t2 - tnow >= 5:
				sensor_now(filename_sensor, cpu.temperature, curr, volt)
				tnow = time()



	#if keyboard interrupt pressed
	except KeyboardInterrupt:
		print("Program Stopped")

if __name__ == "__main__":
	main()