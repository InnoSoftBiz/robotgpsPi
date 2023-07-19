import time
import math
import threading
import json
import multiprocessing

import gps
import WaypointNavigationAlgorithm as wna
import mqtt
from multiprocessing import Process
import File_kml as kml
import move_robot as mr

class main:
	
	def __init__(self,hostname,username,password,topic):
		self.hostname = hostname
		self.username = username
		self.password = password
		self.topic = topic
		self.file_kml = "waypoint.kml"
		self.pos = {}
		self.posrobot = []
		self.travel = {}
		self.BMM150 = 90
		#self.posrobot = [0,0]
		
	def run_gps(self):
		while True:
			posRobot = gps.GPSModule().read_gps_data()
			self.posRobot = posRobot
			if len(self.posRobot) > 2:
				self.posRobot.pop(0)
			yield self.posRobot
			
	def pud_thread(self):
		i = json.JSONEncoder().encode(self.pos)
			#j = json.JSONEncoder().encode(j)
		mqtt.MQTT_R(self.hostname,self.username,self.password).publish_single(self.topic[0],i)
			#mqtt.MQTT_R(self.hostname,self.username,self.password).publish_single(topic[1],j)
			#print(i)
			
	def robot_move(self, L, r, posrobot, path):
		mainpath = self.kml_thread().copy()
		# self.waypoint1 = gps.GPSModule().read_gps_data()
		robot = mr.Robot(L, r, posrobot, path[0], path[1], self.BMM150)
		if len(path) > 0:
			robot.follow_path()
			robot.move()
			print(f"Vl : {robot.vl * 50} Vr : {robot.vr * 50}")
			if wna.Waypoint(posrobot, path[0][0]).haversine() < 0.0001:
				path[0].pop(0)
				if path[0][0] == mainpath[0]:
					path[1].pop(0)
					mainpath.pop(0)
		#print(self.pos)
	
	def cal_thread(self,posrobot):
		waypoints = self.kml_thread().copy()
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
			theta.append(int(set_upcal.bearing()[1]))
				
			for j in range(des[0]):
				#print("Process point:", j+1)
				point = des[2::]
				Nwaypoints.append(point)
				#print(point)
				des = set_upcal.destination(point)
			
		Nwaypoints.append(waypoints[len(waypoints)-1])
		#print(Nwaypoints)
		return (Nwaypoints, theta)
	
	def kml_thread(self):
		waypoints = []
		for i in kml.kml_to_csv(self.file_kml):
			waypoints.append(i)
		return waypoints
	
	def gps_threading(self,posrobot):
				
		if (posrobot[0] != 0) and (posrobot[1] != 0):
			self.pos["name"] = "robotgps"
			self.pos["lat"] = posrobot[0]
			self.pos["lon"] = posrobot[1]
			#selftravel["dis"] = dis
			#self.travel["ber"] = round(ber)
			return self.pos
	
	

if __name__ == "__main__"	:
	hostname = "localhost"
	username = "robotgps"
	password = "RIPzero27413."	
	main_f = main(hostname,username,password,["Robot/GPS","Robt/Travel"])
	path_all = []
	
	for posgps in main_f.run_gps():
		if posgps[0] != 0 and posgps[1] != 0 :
			
			main_f.gps_threading(posgps)
			main_f.pud_thread()
			
			if len(path_all) == 0:
				path_all = main_f.cal_thread(posgps)
				print(path_all)
				
			if len(path_all) > 0 :
				main_f.robot_move(0.324, 8.4, posgps, path_all)
			print(posgps)
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
		
