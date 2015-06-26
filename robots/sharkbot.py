from robot import Robot

class TheRobot(Robot):
    def initialize(self):
        self.force_direction = 1
        self.turret_direction = 1
        self.act_next = 0
        self.health = 100

    def respond(self):
        kind, angle, dist = self.sensors['PING']
        x, y = self.sensors['POS']
        health = self.sensors['HEALTH']
        self.log("Health: %s" % health)
        if self.sensors['TICK'] > self.act_next:
            if (self.sensors['TICK'] / 150) % 2 == 0:
                self.force_direction = 1
            else:
                self.force_direction = -1
            self.torque(25)
            self.turret(70 * self.turret_direction)
            self.force(20 * self.force_direction)
        else:
            self.turret(0)
            self.torque(0)
            self.force(0)

        if kind == 'r':
            self.log('Wait')
            tick = self.sensors['TICK']
            self.act_next = tick + 100
            self.log(self.turret_direction)
            if self.sensors['LOADING'] == 0 and self.sensors['HEAT'] < 80:
                if dist < 4:
                    self.fire()
                else:
                    self.fire(dist)
                self.log("Heat: %s" % self.sensors['HEAT'])
            elif self.sensors['HEAT'] > 80:
                self.turret_direction = -self.turret_direction
                self.act_next = 0
        if self.health < health:
            self.force(self.force_direction * 100)

        self.health = health
        self.ping()
