import time
import math
#import threading
import json
#import multiprocessing
import bmm150
from multiprocessing import Process, Queue
import serial
import pynmea2

import gps
import WaypointNavigationAlgorithm as wna
import mqtt
import File_kml as kml
import move_robot as mr
import filewaypoint as mp
import hard_controll as hc

class mainR:
	
	def __init__(self):
		self.file_kml = "waypoint.kml"
		self.pos = {}
		self.travel = {}
		#self.posrobot = [0,0]
			
	def robot_move(self, posrobot, path, compass):
		mainpath = self.file_thread().copy()
		# self.waypoint1 = gps.GPSModule().read_gps_data()
		# robot = mr.Robot(L, posrobot, path[0], path[1], compass)
		#print(compass)
		robot = hc.Robot_hard(posrobot, path, compass)
		if len(path) > 0:
			#robot.follow_path()
			robot.move_h()
			#print(f"V : {robot.u}")
			if wna.Waypoint(posrobot, path[0][0]).haversine() < 0.0001:
				path[0].pop(0)
				if path[0][0] == mainpath[0]:
					path[1].pop(0)
					mainpath.pop(0)
		#print(self.pos)
	
	def cal_thread(self, posrobot):
		waypoints = self.file_thread().copy()
		waypoints.insert(0,posrobot)
		Nwaypoints = []
		theta = []
		for i in range(len(waypoints)-1):
			start = waypoints[i]
			goal = waypoints[i+1]
			set_upcal = wna.Waypoint(start,goal)
			set_upcal.haversine()
			set_upcal.bearing()
			des = set_upcal.destination(start)
			#print("All polt:", (haver, bear, des))
			Nwaypoints.append(start)
			theta.append(round(set_upcal.bearing()[1]))
				
			for j in range(des[0]):
				#print("Process point:", j+1)
				point = des[2::]
				Nwaypoints.append(point)
				#print(point)
				des = set_upcal.destination(point)
			
		Nwaypoints.append(waypoints[len(waypoints)-1])
		#print(theta)
		#print(set_upcal.d)
		return (Nwaypoints, theta)
	
	def file_thread(self):
		waypoints = []
		for i in kml.kml_to_csv():
			waypoints.append(i)
		#waypoints = mp.read_mp()
		return waypoints
			
compass_data_queue = Queue()
gps_data_queue = Queue()

def read_gps():
	gps = []
	latitude = 0
	lontitude = 0
	while True:
		sergps = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
		dataout = pynmea2.NMEAStreamReader()
		newdata = sergps.readline().decode("unicode_escape")

		if newdata[0:6] == "$GPRMC":
			newmsg = pynmea2.parse(newdata)
			lat = newmsg.latitude
			lng = newmsg.longitude
			latitude = lat
			lontitude = lng
			gps = [latitude,lontitude]
			gps_data_queue.put(gps)
			time.sleep(0.02)
	
def read_compass():
	while True:
		x, y, z = bmm150.BMM150().read_mag_data()
		heading_rads = math.atan2(x, y)
		heading_degrees = math.degrees(heading_rads)
		heading_degrees = round(heading_degrees)
		compass_data_queue.put(heading_degrees)
		time.sleep(0.5)
	
def main():
	compass_process = Process(target = read_compass)
	compass_process.daemon = True
	compass_process.start()
	
	gps_process = Process(target = read_gps)
	gps_process.daemon = True
	gps_process.start()
	global compass
	global gps
	path_all=[]
	while True:
		if not compass_data_queue.empty() and not gps_data_queue.empty():
			compass = compass_data_queue.get()
			gps = gps_data_queue.get()
			#print("GPS", gps)
			print("compass", compass)
			# print(type(path_all))
			if gps != None and len(path_all) == 0:
				path_all = mainR().cal_thread(gps)
				print(path_all)
			if gps != None  and path_all != None:
				mainR().robot_move(gps, path_all, compass)
			
	
if __name__ == "__main__"	:
	main()
	# path_all = []
	# #device = bmm150.BMM150()
	# heading_degrees = 0
	# while True:	
		# gps = read_gps()
		# compass = read_compass()	
		# print(gps)
		# print(compass)
		
		# if gps != None and path_all != None:
			# path_all = mainR().cal_thread(gps)
			# #print(path_all)
			
		# if (gps != None and gps[1] != 0) and path_all != None:
			# mainR().robot_move(gps, path_all, compass)
			
	
	# for posgps in main_f.run_gps():
		# if posgps[0] != 0 and posgps[1] != 0 :
			
			# main_f.gps_threading(posgps)
			# main_f.pud_thread()
			# x, y, z = device.read_mag_data()

			# heading_rads = math.atan2(x, y)
			# heading_degrees = math.degrees(heading_rads)
			# heading_degrees = (heading_degrees + 360) % 360
			# # heading_degrees = round(heading_degrees)
			
			# if len(path_all) == 0:
				# path_all = main_f.cal_thread(posgps)
				# #print(path_all)
				
			# if len(path_all) > 0 :
				# main_f.robot_move(posgps, path_all, heading_degrees)
			# #print(posgps)
	# print("Out for loop")
	#kml_file = "waypoint.kml"
	# posRobot = gps.GPSModule().read_gps_data()
	# running = True
	#main_f.cal_thread()
	# waypointpath = None
	#p1 = multiprocessing.Process(target=main_f.robot_move(), args=(0.7, 0.84,waypointpath))
	#p1.start()
	#p1.join()
	# while waypointpath == None:
		# posRobot
		# main_f = main(hostname,username,password,["Robot/GPS","Robt/Travel"], posRobot)
		# waypointpath = main_f.cal_thread()
		# print(main_f.cal_thread())
	# while running:
		#posRobot = posGPS.read_gps_data()
		# main_f = main(hostname,username,password,["Robot/GPS","Robt/Travel"], posRobot)
		# main_f.gps_threading()
		# main_f.pud_thread()
		#main_f.kml_thread()
		#main_f.cal_thread()
		#print(main_f.pos)
# 		if waypointpath is None:
# 			waypointpath = main_f.cal_thread()
		
		#if len(waypointpath) == 0:
		#	waypointpath = main_f.cal_thread()
		
		# if len(waypointpath) > 0 :
			# main_f.robot_move(0.5, 0.08,waypointpath)
			
		#print(len(waypointpath))
		#print(main_f.cal_thread())
			
	
	#print(main_f.cal_thread()[1])
	#t1 = threading.Thread(target=gps_threading, args=([13.720302, 100.570397],))
	#t1 = threading.Thread(target=main_f.pud_thread)
	#t1 = gps_main.pud_thread(hostname,username,password,["Robot/GPS","Robt/Travel"])
	#t2 = threading.Thread(target=main_f.robot_move)

	#t1.start()
	#t2.start()

	#t1.join()
	#t2.join()
	#for i in gps_threading([13.720302, 100.570397]):
	#	print(i)
		
