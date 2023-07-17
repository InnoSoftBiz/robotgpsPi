#!/usr/bin/env python3
import serial
from time import sleep
import json
import tty, sys, termios
#from pygame.locals import *
import sys


class keyController():
	def __init__(self):
		self.port = '/dev/ttyACM0'
		self.ser = serial.Serial(self.port, baudrate=115200, timeout=0.1)
		self.currency_L = 0
		self.currency_R = 0
		self.cur_troll = {}
		self.cur_troll["wheel-L"] = self.currency_L
		self.cur_troll["wheel-R"] = self.currency_R
		
	def key_controll(self,x):
		global lastkey
		x=sys.stdin.read(1)[0]
		if x != lastkey:
			self.currency_L = 0
			self.currency_R = 0
		#print("You pressed", x)
		if x == "w":
			print("GO!")
			#self.currency_L = 0.6
			#self.currency_R = 0.6
			self.currency_L += 0.01
			self.currency_R += 0.01
			if (self.currency_L >= 0.8) or (self.currency_R >= 0.8):
				self.currency_L = 0.8
				self.currency_R = 0.8
		elif x == "s":
			print("BACK!")
			#self.currency_L = -0.6
			#self.currency_R = -0.6
			self.currency_L -= 0.01
			self.currency_R -= 0.01
			if (self.currency_L <= -0.8) or (self.currency_R <= -0.8):
				self.currency_L = -0.8
				self.currency_R = -0.8
		elif x == "a":
			print("LEFT!")
			self.currency_L -= 0.01
			self.currency_R += 0.01
			if (self.currency_L <= -1.5) or (self.currency_R >= 1.5):
				self.currency_L = -1.5
				self.currency_R = 1.5
		
		elif x == "d":
			print("RIGHT!")
			self.currency_L += 0.01
			self.currency_R -= 0.01
			if (self.currency_L >= 1.5) or (self.currency_R <= -1.5):
				self.currency_L = 1.5
				self.currency_R = -1.5
			
				
		lastkey = x
		#print((self.currency_L,self.currency_R)
		return (self.currency_L,self.currency_R)
			
	def port_controll(self):
		self.ser.reset_input_buffer()
			
	def send_controll(self):
		self.cur_troll["wheel-L"] = self.currency_L
		self.cur_troll["wheel-R"] = self.currency_R
		sendtroll = json.dumps(self.cur_troll)
		bytes_troll = sendtroll.encode('ascii')
		self.ser.write(bytes_troll + b"\n")
		#line = self.ser.readline().decode('utf-8').rstrip()
		#print(line)
		return sendtroll
		#time.sleep(0.05)
		
if __name__ == '__main__':
	filedescriptors = termios.tcgetattr(sys.stdin)
	tty.setcbreak(sys.stdin)
	x = ""
	lastkey = ""
	key = keyController()
	key.port_controll()
	while True:
		key.key_controll(x)
		key.send_controll()
	
