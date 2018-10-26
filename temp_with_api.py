#!/usr/bin/python

from flask import Flask
from gpiozero import CPUTemperature
from time import sleep, strftime, time
from csv import writer
import os
import thread
app = Flask(__name__)


sensor = {
	'time' : 'time',
	'temperature' : 'temperature'
}


cpu = CPUTemperature()
header_temp = ['time', 'temperature']
dirpath = os.path.dirname(os.path.realpath(__file__))
filename_date = strftime("%Y-%m")
filename_temp = dirpath + '/log/' + filename_date + '-temp.csv'
updateTemp = 5 #5 second interval update
tt = time() #temp initial timer

print("Logging Temperature")

def get_temp_data():
	while True:
		global temp_data
		temp_data = []
		t1 = time()
		if t1 - tt >= updateTemp:
			temp_data.append(strftime("%Y-%m-%d %H:%M:%S"))
			temp_data.append(cpu.temperature)
			tt = time()

@app.route("/api/v1/sensor")
def index():
	sensor = {
		'time' : temp_data[1],
		'temperature' : temp_data[2]
	}
	return jsonify(sensor)

if __name__ == "__main__":
	thread.start_new_thread(get_temp_data, ())
	app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
