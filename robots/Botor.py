from robot import Robot

class TheRobot(Robot):
    
    def initialize(self):
        # Will be called once, immediately after robot is created
        # Must finish in less than 1 second
        self.previousKind = None
        self.movingTimer = 0
        self.torqueRot = 100
        pass


    def shoot(self, loading):
        if loading == 0:
            self.fire()
        
    def move(self, force, time):
        self.force(force)
        self.movingTimer = time

    def respond(self):
        if self.movingTimer is not 0:
            self.movingTimer -= 1
        else:
            self.force(0)

        tick = self.sensors['TICK']
        health = self.sensors['HEALTH']
        x, y = self.sensors['POS']
        turret_angle = self.sensors['TUR']
        kind, angle, distance = self.sensors['PING']
        robot_angle = self.sensors['GYRO']
        heat = self.sensors['HEAT']
        loading = self.sensors['LOADING']

        self.torque(0)        

        if kind == 'r':
            self.turret(0)
            self.torque(0)
#            self.movingTimer = 2
            if loading == 0:
                self.fire(distance+1)
            
        elif kind == 'w':
            if self.previousKind == 'r' or self.previousKind == 'b':
                self.turret(100)
            else:
                self.turret(-100)

        elif kind == 'b':
             if self.previousKind == 'r' or self.previousKind == 'b':
                 self.turret(100)
             else:
                 self.turret(-100)
             if self.previousKind == 'b':
                 self.move(100,2)
        
        
        self.previousKind = kind
        self.ping()
        ## if tick < 120:
        ##    self.force(100)
        ##else:
        ##    self.force(0)
        # Will be called 60 times per second
        # Must finish in less than 0.015 seconds
        #
        # sensors are available as the self.sensors dictionary
        #
        # use robot.Robot class methods to control
        pass
