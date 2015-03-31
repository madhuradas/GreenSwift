import socket
import os

def make_conn():
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client.connect(('',12321))
	client.send('*!')
	data = client.recv(512)
	client.close()
	return 1
