import socket
from flush_module import *
from chkdisk import *
import os

def main():
	f = open('/usr/bin/spinDownDevices','r')
        Str = f.read()
        List = Str.split('\n')
        List.remove('')
        f.close()
	serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serv.bind(('',12321))
	while 1:
		serv.listen(1)
		conn, addr = serv.accept()
		data = conn.recv(512)
		if data == '*!':
			perc = check('/dev/sdh')
		 	if perc > 8:
			    for i in List:
				os.system('mount -t xfs -L %s /srv/node/%s'%(i,i))	
			    flush()
			    for i in range(ord('d'),ord('g')):
				os.system('umount /dev/sd%s'%(chr(i)))
		conn.send('done')

if __name__ == '__main__':
	main()
