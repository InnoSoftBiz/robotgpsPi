import time
import gps
import math
import WaypointNavigationAlgorithm as wna
import mqtt
import threading
from multiprocessing import Process
import json
import File_kml as kml

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
			
	def pud_thread(self):
		for i in self.gps_threading():
			i = json.JSONEncoder().encode(i)
			#j = json.JSONEncoder().encode(j)
			mqtt.MQTT_R(self.hostname,self.username,self.password).publish_single(self.topic[0],i)
			#mqtt.MQTT_R(self.hostname,self.username,self.password).publish_single(topic[1],j)
			print(i)

	def kml_thread(self):
		waypoints = []
		for i in kml.kml_to_csv(self.file_kml):
			waypoints.append(i[1:])
		return waypoints
	
	def cal_thread(self):
		self.waypoint1
		while self.waypoint1[0] == 0:
			self.waypoint1 = gps.GPSModule().read_gps_data()
			
		waypoints = self.kml_thread().copy()
		waypoints.insert(0,self.waypoint1)
		Nwaypoints = []
		for i in range(len(waypoints)-1):
			start = waypoints[i]
			goal = waypoints[i+1]
			set_upcal = wna.Waypoint(start,goal)
			haver = set_upcal.haversine()
			bear = set_upcal.bearing()
			des = set_upcal.destination(start)
			#print("All polt:", (haver, bear, des))
			Nwaypoints.append(start)
			
			for j in range(des[0]):
				#print("Process point:", j+1)
				point = des[2::]
				Nwaypoints.append(point)
				#print(point)
				des = set_upcal.destination(point)
		
		Nwaypoints.append(len(waypoints)-1)
		print(Nwaypoints)
			
		
		
		return Nwaypoints
	

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
		
