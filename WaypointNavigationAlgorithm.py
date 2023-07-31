import math

class Waypoint:

    def __init__(self,start,goal):
        self.start = start
        self.goal = goal
        self.num_sub = 0
        self.bearing_rad = 0
        self.lat1_rad = math.radians(self.start[0])
        self.lon1_rad = math.radians(self.start[1])
        self.lat2_rad = math.radians(self.goal[0])
        self.lon2_rad = math.radians(self.goal[1])
        self.d = 0
        self.R = 6371


    def haversine(self):
        # distance between latitudes
        # and longitudes
        dLat = self.lat2_rad - self.lat1_rad
        dLon = self.lon2_rad - self.lon1_rad

        # apply formulae
        h = (pow(math.sin(dLat / 2), 2) +
             pow(math.sin(dLon / 2), 2) *
             math.cos(self.lat1_rad) * math.cos(self.lat2_rad));
        c = 2 * math.asin(math.sqrt(h))
        self.d = self.R * c
        return self.d

    def bearing(self):

        # Calculate the difference in longitude
        delta_lon = self.lon2_rad - self.lon1_rad

        # Calculate the bearing using the atan2 function
        y = math.sin(delta_lon) * math.cos(self.lat2_rad)
        x = math.cos(self.lat1_rad) * math.sin(self.lat2_rad) - math.sin(self.lat1_rad) * math.cos(self.lat2_rad) * math.cos(delta_lon)
        self.bearing_rad = math.atan2(y, x)

        # Convert bearing from radians to degrees
        bearing_deg = math.degrees(self.bearing_rad)

        # Normalize the bearing to a range of 0 to 360 degrees
        bearing_deg = (bearing_deg + 360) % 360

        return (self.bearing_rad, bearing_deg)

    def destination(self,start):
        latr = math.radians(start[0])
        lonr = math.radians(start[1])
        num_sub = self.d // 0.005
        d = self.d / (num_sub-1)
        delta_lat = d / self.R
        lat_sub = latr + (delta_lat * math.cos(self.bearing()[0]))
        mlat_sub = math.degrees(lat_sub)
        psi = math.log(math.tan((math.pi / 4) + (lat_sub / 2)) / math.tan((math.pi / 4) + ( latr / 2)))
        q = (lat_sub - latr) / psi
        delta_lo = delta_lat * (math.sin(self.bearing()[0]) / q)
        lon_sub = lonr + delta_lo
        mlon_sub = math.degrees(lon_sub)

        return (int(num_sub)-1, d, mlat_sub, mlon_sub)
		
		
		
