from robot import Robot

class TheRobot(Robot):
    def initialize(self):
        self.force_direction = 1
        self.turret_direction = 1
        self.act_next = 0
        self.health = 100
        self.rest_force = 0

    def respond(self):
        kind, angle, dist = self.sensors['PING']
        x, y = self.sensors['POS']
        health = self.sensors['HEALTH']
        tick = self.sensors['TICK']
        #self.log("Health: %s" % health)
        if self.sensors['TICK'] > self.act_next:
            if (self.sensors['TICK'] / 150) % 2 == 0:
                self.force_direction = 1
            else:
                self.force_direction = -1
            self.torque(25)
            self.turret(100 * self.turret_direction)
            self.force(30 * self.force_direction)
            self.rest_force = 0
        else:
            self.turret(0)
            self.torque(0)
            self.force(self.rest_force * self.force_direction)

        if kind == 'r':
            self.log('Wait')
            self.act_next = tick + 100
            self.log(self.turret_direction)
            if self.sensors['LOADING'] == 0 and self.sensors['HEAT'] < 80:
                if dist < 4:
                    self.fire()
                else:
                    self.fire(dist)
                self.log("Heat: %s" % self.sensors['HEAT'])
            elif self.sensors['HEAT'] > 80:
                self.log("Turret direction: %s" % self.turret_direction)
                self.turret_direction = -self.turret_direction
                self.act_next = 0
        if self.health > health:
            self.log("Health decreased")
            self.act_next = tick + 30
            self.rest_force = 100

        self.health = health
        self.ping()
