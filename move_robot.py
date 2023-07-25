import  math

class Robot:
    
    def __init__(self, L, pos_robot, path, theta_desired, theta_actual):
        self.L = L
        self.r = L/2
        self.pos = pos_robot
        self.path = path[0]
        self.theta_d = theta_desired[0]
        self.theta_a = theta_actual
        self.theta_e = 0
        self.vr = 0
        self.vl = 0
        self.u = 0
        self.w = 0
    
    def move(self):
        self.vr = self.u + ((self.L / 2) * self.w)
        self.vl = self.u - ((self.L / 2) * self.w)
        
        return self.vr, self.vl
    
    def follow_path(self):
        self.theta_e = math.atan2(math.sin(self.theta_d - self.theta_a),math.cos(self.theta_d - self.theta_a))
        target_x, target_y = self.path
        delta_x = target_x - self.pos[0]
        delta_y = target_y - self.pos[1]
        self.u = delta_x * math.cos(self.theta_e) + delta_y * math.sin(self.theta_e)
        self.w = (-1 / self.r) * math.sin(self.theta_e) * delta_x + (1 / self.r) * math.cos(self.theta_e) * delta_y
        
        return self.u, self.w, self.theta_e, self.theta_d
