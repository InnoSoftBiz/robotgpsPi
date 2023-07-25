import json
# import bmm150
import tty, sys, termios
import serial

def turn(deg):
	# x, y, z = device.read_mag_data()

	# heading_rads = math.atan2(x, y)
	# heading_degrees = math.degrees(heading_rads)
	# heading_degrees = int((heading_degrees + 360) % 360)
	heading_degrees = int(input("BMM150: "))
	
	if heading_degrees < deg - 5:
		controll["vl"] = 0.1
		controll["vr"] = -0.1
		
	elif heading_degrees > deg + 5:
		controll["vl"] = -0.1
		controll["vr"] = 0.1
	else:
		controll["vl"] = 0
		controll["vr"] = 0
	
	send = json.dumps(controll)
	bytes_send = send.encode('ascii')
	#line = ser.readline().decode('utf-8').rstrip()
	print(send)
	#ser.write(bytes_send  + b"\n")
	
#ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=3000)
controll = {}
controll["vl"] = 0
controll["vr"] = 0
# device = bmm150.BMM150()
while True:
	turn(90)
