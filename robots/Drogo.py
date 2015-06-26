from robot import Robot

class TheRobot(Robot):
    def initialize(self):
        # Will be called once, immediately after robot is created
        # Must finish in less than 1 second
        self.health = 100
        self.speed = 100



    def respond(self):
        # Will be called 60 times per second
        # Must finish in less than 0.015 seconds
        #
        # sensors are available as the self.sensors dictionary
        #
        # use robot.Robot class methods to control
        
        x, y = self.sensors['POS']
        
        health = self.sensors['HEALTH']
        
        if health != self.health:
            self.torque(90)
            self.speed = 100
            self.force(self.speed)
        self.health = health
        
        if self.speed > 0:
            self.speed -= 2
            self.force(self.speed)
        
        self.turret(50)
        self.ping()

        kind, angle, dist = self.sensors['PING']
        if kind in 'r':
            self.fire(dist)
