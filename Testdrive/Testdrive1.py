# import json
# import bmm150
import tty, sys, termios
import serial
import math

def turn(deg):
	# x, y, z = device.read_mag_data()

	# heading_rads = math.atan2(x, y)
	# heading_degrees = math.degrees(heading_rads)
	# heading_degrees = round((heading_degrees + 360) % 360)
	# #heading_degrees = int(input("BMM150: "))
	# controll["compass"] = heading_degrees
	
	# if (heading_degrees >= deg + 5):
		# controll["vl"] = -0.05
		# controll["vr"] = 0.05
	
	# elif(heading_degrees <= deg - 5):
		# controll["vl"] = 0.05
		# controll["vr"] = -0.05
		
	# # elif heading_degrees > deg + 5:
		# # controll["vl"] = 0.05
		# # controll["vr"] = -0.05
	# elif deg - 5 <= heading_degrees <= deg + 5:
		# controll["vl"] = 0
		# controll["vr"] = 0
		# #print("OK!")
		# #deg = int(input("Deg : "))
	
	# send = json.dumps(controll)
	bytes_send = str(deg).encode('utf-8')
	line = ser.readline().decode('utf-8').rstrip()
	ser.write(bytes_send + b"\n")
	print(line)
	
ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0.1)
# controll = {}
# controll["vl"] = 0
# controll["vr"] = 0
# # controll["compass"] = 0
# device = bmm150.BMM150()
deg = int(input("BMM150: "))
while True:
	turn(deg)
