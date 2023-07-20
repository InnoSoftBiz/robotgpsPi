import bmm150
import math

device = bmm150.BMM150()

while True:

	x, y, z = device.read_mag_data()

	heading_rads = math.atan2(x, y)
	heading_degrees = math.degrees(heading_rads)

	print(f"X : {x:.2f}uT")
	print(f"Y : {y:.2f}uT")
	print(f"Z : {z:.2f}uT")

	print(f"Heading : {(heading_degrees+ 360) % 360:.2f}Deg")
