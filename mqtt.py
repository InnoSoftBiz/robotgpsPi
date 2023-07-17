import paho.mqtt.publish as pub
import paho.mqtt.subscribe as sub
import time
import threading

class MQTT_R():
	def __init__(self,hostname,username,password):
		self.hostname = hostname
		self.auth = {'username': username,'password': password}
		#self.protocol = mqtt.MQTTv311
		

	def publish_single(self, topic, payload):
				
		return pub.single(topic, payload, hostname = self.hostname, auth = self.auth)
		
	def subscribe_S(self,topic):
		
		msgs = sub.simple(topic,hostname=self.hostname,auth=self.auth)
		print("%s %s" % (msgs.topic, msgs.payload))
		
def public_thread(hostname,username,password,topic1,payload1):
	mqtt_gps = MQTT_R(hostname,username,password)
	while True:
		mqtt_gps.publish_single(topic1,payload1)
		time.sleep(0.5)
	
def subscribe_thread(hostname,username,password,topic):
	mqtt_gps = MQTT_R(hostname,username,password)
	while True:
		mqtt_gps.subscribe_S(topic)
		#time.sleep(1)

# Usage in the main program
if __name__ == '__main__':
	#mqtt_gps = MQTT_R("192.168.43.214","robotgps","RIPzero27413.")
	#while True:
	#	mqtt_gps.publish_single("GPS/lat",2313)
	#	mqtt_gps.publish_single("GPS/lon",2000)
	#	time.sleep(1)
	#	mqtt_gps.subscribe_S("GPS/lat")
	#	time.sleep(1)
	t1 = threading.Thread(target=public_thread, args=("192.168.43.214","robotgps","RIPzero27413.","GPS/lat",2313,))
	t2 = threading.Thread(target=public_thread, args=("192.168.43.214","robotgps","RIPzero27413.","GPS/lon",2000,))
	t3 = threading.Thread(target=subscribe_thread, args=("192.168.43.214","robotgps","RIPzero27413.","GPS/lat"))
	
	t1.start()
	t2.start()
	t3.start()
