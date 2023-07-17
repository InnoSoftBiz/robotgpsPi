import networkx as nx
import plotly.graph_objects as go
import osmnx as ox
import pandas as pd
import geopandas
import numpy as np

##### Interface to OSMNX  
def generate_path(origin_point, target_point, perimeter):
	# Using the cache accelerates processing for a large map
	ox.config(log_console=True, use_cache=True)
	# Splice the geographical coordinates in long and lat
	origin_lat = origin_point[0]
	origin_long = origin_point[1]
	
	target_lat = target_point[0]
	target_long = target_point[1]
	
	# Build the geocoordinate structure of the path's graph
	
    # If the origin is further from the equator than the target
	if origin_lat > target_lat:
		north = origin_lat
		south = target_lat
		
	else:
		north = target_lat
		south = origin_lat
		
	# If the origin is further from the prime meridian than the target
	if origin_long > target_long:
		east = origin_long
		west = target_long
	else:
		east = target_long
		west = origin_long
	
	# Construct the road graph
    # Modes 'drive', 'bike', 'walk' (walk is usually too slow)
	mode = "drive"
    # Create the path/road network graph via setting the perimeters
	roadgraph = ox.graph_from_bbox(north+perimeter,south-perimeter,
				east+perimeter, west-perimeter,network_type=mode,simplify=False)
	# Alternatively a road network can be determined via providing a place
	place = 'Munich, Bavaria', 'Germany'
	roadgraph = ox.graph_from_bbox(place,network_type='drive', simplify=False)
	'''
    # Alternatively a road network can be determined via providing a place
    place  = 'Munich, Bavaria, Germany'
    roadgraph = ox.graph_from_bbox(place, network_type = 'drive', simplify=False )
    '''
    # Get the nearest node in the OSMNX graph for the origin point
	origin_node = ox.get_nearest_node(roadgraph,origin_point)
    # Get the nearest node in the OSMNX graph for the target point
	target_node = ox.get_neatrest_node(roadgraph,target_point)
    # Get the optimal path via dijkstra
	route = nx.shortest_path(roadgraph,origin_node, target_node, weight = 'length', method='dijkstra')
    # Create the arrays for storing the paths
	lat = []
	lon = []
    
	for i in route:
		point = roadgraph.nodes[i]
		lon.append(point['x'])
		lat.append(point['y'])
	# Return the paths
	return lon,lat
	
def plot_map(origin_point, target_points, lons, lat, lat_center, lon_center):
	# Create a plotly map and add the origin point to the map
	print('Setting up figure...')
	fig = go.Figure(go.Scattermapbox(
	name = "Origin",
	mode = "markers",
	lon = [origin_point[1]],
	lat = [origin_point[0]],
	marker = {'size': 16, 'color': "#333333"},
	)
)
	# Plot the optimal paths to the map
	print("Generating paths...")
	for i in range(len(lat)):
		fig.add_trace(go.Scattermapbox(
			name = "Paih",
			mode = "lines",
			lon =  lons[i],
			lat = lat[i],
			marker = {'size':10},
			showlegend=False,
			line = dict(width = 4.5, color="#ffd700"))
			)
			
	# Plot the target geocoordinates to the map
	print("Generating target...")
	for target_point in target_points:
		fig.add_trace(go.Scattermapbox(
			name = "Destination",
			mode = "markers",
			showlegend=False,
			lon = [target_point[1]],
			lat = [target_point[0]],
			marker = {'size': 16, 'color': '#ffd700'}))
	# Style the map layout
	fig.update_layput(
		mapbox_style = "linght",
		mapbox_accesstoken = "############",
		legend = dict(yanchor="top", y=1, xanchor="left", x=0.83),
		title="<span style='font-size: 32px;'><b>The Shortest Paths Dijkstra Map</b></span>",
		font_size = 18,
		width = 1000,
		height = 1000,
		)
		
	# Set the center of the map
	lat_center = lat_center 
	lon_center = lon_center 
	
	# Add the center to the map layout
	fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
						title=dict(yanchor="top", y=.97, xanchor="left", x=0.03),
						mapbox = {
						"center": {'lat':lat_center,
									'lon':lon_center},
									'zoom': 12.2}
	)
	

if __name__ == '__main__':
	lat_center = 13.87013
	lon_center = 100.54475
	lat_lon = [[13.86999261435705, 100.5500108206279], [13.87006200437641, 100.5501733820456], [13.86993362751711, 100.5502764295459], [13.86988636466538, 100.5501029992414]]
	lat_lon = np.array(lat_lon)
	numwaypoint = len(lat_lon)
	print(lat_lon[0:numwaypoint,0])

	
