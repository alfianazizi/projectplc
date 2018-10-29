#!/usr/bin/python

from flask import Flask
from flask import jsonify
from gpiozero import CPUTemperature
from time import sleep, strftime, time
from csv import writer
import os
import threading
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
updateTemp = 2 #5 second interval update
global tt
tt = time() #temp initial timer

print("Logging Temperature")

def get_temp_data():
	while True:
		global temp_data, tt
		temp_data = []
		t1 = time()
		if t1 - tt >= updateTemp:
			temp_data.append(strftime("%Y-%m-%d %H:%M:%S"))
			temp_data.append(str(cpu.temperature))
			tt = time()

@app.route("/api/v1/sensor")
def index():
	sensor = {
		'time' : strftime("%Y-%m-%d %H:%M:%S"),
		'temperature' : str(cpu.temperature)
	}
	return jsonify(sensor)

if __name__ == "__main__":
	#threading.Thread(target=get_temp_data).start()
	app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
