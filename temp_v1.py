from gpiozero import CPUTemperature
from time import sleep, strftime, time
from csv import writer
import os

cpu = CPUTemperature()
header = ['time', 'temperature']
filename_date = strftime("%Y-%m")
filename_temp = filename_date + '-temp.csv'
updateTemp = 5 #5 second interval update
tt = time() #temp initial timer

print("Logging Temperature")
print(filename_date)

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
			temp_writer.writerow(header)
		temp_writer.writerow(data)

while True:
	data = get_temp_data()
	t1 = time()
	if t1 - tt >= updateTemp:
		write_temp(filename_temp, data)
		tt = time()
