import bmm150
import math

device = bmm150.BMM150()

x, y, z = device.read_mag_data()

heading_rads = math.atan2(x, y)

heading_degrees = math.degrees(heading_rads)
