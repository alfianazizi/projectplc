#!/usr/bin/python

# Pin Allocation:
# Relay 1 : GPIO18
# Relay 2 : GPIO27
# DHT : GPIO22

from gpiozero import MCP3008, Button, OutputDevice
from time import sleep, strftime, time
from csv import writer
from subprocess import check_call
import os
import random
import Adafruit_DHT as dht
import Adafruit_MCP3008
import I2C_LCD_driver
import averagedata

# Software SPI configuration for MCP3008:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#define GPIO Pin for resetting all settings and senssing the charger
reset_pin = 24
charging_pin = 23

#define relay
relay_output = OutputDevice(18)
relay_input = OutputDevice(27)

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

def sensor_now(filename, temp, current, voltage, state):
	with open(filename, 'w') as now:
		now.write(str(temp) + '\n')
		now.write(str(current) + '\n')
		now.write(str(voltage) + '\n')
		now.write(state)

def battery_now(filename, battery1, battery2, battery3, battery4):
	with open(filename, 'w') as now:
		now.write(str(battery1) + '\n')
		now.write(str(battery2) + '\n')
		now.write(str(battery3) + '\n')
		now.write(str(battery4) + '\n')

#module to restart the Pi
def reboot():
	lcd.lcd_clear()
	lcd.lcd_display_string("Rebooting System", 1)
	check_call(['sudo', 'reboot'])

#module to write default IP Address in Raspberry Pi
def set_default():
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
	f = open("/etc/dhcpcd.conf", "w")
	f.write(default_data)
	f.close
	reboot()

def main():

	#Define interval sensor update
	updateSensor = 300 #second interval update

	#define factory reset button
	factory_reset_button = Button(reset_pin, hold_time=5)

	#define charger sensing logic
	charging_state = Button(charging_pin)

	#initiate array of sensor data
	mcp_analog = [0]*8
	voltage_volt = [0]*4
	current_amp = [0]*7
	analogData_ch = [0]*8
	temp_read = 0

	#define timer
	tlog = time() #temp initial timer
	tnow = time()
	tread = time()
	ttemp = time()
	tbat = time()

	#initiate analog data reading for MCP3008 and DHT22 average value
	for i in range (8):
		analogData_ch[i] = averagedata.averageData(150, 150, 'Analog Values Channel ' + str(i))
		tempData = averagedata.averageData(10, 10, 'Temperature Values')
		batteryPercent = averagedata.averageData(10, 10, 'Battery Percentage')

	try:
		#begin loop
		while True:
			t1 = time()
			curr = random.randint(10,80)
			filename_date = strftime("%Y-%m")
			filename_log = dirpath + '/log/' + filename_date + '.csv'

			#read all analog pin from mcp3008 with interval of 1 second
			if t1 - tread >= 0.075:
				for i in range(8):
					values[i] = mcp.read_adc(i)
					analogData_ch[i].updateData(values[i])
				tread = time()

			if t1 - ttemp >= 0.5:
				temp_read = get_temperature(DHT_number, DHT_input_pin)
				tempData.updateData(temp_read)
				ttemp = time()

			#get average value of all MCP3008 Channel
			for i in range(8):
				mcp_analog[i] = analogData_ch[i].runningAverage()

			#get DHT22 temperature
			temp = tempData.runningAverage()
			temp = round(temp,1)

			#sense the charging state
			#if charging is on then the voltage reference is bigger
			#get voltage analog value then convert to actual voltage

			if charging_state.value == True:
				charging_reference = 14
				state_charge = 'Charging'
			else:
				charging_reference = 10
				state_charge = 'Discharging'


			voltage_reference1 = 13.7
			voltage_reference2 = 70
			voltage_reference3 = 59
			voltage_reference4 = 56.6

			voltage_volt[0] = (mcp_analog[0] / 1023) * voltage_reference1
			voltage_volt[1] = (mcp_analog[1] / 1023) * voltage_reference2
			voltage_volt[2] = (mcp_analog[2] / 1023) * voltage_reference3
			voltage_volt[3] = (mcp_analog[3] / 1023) * voltage_reference4

			for i in range(4):
				voltage_volt[i] = round(voltage_volt[i] , 1)

			rescaled_voltage = voltage_volt[3] - 40
			battery_1 = voltage_volt[0]
			battery_2 = voltage_volt[1] - voltage_volt[0]
			battery_3 = voltage_volt[2] - voltage_volt[1]
			battery_4 = voltage_volt[3] - voltage_volt[2]
			#until here

			#get current value from 3 sensor ACS712
			for i in range(4, 7):
				current_amp[i] = round(((1.5 - (mcp_analog[i] * (3 / 1024.0))) / 0.066), 2)

			#power consumed by load, calculate with current * voltage output.
			#Output 1: current reading 1 * 12V
			#Output 2: current reading 1 * 24V
			#Output 3: current reading 1 * 48V
			power_output1 = round(current_amp[4]*12,0)
			power_output2 = round(current_amp[5]*24,0)
			power_output3 = round(current_amp[6]*48,0)
			total_power_usage = power_output1 + power_output2 + power_output3

			#get battery percentage by comparing voltage reading to reference voltage then multiply by 100
			if t1 - tbat >= 0.5:
				battery_read = (rescaled_voltage/charging_reference) * 100
				batteryPercent.updateData(battery_read)
				tbat = time()

			battery_percentage = batteryPercent.runningAverage()
			if battery_percentage > 100:
				battery_percentage = 100

			sensorData = get_sensor_data(temp, total_power_usage, battery_percentage)
			#check if factory reset button is pressed more than 5 second
			factory_reset_button.when_held = set_default

			if t1 - tlog >= updateSensor:
				write_sensor(filename_log, sensorData)
				tlog = time()

			if t1 - tnow >= 5:
				print('\nAverage Temperature: ' + str(temp))
				# print('Battery 1 : ' + str(battery_1) + 'V')
			 # 	print('Battery 2 : ' + str(battery_2) + 'V')
			 # 	print('Battery 3 : ' + str(battery_3) + 'V')
			 # 	print('Battery 4 : ' + str(battery_4) + 'V')
			 	print('Battery in series : ' + str(voltage_volt[3]) + 'V')
				for i in range(4):
					print('Battery ' + str(i) + ' : ' + str(voltage_volt[i]) + 'V')
			 	for i in range(4,7):
			 		print('Load ' + str(i-3) + ' : ' + str(current_amp[i]) + 'A')
			 	print('Total Power Usage : ' + str(total_power_usage) + 'W')
			 	print('Battery Capacity : ' + str(battery_percentage) + '%')
			 	print('State of Reset : ' + str(factory_reset_button.value))
			 	print('State of charging : ' + str(charging_state.value))
			 	lcd.lcd_display_string('-----RG-10------', 1)
				lcd.lcd_display_string('Temp: ' + str(temp) + 'C', 2)
				lcd.lcd_display_string('Battery: ' + str(round(battery_percentage,0)) + '%', 3)
				lcd.lcd_display_string('Load: ' + str(total_power_usage) + 'W', 4)
				sensor_now(filename_sensor, temp, total_power_usage, round(battery_percentage,0), state_charge)
				battery_now(filename_battery, voltage_volt[0], voltage_volt[1], voltage_volt[2], voltage_volt[3])
				# battery_now(filename_battery, battery_1, battery_2, battery_3, battery_4)
				tnow = time()

	#if keyboard interrupt pressed
	except KeyboardInterrupt:
		print("Program Stopped")
		#GPIO.cleanup()
if __name__ == "__main__":
	print("Logging Temperature")
	lcd.lcd_clear()
	main()
