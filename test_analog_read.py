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
import RPi.GPIO as GPIO

# Software SPI configuration for MCP3008:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#define LCD I2C

lcd = I2C_LCD_driver.lcd()

#Define header for csv log files
header_temp = ['time', 'temperature', 'arus', 'battery']

#Specify direcroty path of sensor log
dirpath = os.path.dirname(os.path.realpath(__file__))
filename_sensor = dirpath + '/log/sensor-now.txt'
filename_battery = dirpath + '/log/battery-now.txt'

#Define array of analog read value
global values
values = [0]*8

#Define DHT Type
DHT_number = dht.DHT22

#Define DHT PIN
DHT_input_pin = 22

#degree symbol
global degree
degree = unichr(176)

def get_temperature(dhttype, dhtpin):
	humi, temp = dht.read_retry(dhttype, dhtpin)
	return temp

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

def battery_now(filename, battery1, battery2, battery3, battery4):
	with open(filename, 'w') as now:
		now.write(str(battery1) + '\n')
		now.write(str(battery2) + '\n')
		now.write(str(battery3) + '\n')
		now.write(str(battery4) + '\n')

#module to write default IP Address in Raspberry Pi
def set_default(filename):
	default_data = """hostname
	clientid
	persistent
	option rapid_commit
	option domain_name_servers, domain_name, domain_search, host_name
	option classless_static_routes
	option ntp_servers
	option interface_mtu
	require dhcp_server_identifier
	slaac private
	interface eth0
	static ip_address=10.8.41.181/24
	static routers=10.8.41.1
	static domain_name_servers=10.8.41.1 8.8.8.8"""
	f = open(filename, "w")
	f.write(default_data)
	f.close

#module to restart the Pi
def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


print("Logging Temperature")
def main():

	#Define interval sensor update
	updateSensor = 300 #second interval update

	#initiate array of sensor data
	mcp_analog = [0]*8
	voltage_volt = [0]*4
	analogData_ch = [0]*8
	temp_read = 0

	#define timer
	tlog = time() #temp initial timer
	tnow = time()
	tread = time()

	#initiate analog data reading for MCP3008 and DHT22 average value
	for i in range (8):
		analogData_ch[i] = averagedata.averageData(10, 10, 'Analog Values Channel ' + str(i))
	tempData = averagedata.averageData(10, 10, 'Temperature Values')


	try:
		#begin loop
		while True:
			t1 = time()
			t2 = time()
			t3 = time()
			curr = random.randint(10,80)
			filename_date = strftime("%Y-%m")
			filename_log = dirpath + '/log/' + filename_date + '.csv'

			#read all analog pin from mcp3008 with interval of 1 second
			if t3 - tread >= 1:
				for i in range(8):
					values[i] = mcp.read_adc(i)
					analogData_ch[i].updateData(values[i])
					mcp_analog[i] = analogData_ch[i].runningAverage()
				temp_read = get_temperature(DHT_number, DHT_input_pin)
				tread = time()

			#get voltage analog value then convert to actual voltage
			voltage_volt[0] = (mcp_analog[0] / 1023) * 13.8
			voltage_volt[1] = (mcp_analog[1] / 1023) * 30.02
			voltage_volt[2] = (mcp_analog[2] / 1023) * 37.29
			voltage_volt[3] = (mcp_analog[3] / 1023) * 57.06

			for i in range(4):
				voltage_volt[i] = round(voltage_volt[i] , 1)


			battery_1 = voltage_volt[0]
			battery_2 = voltage_volt[1] - voltage_volt[0]
			battery_3 = voltage_volt[2] - voltage_volt[1]
			battery_4 = voltage_volt[3] - voltage_volt[2]
			#get DHT22 temperature
			tempData.updateData(temp_read)
			temp = tempData.runningAverage()
			temp = round(temp,2)
			sensorData = get_sensor_data(temp, curr, battery_1)
			if t1 - tlog >= updateSensor:
				write_sensor(filename_log, sensorData)
				tlog = time()

			if t2 - tnow >= 10:
				print('\nAverage Temperature: ' + str(temp))
        print('Average Voltage 1 : ' + str(battery_1))
			 	print('Average Voltage 2 : ' + str(battery_2))
			 	print('Average Voltage 3 : ' + str(battery_3))
			 	print('Average Voltage 4 : ' + str(battery_4))
      	lcd.lcd_display_string("Temp: " + str(temp) + degree + "C", 1)
    		lcd.lcd_display_string("Voltage: " + str(voltage_volt[0]) + "V", 2)
				sensor_now(filename_sensor, temp, curr, voltage_volt[0])
				battery_now(filename_battery, battery_1, battery_2, battery_3, battery_4)
				tnow = time()



	#if keyboard interrupt pressed
	except KeyboardInterrupt:
		print("Program Stopped")
		GPIO.cleanup()
if __name__ == "__main__":
	main()
