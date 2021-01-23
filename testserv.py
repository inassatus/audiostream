import socket


def addr2b(addr):
	ip, port = addr
	if ip=="192.168.0.1":
		ip="1.248.169.25"
	return (ip+":"+str(port)).encode()

def b2addr(comb):
	des = comb.split(":")
	ip = des[0]
	port = int(des[1])
	return (ip, port) 

def maintainconn(dic, socket):
	for v in dic.values():
		socket.sendto("server".encode(), v)
	return



ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("server: created")

hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
port = 80
matchdict = {}

ss.bind((host, port))
print("server: bound to", host, "on", port)

while True:
	data, addr = ss.recvfrom(4096)
	if data:
		print("request from: ", addr)
		print("request: ", data)
		data = data.decode()
		if(len(data.split('@'))<2):
			ss.sendto("wrong request".encode(), addr)
			continue
		fp = data.split("@")[1]
		#from user = fp
		tp = data.split('@')[0]
		#to user = tp
		indict = False
		for key in matchdict:
			if key==fp:
				ss.sendto(addr2b(matchdict[fp]), addr)
				ss.sendto(addr2b(addr), matchdict[fp])
				indict = True
		
		if indict:
			del matchdict[fp]
			continue

		ss.sendto("server".encode(), addr)
		matchdict[tp] = addr
