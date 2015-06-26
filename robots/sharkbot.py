from robot import Robot

class TheRobot(Robot):
    def initialize(self):
        self.act_next = 0

    def respond(self):
        kind, angle, dist = self.sensors['PING']
        if self.sensors['TICK'] > self.act_next:
            self.log('Go')
            self.torque(50)
            self.turret(40)
            self.force(40)
        else:
            self.turret(0)
            self.torque(0)
            self.force(0)

        if kind == 'r':
            self.log('Wait')
            tick = self.sensors['TICK']
            self.act_next = tick + 100
            self.fire()

        self.log(kind)
        self.ping()