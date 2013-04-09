import socket
import sys
try:    
	import thread 
except ImportError:
	import _thread as thread

class port_forwarding:
	def __init__(self, ip, port, listen_port):
		thread.start_new_thread(self.server, (ip, port, listen_port))
		lock = thread.allocate_lock()
		lock.acquire()
		lock.acquire()

	def server(self, ip, port, listen_port):
		try:
			print("ip:" + ip + " port:" + str(port) + " listen-port:" + str(listen_port))
			dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			dock_socket.bind(('', listen_port))
			dock_socket.listen(5)
			while True:
				client_socket, address = dock_socket.accept()
				server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				server_socket.connect((ip, port))
				thread.start_new_thread(self.forward, (client_socket, server_socket))
				thread.start_new_thread(self.forward, (server_socket, client_socket))
		except Exception as e:
			print("Server exception:" + str(e))
		finally:
			thread.start_new_thread(self.server, settings)

	def forward(self, source, destination):
		buffer = ' '
		while buffer:
			buffer = source.recv(1024)
			if buffer:
				destination.sendall(buffer)
		else:
			try:
				source.shutdown(socket.SHUT_RDWR)
				destination.shutdown(socket.SHUT_RDWR)
			except Exception as e:
				print("Forward exception:" + str(e))

if __name__ == '__main__':
	if len(sys.argv) != 4 :
		print("Usage: python port-forwading.py <ip/dns> <port> <listen port>")
		sys.exit()
	demon = port_forwarding(str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
