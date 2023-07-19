import bmm150
import math

device = bmm150.BMM150()

x, y, z = device.read_mag_data()


