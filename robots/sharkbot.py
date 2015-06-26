from robot import Robot

class TheRobot(Robot):
    def initialize(self):
        self.act_next = 0

    def respond(self):
        kind, angle, dist = self.sensors['PING']
        if self.sensors['TICK'] > self.act_next:
            self.log('Go')
            self.torque(10)
            self.turret(40)
            self.force(20)
        else:
            self.turret(0)
            self.torque(0)
            self.force(0)

        if kind == 'r':
            self.log('Wait')
            tick = self.sensors['TICK']
            self.act_next = tick + 100
            if self.sensors['HEAT'] < 100:
                if self.sensors['LOADING'] == 0 and  self.sensors['HEAT'] < 80:
                    self.fire(dist - 0.1)
                    self.log("Heat: %s" % self.sensors['HEAT'])

        self.ping()
