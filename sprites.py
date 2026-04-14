from images import *
from pygame import sprite, draw, Surface, SRCALPHA, Vector2, mask
from math import cos, sin, radians, atan2, sqrt, degrees

directions = {
    "clockwise": 1,
    "counter_clockwise": -1
}

class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()


        self.g_pull = (0, G_ACCELERATION)
        
        self.image = Surface((PLAYER_W, PLAYER_H), SRCALPHA) # , SRCALPHA
        self.mask = None
        self.nose = (0, -PLAYER_H // 2)
        self.right_wing = (PLAYER_W // 2, PLAYER_H // 2)
        self.thruster = (0, PLAYER_H // 4)
        self.left_wing = (-PLAYER_W // 2, PLAYER_H // 2)
        self.hyp = sqrt(pow(PLAYER_W // 2, 2) + pow(PLAYER_H, 2))
        
        self.width = PLAYER_W
        self.height = PLAYER_H
        self.define_shape()
        self.draw()

#        self.position = self.spawnpoint
        self.position = Vector2(self.spawnpoint[0], self.spawnpoint[1])
        self.velocity = Vector2(0, 0)
        self.direction = Vector2(0, -1)

        self.acceleration = 0.1
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.angle = -90

        self.falling = False

    def define_shape(self):
        self.dimensions = [(self.nose[0] * 2, self.nose[1] * 2),
                            (self.right_wing[0] * 2, self.right_wing[1] * 2),
                            (self.thruster[0] * 2, self.thruster[1] * 2),
                            (self.left_wing[0] * 2, self.left_wing[1] * 2)]
        self.width = min(max(abs(point[0]) for point in self.dimensions), self.hyp)
        self.height = min(max(abs(point[1]) for point in self.dimensions), self.hyp)
        self.shape = [(self.nose[0] + self.width // 2, self.nose[1] + self.height // 2),
                      (self.right_wing[0] + self.width // 2, self.right_wing[1] + self.height // 2),
                      (self.thruster[0] + self.width // 2, self.thruster[1] + self.height // 2),
                      (self.left_wing[0] + self.width // 2, self.left_wing[1] + self.height // 2)]
        
#        if self.nose[0] != 0:
        self.angle = round(degrees(atan2(self.nose[1], self.nose[0])), 0)
#        elif self.nose[1] < 0:
#            self.angle = 90
#        else:
#            self.angle = 270
        print(f"\n{self.angle = }")

    def draw(self):
#        self.shape = [(self.nose[0] + PLAYER_BOX_LEN // 2, self.nose[1] + PLAYER_BOX_LEN // 2),
#                      (self.right_wing[0] + PLAYER_BOX_LEN // 2, self.right_wing[1] + PLAYER_BOX_LEN // 2),
#                      (self.thruster[0] + PLAYER_BOX_LEN // 2, self.thruster[1] + PLAYER_BOX_LEN // 2),
#                      (self.left_wing[0] + PLAYER_BOX_LEN // 2, self.left_wing[1] + PLAYER_BOX_LEN // 2)]

        draw.polygon(self.image, self.color, self.shape)
        draw.polygon(self.image, (0, 0, 0, 128), [(self.width // 2, self.height // 2 - 4),
                                                    (self.width // 2, self.height // 2 + 4),
                                                    (self.width // 2, self.height // 2),
                                                    (self.width // 2 - 4, self.height // 2),
                                                    (self.width // 2 + 4, self.height // 2),
                                                    (self.width // 2, self.height // 2)])
        
    def get_direction(self):
        direction = Vector2(0, -1)
        return direction.rotate(-self.angle)

    def update(self):

        self.rect.center = self.position
        self.draw()
        self.mask = mask.from_surface(self.image)

#        if self.rect.bottom < window_h - 50:
#            self.fall()
#        else:
#            self.rect.bottom = window_h - 50
#            self.falling = False


    def fire(self):
        pass

    def thrust(self):
        self.direction = self.get_direction()
        self.velocity += self.direction * self.acceleration
        self.position += self.velocity

    def rotate(self, direction: str):
#        self.position = (self.position[0] * cos(100) - self.position[1] * sin(100),
#                        self.position[0] * sin(100) + self.position[1] * cos(100))
        degrees = directions[direction] * ROT_PER_FRAME
#        rads = radians(degrees)
#        self.nose = (self.nose[0] * cos(rads) - self.nose[1] * sin(rads),
#                     self.nose[0] * sin(rads) + self.nose[1] * cos(rads))
#        self.right_wing = (self.right_wing[0] * cos(rads) - self.right_wing[1] * sin(rads),
#                            self.right_wing[0] * sin(rads) + self.right_wing[1] * cos(rads))
#        self.thruster = (self.thruster[0] * cos(rads) - self.thruster[1] * sin(rads),
#                        self.thruster[0] * sin(rads) + self.thruster[1] * cos(rads))
#        self.left_wing = (self.left_wing[0] * cos(rads) - self.left_wing[1] * sin(rads),
#                        self.left_wing[0] * sin(rads) + self.left_wing[1] * cos(rads))
#        self.define_shape()
#        self.image = transform.scale(self.image, (self.width, self.height))
##        self.image.fill((0, 0, 0, 0))
#        self.image.fill((200, 200, 200, 20))

        #self.angle = 
        self.image = transform.rotozoom(self.image, self.angle, 0.25)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.draw()

    def fall(self):
        self.falling = True
        self.position = (self.position[0], self.position[1] + self.g_pull)

    def __str__(self):
        return f"{'Player 1' if type(self) is PlayerOne else 'Player 2'}"

class PlayerOne(Player):
    def __init__(self, screen):
        self.screen = screen
        self.spawnpoint = (window_w - window_w // 1.618, window_h // 1.618)
        self.color = P1_COLOR
        self.controls = p1_controls
        super().__init__()

class PlayerTwo(Player):
    def __init__(self, screen):
        self.screen = screen
        self.spawnpoint = (window_w // 1.618, window_h // 1.618)
        self.color = P2_COLOR
        self.controls = p2_controls
        super().__init__()

class Bullet(sprite.Sprite):
    def __init__(self):
        super().__init__()