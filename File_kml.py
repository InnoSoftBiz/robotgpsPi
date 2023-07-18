from pykml import parser

def kml_to_csv(kml_file_path):
	pack_waypoint = None
	with open(kml_file_path,'rb') as kml_file:
		root = parser.parse(kml_file).getroot()
		placemarks = root.Document.Placemark
		for placemark in placemarks:
			coordinates = placemark.Point.coordinates.text.strip().split(',')
			longitude, latitude = [float(coord.strip()) for coord in coordinates[:2]]
				
			pack_waypoint = [latitude,longitude]
			yield pack_waypoint

if __name__ == '__main__':				
	waypointall = []
	kml_file = "waypoint.kml"
	for i in kml_to_csv("/home/pi/robot_gsp_controll/waypoint.kml"):
		waypointall.append(i[1:])
		#print(kml_file)	
	print(waypointall)
