from robot import Robot

class TheRobot(Robot):
    def initialize(self):
        # Will be called once, immediately after robot is created
        # Must finish in less than 1 second
        self.health = 100



    def respond(self):
        # Will be called 60 times per second
        # Must finish in less than 0.015 seconds
        #
        # sensors are available as the self.sensors dictionary
        #
        # use robot.Robot class methods to control
        
        self.torque(10)
        self.force(10)
        
        health = self.sensors['HEALTH']
        
        if health != self.health:
            self.torque(90)
            self.force(100)
        self.health = health
        
        self.turret(50)
        self.ping()

        self.fire()
        
        pass
