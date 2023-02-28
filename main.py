import time
import json
import requests
import socket
from multiprocessing import Array, Process, Lock

def get_weather(output):
	# Get own API key
	api="https://openweathermap.org/api"
	lat=55.81632
	lon=49.18270
	icons={
	'01d':'\ue30d',
	'02d':'\ue302',
	'03d':'\ue33d',
	'04d':'\ue312',
	'09d':'\ue312',
	'10d':'\ue306',
	'11d':'\ue31c',
	'13d':'\ue31a',
	'50d':'\ue313',
	'01n':'\ue32b',
	'02n':'\ue37e',
	'03n':'\ue33d',
	'04n':'\ue312',
	'09n':'\ue312',
	'10n':'\ue326',
	'11n':'\ue31c',
	'13n':'\ue31a',
	'50n':'\ue313'
	}
	while 1:
		url="http://api.openweathermap.org/data/2.5/weather?units=metric&lat={}&lon={}&appid={}".format(lat,lon,api)
		while True:
			try:
				data=json.loads(requests.get(url).content)
				break
			except:
				pass
		icon=icons[data['weather'][0]['icon']]
		temp="{}".format(data['main']['temp'])
		output.value="{}  {}".format(icon,temp).encode('u8')
		time.sleep(300)

if __name__=="__main__":
	lock=Lock()
	weather=Array('c',b' '*11,lock=lock)
	Process(target=get_weather, args=(weather,)).start()
	port=1024
	s = socket.socket()
	while 1:
		try:
			s.bind(('0.0.0.0', port))
			break
		except:
			pass
	print ('start')
	s.listen()
	while True:
		c, addr = s.accept()
		if b"    " in weather[:].split(b"\x00")[0]:
			c.send(b"")
		else:
			c.send(weather[:].split(b"\x00")[0])
		c.close()
