import bmm150
import math

def compass():
	device = bmm150.BMM150()
	while True:
		x, y, z = device.read_mag_data()

		heading_rads = math.atan2(x, y)
		heading_degrees = math.degrees(heading_rads)
		heading_degrees = int((heading_degrees + 360) % 360)
		
		yield heading_degrees
	
if __name__ == '__main__':
	for i in compass():
		print(i)
