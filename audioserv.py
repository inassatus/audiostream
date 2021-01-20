import sounddevice as sd
import numpy
from threading import Thread
import socket
import time


def b2addr(comb):
	comb = comb.decode()
	des = comb.split(":")
	ip = des[0]
	port = int(des[1])
	return (ip, port) 

def v2b(data):
	return data.tobytes()

def b2v(data):
	return numpy.frombuffer(data, dtype=numpy.float32)


class mystream():
	def __init__(self):
		self.ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.dev = sd.Stream()
		self.buffer = 4096
		self.str = False
		self.overflow = False
		self.underflow = False
		self.peer = None
		self.est = False

	def streaming(self):
		self.dev.start()
		self.str = True
		reading = Thread(target=self.keepread)
		reading.start()
		while self.str:
			self.write2peer()
		reading.join()
		self.endcall()
		self.dev.stop()
		self.dev.abort()

	def keepread(self):
		while self.str:
			self.readfrompeer()
	
	def readfrompeer(self):
		data, addr = self.ss.recvfrom(self.buffer*8)
		if data==b"endcall":
			print("your peer", self.peer, " exited")
			self.str = False
			return
		data = b2v(data)
		self.underflow = self.dev.write(data)
		if self.underflow:
			print("output underflow")

	def write2peer(self):
		data, self.overflow = self.dev.read(self.buffer)
		data = v2b(data)
		self.ss.sendto(data, self.peer)
		if self.overflow:
			print("input overflow")

	def endcall(self):
		self.ss.sendto("endcall".encode(), self.peer)

	def get_input(self):
		key = input()
		if key == '':
			self.str = False

	def request(self, host, port):
		self.ss.bind(("", 0))
		self.ss.sendto(b'0', (host, port))
		print("requesting to server")
		self.conn()

	def conn(self):
		data, addr = self.ss.recvfrom(64)
		self.peer = b2addr(data)
		sending = Thread(target=self.initping)
		recving = Thread(target=self.getping)
		sending.start()
		recving.start()
		sending.join()
		recving.join()
		print("You are connected to your peer ", self.peer)

	def initping(self):
		for i in range(50):
			self.ss.sendto("ping".encode(), self.peer)
			time.sleep(1)
			if self.est:
				return

	def getping(self):
		data, addr = self.ss.recvfrom(64)
		if addr==self.peer:
			self.est = True
		return



a = mystream()
a.request("192.168.0.10", 80)
#stun server that i implemented
#for git, see NAT-HOLE-PUNCH repo, stun server is there as name testserv.py
stream = Thread(target=a.streaming)
stream.start()
a.get_input()
stream.join()