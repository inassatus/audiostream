import sounddevice as sd
import numpy
import threading
import socket


class mystream():
	def __init__(self):
		self.socket = 
		self.dev = sd.Stream()
		self.buffer = 8192
		self.str = False
		self.overflow = False
		self.underflow = False

	def streaming(self):
		lock = threading.Lock()
		lock.acquire()
		self.dev.start()
		self.str = True
		while self.str:
			data, self.overflow=self.dev.read(self.buffer)
			self.underflow = self.dev.write(data)
			if self.overflow:
				print("input overflow")
			if self.underflow:
				print("output underflow")
		self.dev.stop()
		self.dev.abort()
		lock.release()

	def get_input(self):
		key = input()
		if key == '':
			self.str = False

	def stop(self):
		self.str = False

maxt = 3

a = []
for i in range(maxt):
	temp = mystream()
	a.append(temp)

t = []

for i in range(maxt):
	temp = threading.Thread(target = a[i].streaming)
	temp.start()
	t.append(temp)


for i in range(maxt):
	a[i].get_input()
	t[i].join()


ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
port = 5000

ss.bind(host, port)

