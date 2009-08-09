class Fake(object):
    def __init__(self, a=None, b=None):
        pass

    def setpos(self, pos):
        pass

    def set_rotation(self, ang):
        pass

    def kill(self):
        pass

    def step(self, n=None):
        pass


class Robot(Fake):
    pass


class Turret(Fake):
    pass

class RobotInfo(Fake):
    def __init__(self, n, name):
        self.health = Fake()


class Bullet(Fake):
    pass

class Explosion(Fake):
    pass

class Wall(Fake):
    pass


class Sprites(Fake):
    def add(self, sprite, level=None):
        pass

class Arena(Fake):
    def __init__(self):
        self.sprites = Sprites()
        self.quit = False

    def step(self):
        pass
