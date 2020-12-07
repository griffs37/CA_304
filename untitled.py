#!/usr/bin/env python3

import threading
import argparse
import os
import socket

class Send(threading.Thread):
	def __init__(self, sock, name):
		super().__init__()
		self.sock = sock
		self.name = name 

	def run(self):
		while True:
			message = input(f"{self.name}: ")

			if message == "--quit":   # type --quit to exit the chatroom
				self.sock.sendall(f"Server: {self.name} has left the chat :(").encode("ascii")
				break

			else:   # send message for broadcasting
				self.sock.sendall(f"{self.name}: {message}").encode("ascii")
