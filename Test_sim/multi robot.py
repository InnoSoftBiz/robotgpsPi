import pygame
import math
import numpy as np
import File_kml as kml
import WaypointNavigationAlgorithm as wna

class Robot:
    def __init__(self, startpos, robotimg, width, follow = None):
        self.m2p = 3779.52 # from meter to pixls
        
        self.leader = False
        self.follow = follow
        
        self.x, self.y = startpos
        self.theta = 0
        self.w = width
        self.u = 30 # pix/sec
        self.w = 0 # rad/sec
        self.a = 10
        self.sub_point = []
        
        self.img = pygame.image.load(robotimg) #skin img path provided in the arguments
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center = (self.x, self.y))
        
    
    def move(self,dt):
        self.x+=(self.u*math.cos(self.theta)-self.a*math.sin(self.theta)*self.w)*dt
        self.y+=(self.u*math.sin(self.theta)+self.a*math.cos(self.theta)*self.w)*dt
        self.theta+=self.w*dt
        
        self.rotated = pygame.transform.rotozoom(self.img,
                                                 math.degrees(-self.theta),1)
        self.rect = self.rotated.get_rect(center=(self.x, self.y))
    
    def following(self,point):
        target = point[0]
        delta_lat = target[0] - self.x
        delta_lon = target[1] - self.y
        self.u = delta_lat*math.cos(self.theta)+delta_lon*math.sin(self.theta)
        self.w = (-1/self.a)*math.sin(self.theta)*delta_lat + (1/self.a)*math.cos(self.theta)*delta_lon
    
    def dist(self, point1, point2):
        (x1, y1) = point1
        (x2, y2) = point2
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        #calculate
        px = (x1 - x2) ** (2)
        py = (y1 - y2) ** (2)
        distance = (px + py) ** (0.5)
        return distance
        
    def draw(self, map):
        map.blit(self.rotated, self.rect)
        
    
class Envir:
    
    def __init__(self, dimentions):
        
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)
        self.file = "/home/pi/robot_gsp_controll/waypoint.kml"
        #map dims
        self.height, self.width = dimentions
        #window settings
        pygame.display.set_caption("diff drive")
        self.map = pygame.display.set_mode((self.width, self.height))
        
    
    def write_info(self):
        pass
    
    def robot_frame(self):
        pass
    
    def trail(self,pos):
        #for i in range(0, len(pos)-1):
        pygame.draw.lines(self.map, self.yel, False,  pos, width=2)
        
    def read_kml(self):
        waypoint = []
        Nwaypoint = []
        for i in kml.kml_to_csv(self.file):
            waypoint.append(i[1:])
            
        #print(len(waypoint))
            
        for i in range(len(waypoint)-1):
            start = waypoint[i]
            goal = waypoint[i+1]
            #print((start, goal))
            cal = wna.Waypoint(start,goal)
            hev = cal.haversine()
            ber = cal.bearing()
            des = cal.destination(start)
            Nwaypoint.append(start)
            
            for j in range(des[0]):
                point = des[2::]
                Nwaypoint.append(point)
                des = cal.destination(point)
        Nwaypoint = np.array(Nwaypoint)
        min_lon = Nwaypoint[0:len(Nwaypoint),1].min()
        min_lat = Nwaypoint[0:len(Nwaypoint),0].min()
        max_lon = Nwaypoint[0:len(Nwaypoint),1].max()
        max_lat = Nwaypoint[0:len(Nwaypoint),0].max()
        
        pixel_lat_lon = []
        for lat,lon in Nwaypoint:
            x = int((lon - min_lon) * self.width / (max_lon - min_lon))
            y = int((lat - min_lat) * self.height / (max_lat - min_lat))
            pixel_lat_lon.append((x,y))
        
        return pixel_lat_lon
    
    
# initialization area

pygame.init()
runing = True
iterations = 0
dt=0
lasttime = pygame.time.get_ticks()
dims = (480, 640)

environment = Envir(dims)

kml_way = environment.read_kml()
#print(kml_way)
start = (200,200)
robot = Robot(start,r'/home/pi/robot_gsp_controll/Test_sim/robotcar.png', width=10, follow=None)
#environment.map.fill(environment.black)
#environment.trail()
#pygame.display.update()
clock = pygame.time.Clock()











#animation loop

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    
    pygame.display.update()
    environment.map.fill(environment.black)
    environment.trail(kml_way.copy())
    robot.draw(environment.map)
    if len(kml_way) > 0:
        #print(i)
        robot.following(kml_way)
        robot.move(dt)
        if math.dist((robot.x, robot.y), kml_way[0]) < 10:
            kml_way.pop(0)
    dt=(pygame.time.get_ticks() - lasttime)/1000
    clock.tick(60)
    #lasttime = pygame.time.get_ticks()
    iterations += 1
