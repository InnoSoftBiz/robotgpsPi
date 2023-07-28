import bmm150
import math
import time

def compass():
	device = bmm150.BMM150()
	while True:
		x, y, z = device.read_mag_data()

		heading_rads = math.atan2(x, y)
		heading_degrees = math.degrees(heading_rads)
		heading_degrees = round(heading_degrees)
		
		print(heading_degrees)
		time.sleep(0.5)
	
if __name__ == '__main__':
	compass()
