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
	
	def __init__(self,hostname,username,password,topic,posrobot):
		self.hostname = hostname
		self.username = username
		self.password = password
		self.topic = topic
		self.file_kml = "waypoint.kml"
		self.pos = {}
		self.posrobot = posrobot
		self.travel = {}
		self.BMM150 = 90
		#self.posrobot = [0,0]
			
	def pud_thread(self):
		i = json.JSONEncoder().encode(self.pos)
			#j = json.JSONEncoder().encode(j)
		mqtt.MQTT_R(self.hostname,self.username,self.password).publish_single(self.topic[0],i)
			#mqtt.MQTT_R(self.hostname,self.username,self.password).publish_single(topic[1],j)
			#print(i)
			
	def robot_move(self, L, r,path):
		# self.waypoint1 = gps.GPSModule().read_gps_data()
		robot = mr.Robot(L, r, self.posrobot, path[0], path[1], self.BMM150)
		if len(all_path) > 0:
			robot.follow_path()
			robot.move()
			print(robot.move(), robot.follow_path())
			if wna.Waypoint(self.pos, all_path[0][0]).haversine() < 0.0001:
				path[0].pop(0)
				path[1].pop(0)
		print(self.pos)
	
	def cal_thread(self):
		if self.posrobot[0] != 0 and self.posrobot[1] != 0:
			waypoints = self.kml_thread().copy()
			waypoints.insert(0,self.posrobot)
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
	
	def gps_threading(self):
				
		if (self.posrobot[0] != 0) and (self.posrobot[1] != 0):
			self.pos["name"] = "robotgps"
			self.pos["lat"] = self.posrobot[0]
			self.pos["lon"] = self.posrobot[1]
			#selftravel["dis"] = dis
			#self.travel["ber"] = round(ber)
			return self.pos
	
	

if __name__ == "__main__"	:
	hostname = "localhost"
	username = "robotgps"
	password = "RIPzero27413."	
	#kml_file = "waypoint.kml"
	posGPS = gps.GPSModule()
	running = True
	#main_f.cal_thread()
	waypointpath = []
	#p1 = multiprocessing.Process(target=main_f.robot_move(), args=(0.7, 0.84,waypointpath))
	#p1.start()
	#p1.join()
	while running:
		posRobot = posGPS.read_gps_data()
		main_f = main(hostname,username,password,["Robot/GPS","Robt/Travel"], posRobot)
		main_f.gps_threading()
		main_f.pud_thread()
		#print(main_f.pos)
		if waypointpath is None:
			waypointpath = main_f.cal_thread()
		
		#if len(waypointpath) == 0:
		#	waypointpath = main_f.cal_thread()
		
		if len(waypointpath) > 0 :
			main_f.robot_move(0.5, 0.08,waypointpath)
			
		print(len(waypointpath))
			
	
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
		
