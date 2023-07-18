import time
import math
import threading
import json

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
		self.travel = {}
		self.waypoint1 = gps.GPSModule().read_gps_data()
		self.BMM150 = 90
			
	def pud_thread(self):
		for i in self.gps_threading():
			i = json.JSONEncoder().encode(i)
			#j = json.JSONEncoder().encode(j)
			mqtt.MQTT_R(self.hostname,self.username,self.password).publish_single(self.topic[0],i)
			#mqtt.MQTT_R(self.hostname,self.username,self.password).publish_single(topic[1],j)
			print(i)
			
	def robot_move(self):
        all_path =self.cal_thread().copy()
        robot = mr.Robot(0.7, 0.084, self.waypoint1, all_path[0], all_path[1], self.BMM150)
        while True:
            if len(all_path) > 0:
                robot.follow_path()
                robot.move()
                
                if wna.Waypoint(self.waypoint1, all_path[0][0]) < 0.0001:
                    all_path[0].pop(0)
                    all_path[1].pop(0)
	
	def cal_thread(self):
		self.waypoint1
		while self.waypoint1[0] == 0:
			self.waypoint1 = gps.GPSModule().read_gps_data()
			
		waypoints = self.kml_thread().copy()
		waypoints.insert(0,self.waypoint1)
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
			theta.append(int(set_upcal.bearing()))
			
			for j in range(des[0]):
				#print("Process point:", j+1)
				point = des[2::]
				Nwaypoints.append(point)
				#print(point)
				des = set_upcal.destination(point)
		
		Nwaypoints.append(len(waypoints)-1)
		print(Nwaypoints)
			
		
		
		return (Nwaypoints, theta)
	
	def kml_thread(self):
		waypoints = []
		for i in kml.kml_to_csv(self.file_kml):
			waypoints.append(i)
		return waypoints
	
	def gps_threading(self):
		while True:
			self.waypoint1 = gps.GPSModule().read_gps_data()
				
			if (self.waypoint1[0] != 0) and (self.waypoint1[1] != 0):
				self.pos["name"] = "robotgps"
				self.pos["lat"] = self.waypoint1[0]
				self.pos["lon"] = self.waypoint1[1]
				#selftravel["dis"] = dis
				#self.travel["ber"] = round(ber)
				yield self.pos
	
	

if __name__ == "__main__"	:	
	hostname = "localhost"
	username = "robotgps"
	password = "RIPzero27413."	
	#kml_file = "waypoint.kml"
	main_f = main(hostname,username,password,["Robot/GPS","Robt/Travel"])
	print(main_f.cal_thread())
	#t1 = threading.Thread(target=gps_threading, args=([13.720302, 100.570397],))
	t1 = threading.Thread(target=main_f.pud_thread)
	#t1 = gps_main.pud_thread(hostname,username,password,["Robot/GPS","Robt/Travel"])
	#t2 = threading.Thread(target=main_f.cal_thread)

	t1.start()
	#t2.start()

	t1.join()
	#t2.join()
	#for i in gps_threading([13.720302, 100.570397]):
	#	print(i)
		
