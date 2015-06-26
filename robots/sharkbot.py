from robot import Robot

class TheRobot(Robot):
    def initialize(self):
        self.direction = 1
        self.act_next = 0

    def respond(self):
        kind, angle, dist = self.sensors['PING']
        x, y = self.sensors['POS']
        if self.sensors['TICK'] > self.act_next:
            if (self.sensors['TICK'] / 150) % 2 == 0:
                self.direction = 1
            else:
                self.direction = -1
            self.torque(25)
            self.turret(40)
            self.force(20 * self.direction)
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
                    self.fire(dist)
                    self.log("Heat: %s" % self.sensors['HEAT'])
            else:
                self.act_next = 0


        self.ping()
