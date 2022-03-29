#https://www.studytonight.com/network-programming-in-python/handling-received-data
import socket
host = socket.gethostname()
port = 12345
s = socket.socket()		# TCP socket object

s.connect((host,port))
data='This will be sent to server'.encode()
s.sendall(data)    # Send This message to server

data = s.recv(1024)	    # Now, receive the echoed
					    # data from server

print (data.decode())			# Print received(echoed) data
s.close()				# close the connection
