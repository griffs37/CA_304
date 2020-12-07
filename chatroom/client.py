#!/usr/bin/env python3

import threading
import argparse
import os
import socket

class Send(threading.Thread):
	"""
	Listen for user input
	
	Attributes:
		sock: the connected socket
		name: the username of the user
	
	"""
	def __init__(self, sock, name):
		super().__init__()
		self.sock = sock
		self.name = name 

	def run(self):
		"""
		Listens for user input, sends to server
		Type --quit to close the connection
		
		"""
		while True:
			message = input("{}: ".format(self.name))

			if message == "--quit":   # type --quit to exit the chatroom
				self.sock.sendall("Server: {} has left the chat :(".format(self.name).encode("ascii"))
				break

			else:   # send message for broadcasting
				self.sock.sendall("{}: {}".format(self.name, message).encode("ascii"))

		print("\nQuitting, goodbye!")
		self.sock.close()
		os._exit(0)

class Receive(threading.Thread):
	"""
	Receiving thread listens for incoming messages

	Attributes:
		sock: connected socket object
		name: name of user
	"""
	def __init__(self, sock, name):
		super().__init__()
		self.sock = sock
		self.name = name

	def run(self):
		"""
		Listens for incoming data until the server has closed
		"""
		while True:
			message = self.sock.recv(1024)
			if message:
				print("\r{}\n{}: ".format(message.decode("ascii"), self.name), end="")
			else:
				print("\nConnection to the server has been lost, quitting...")
				self.sock.close()
				os._exit(0)

class Client:
	"""
	Supports client-server connections

	Attributes:
		host: the ip addr of the servers listening socket
		port: the port number of the servers listening socket
		sock: the connected socket
	"""
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def start(self):
		"""
		Establishes the client-server connection, gathers username info, creates and starts threads to send and receive

		Returns:
			A receive object of the receiving thread
		"""
		print("Trying to connect to {}:{}...".format(self.host, self.port))
		self.sock.connect((self.host, self.port))   # conect to the socket
		print("You are connected to {}:{}\n".format(self.host, self.port))
		
		name = input("Your name: ")
		
		print()
		print("Welcome {}! Getting ready to send and receive messages...".format(name))

		send = Send(self.sock, name)   # create send and receive threads
		receive = Receive(self.sock, name)
		send.start()
		receive.start()   # start threads

		self.sock.sendall("Server: {} has joined the chat".format(name).encode("ascii"))
		print("\rYou can leave the chatroom by typing '--quit'\n")
		print("{}: ".format(name), end="")



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Chatroom Server")
	parser.add_argument("host", help="Interface the server listens at")
	parser.add_argument("-p", metavar="PORT", type=int, default=1060, help="TCP port (default 1060)")
	args = parser.parse_args()
	client = Client(args.host, args.p)
	client.start()  # start the thread named client 





















