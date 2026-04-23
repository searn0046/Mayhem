from abc import ABC, abstractmethod
from typing import Any
from images import *
from pygame import sprite, draw, Surface, SRCALPHA, Vector2, mask, transform
from math import sqrt, pi

directions = {
    "clockwise": 1,
    "counter_clockwise": -1,
    "upwards": 0.5
}


class MovingObject(sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def update(self, time_delta: float | int):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def collide(self, offset: tuple[int, int], other_object):
        pass


class Player(MovingObject):
    def __init__(self, window, position: tuple[int | float, int | float], color, controls):
        super().__init__()

        self.window = window
        self.__position = Vector2(position)
        self.__color = color
        self.__controls = controls

        self.lives = PLAYER["LIVES"]
        self.__image = Surface((int(PLAYER["WIDTH"]), int(PLAYER["HEIGHT"])), SRCALPHA)
        self.__mask = mask.from_surface(self.image)
        self.nose = (0, -PLAYER["HEIGHT"] // 2)
        self.right_wing = (PLAYER["WIDTH"] // 2, PLAYER["HEIGHT"] // 2)
        self.thruster = (0, PLAYER["HEIGHT"] // 4)
        self.left_wing = (-PLAYER["WIDTH"] // 2, PLAYER["HEIGHT"] // 2)
        self.hyp = sqrt(pow(PLAYER["WIDTH"] // 2, 2) + pow(PLAYER["HEIGHT"], 2))

        self.__size = (PLAYER["WIDTH"], PLAYER["HEIGHT"])
        self.__direction = Vector2(0, -1)
        self.define_shape()
        self.draw()
        self.__original_image = self.image.copy()   # For rotation purposes.
        self.__velocity = Vector2(0, 0)
        self.__max_THRUST = PLAYER["MAX_THRUST"] / FRAMERATE
        self.__rotation_speed = PLAYER["ROTATION_SPEED"] / FRAMERATE
        self.__prev_position = Vector2(position)
        self.__prev_direction = Vector2(self.__direction)
        self.__prev_angle = 0
        self.__prev_velocity = Vector2(0, 0)

        self.thrusting = False
        self.thrust_timer = 0
        self.thrust_speed = 0
        self.thrust_acceleration = PLAYER["ACCELERATION"] / FRAMERATE
#        print(f"{self} acceleration: {self.thrust_acceleration}")
        self.landed = False

        self.__rect = self.image.get_rect(center=position)
        self.__angle = 0
        self.__fuel = 100
        self.falling = False
        self.fall_speed = 0
        self.fall_timer = 0

        print(f"{self}\f{self.falling = }")
#        print(f"\n\x1b[1m{self}\x1b[0m\n{(self.rect.width, self.rect.height) = }\n{self.mask.get_size() = }\n")

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def original_image(self):
        return self.__original_image

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @property
    def mask(self):
        return self.__mask

    @property
    def color(self):
        return self.__color

    @property
    def size(self):
        return self.__size

    @property
    def position(self):
        return self.__position

    @property
    def direction(self):
        return self.__direction

    @property
    def angle(self):
        return self.__angle

    @property
    def velocity(self):
        return self.__velocity
    
    @property
    def max_THRUST(self):
        return self.__max_THRUST
    
    @property
    def rotation_speed(self):
        return self.__rotation_speed

    @property
    def controls(self):
        return self.__controls

    @property
    def fuel(self):
        return self.__fuel

    def __set_rect_position(self, part: str="center"):
#        print(f"{self.rect.center = }\n{self.position = }", end="\f")
        attribute = getattr(self.rect, part)
        if type(attribute) is tuple and len(attribute) == 2:
            setattr(self.rect, part, self.position)
        elif type(attribute) in (int, float):
            setattr(self.rect, part, getattr(self.position, "x" if part in ("left", "centerx", "right") else "y"))
        self.__set_mask()
#        print(f"But now: {self.rect.center = }")

    def __set_mask(self):
        self.__mask = mask.from_surface(self.image)

    def __set_position(self, new_position: Vector2, rect_part: str = "center"):
        self.__position = Vector2(new_position)
        self.__set_rect_position(part=rect_part)

    def __change_position(self, delta: Vector2 | tuple[int | float, int | float]):
        self.__position += delta
#        print(f"{self} changing position by {delta}, new position: {self.position}")
        self.__set_rect_position()

    def __change_direction(self, angle):
        self.__direction = self.direction.rotate(-angle)

    def __change_angle(self, degrees: float | int):
        self.__angle = (self.angle + degrees) % 360

    def __set_velocity(self, velocity: Vector2 | tuple[int | float, int | float]):
#        self.__velocity = velocity + Vector2(0, 0.5) if self.falling else velocity
        self.__velocity = velocity

    def __save_state(self):
        self.__prev_position = Vector2(self.position)
        self.__prev_direction = Vector2(self.direction)
        self.__prev_angle = self.angle
        self.__prev_velocity = Vector2(self.velocity)

    def __restore_prev_state(self,
                             pos_change: Vector2 | tuple[int | float, int | float] = (0, 0),
                             dir_change: Vector2 | tuple[int | float, int | float] = (0, 0),
                             angle_change: float | int = 0,
                             vel_change: Vector2 | tuple[int | float, int | float] = (0, 0)):
        self.__position = Vector2(self.__prev_position[0] + pos_change[0], self.__prev_position[1] + pos_change[1])
        self.__direction = Vector2(self.__prev_direction)
        self.__angle = self.__prev_angle
        self.__velocity = Vector2(self.__prev_velocity)
        self.__rotate_image(self.angle)
        old_center = self.rect.center
        self.__set_rect()
        self.__rect.center = old_center
        self.__set_rect_position()

    def __rotate_image(self, degrees):
        self.__image = transform.rotate(self.original_image, degrees)

    def define_shape(self):
        self.dimensions = [
            (self.nose[0] * 2, self.nose[1] * 2),
            (self.right_wing[0] * 2, self.right_wing[1] * 2),
            (self.thruster[0] * 2, self.thruster[1] * 2),
            (self.left_wing[0] * 2, self.left_wing[1] * 2),
        ]
        self.width = min(max(abs(point[0]) for point in self.dimensions), self.hyp)
        self.height = min(max(abs(point[1]) for point in self.dimensions), self.hyp)
        self.shape = [
            (self.nose[0] + self.width // 2, self.nose[1] + self.height // 2),
            (self.right_wing[0] + self.width // 2, self.right_wing[1] + self.height // 2),
            (self.thruster[0] + self.width // 2, self.thruster[1] + self.height // 2),
            (self.left_wing[0] + self.width // 2, self.left_wing[1] + self.height // 2),
        ]

    def draw(self):
        ''' Resets the image and draws a polygon of the player shipe on it. '''
        self.__image.fill((0, 0, 0, 0))
        self.ship = draw.polygon(self.image, self.color, self.shape)
        #draw.rect()

#    def get_direction(self):
#        return Vector2(0, -1).rotate(-self.angle)

    def update(self, time_delta: float | int):
        ''' ADD INERTIA AND FRICTION AT SOME POINT '''

        if self.landed and not self.thrusting:
            self.stop_fall()
        else:
            self.start_fall()

        if self.thrusting:
#            self.start_fall()
#            self.__set_velocity(min(self.thrust_speed, PLAYER["MAX_THRUST"]) * self.direction)
            thrust_momentum = self.direction * min(self.thrust_speed, PLAYER["MAX_THRUST"])
        else:
            thrust_momentum = Vector2(0, 0)
        momentum = thrust_momentum + (self.fall(time_delta) if self.falling else Vector2(0, 0))
#        move = self.velocity + (self.fall(time_delta) if self.falling else Vector2(0, 0))
        self.__set_velocity(momentum)
        if momentum.length_squared() > 0:
            self.__save_state()
        self.__change_position(momentum)

    def land(self):
        self.landed = True
        self.stop_fall()
        self.__set_velocity(Vector2(0, 0))

    def collide(self, offset: tuple[int | float, int | float] | None, other_object):
        if not offset or self is other_object:
            return
        
        
#        relative_vel = self.velocity + (other_object.velocity if hasattr(other_object, "velocity") else Vector2(0, 0))
#        print(f"{self.velocity = }\n{other_object.velocity = }\f{self.velocity} + {other_object.velocity} = {self.velocity + other_object.velocity}")

        relative_vel = self.velocity - (other_object.velocity if hasattr(other_object, "velocity") else Vector2(0, 0))

        angle = self.angle
        if angle >= 315:
            pass
        elif angle >= 270:
            pass
        elif angle >= 225:
            pass
        elif angle >= 180:
            pass
        elif angle >= 135:
            pass
        elif angle >= 90:
            pass
        elif angle >= 45:
            pass
        else:
            pass

        x_center = self.rect.width / 2
        y_center = self.rect.height / 2
        dist_from_x_center = x_center - offset[0]
        dist_from_y_center = y_center - offset[1]

        if offset[1] >= self.rect.height * 0.9:
            if self.angle > 355 or self.angle < 5:
                if abs(self.velocity[0]) * abs(self.velocity[1]) < 10000:
#                    print(f"{abs(self.velocity[0])} * {abs(self.velocity[1])}")
                    self.land()
                    return
                else:
                    self.landed = False
            else:
                self.landed = False
        else:
            self.landed = False

        if relative_vel[0] < 0:                                 # Left
            horiz_bump = PLAYER["COLLISION_BUMP"]
            if relative_vel[1] < 0:                                 # Top
                vert_bump = PLAYER["COLLISION_BUMP"]
                if abs(dist_from_x_center) > abs(dist_from_y_center):   # Vertical impact
                    if dist_from_x_center > 0:                              # Left of center
                        rotation_direction = "counter_clockwise"
                        x_vel = -relative_vel[0]
                        y_vel = relative_vel[1]
                    else:                                                   # Right of center
                        rotation_direction = "clockwise"
                        x_vel = relative_vel[0]
                        y_vel = relative_vel[1]
                else:                                                   # Horizontal impact
                    if dist_from_y_center > 0:                              # Above center
                        rotation_direction = "clockwise"
                        x_vel = relative_vel[0]
                        y_vel = -relative_vel[1]
                    else:                                                   # Below center
                        rotation_direction = "counter_clockwise"
                        x_vel = relative_vel[0]
                        y_vel = relative_vel[1]
            else:                                                   # Bottom
                vert_bump = -PLAYER["COLLISION_BUMP"]
                if abs(dist_from_x_center) > abs(dist_from_y_center):   # Vertical impact
                    if dist_from_x_center > 0:                              # Left of center
                        rotation_direction = "clockwise"
                        x_vel = -relative_vel[0]
                        y_vel = relative_vel[1]
                    else:                                                   # Right of center
                        rotation_direction = "counter_clockwise"
                        x_vel = relative_vel[0]
                        y_vel = relative_vel[1]
                else:                                                   # Horizontal impact
                    if dist_from_y_center > 0:                              # Above center
                        rotation_direction = "counter_clockwise"
                        x_vel = relative_vel[0]
                        y_vel = -relative_vel[1]
                    else:                                                   # Below center
                        rotation_direction = "clockwise"
                        x_vel = relative_vel[0]
                        y_vel = relative_vel[1]

        else:                                                   # Right
            horiz_bump = -PLAYER["COLLISION_BUMP"]
            if relative_vel[1] < 0:                                 # Top
                vert_bump = PLAYER["COLLISION_BUMP"]
                if abs(dist_from_x_center) > abs(dist_from_y_center):   # Vertical impact
                    if dist_from_x_center > 0:                              # Left of center
                        rotation_direction = "clockwise"
                        x_vel = -relative_vel[0]
                        y_vel = relative_vel[1]
                    else:                                                   # Right of center
                        rotation_direction = "counter_clockwise"
                        x_vel = relative_vel[0]
                        y_vel = relative_vel[1]
                else:                                                   # Horizontal impact
                    if dist_from_y_center > 0:                              # Above center
                        rotation_direction = "counter_clockwise"
                        x_vel = relative_vel[0]
                        y_vel = -relative_vel[1]
                    else:                                                   # Below center
                        rotation_direction = "clockwise"
                        x_vel = relative_vel[0]
                        y_vel = relative_vel[1]
            else:                                                   # Bottom
                vert_bump = -PLAYER["COLLISION_BUMP"]
                if abs(dist_from_x_center) > abs(dist_from_y_center):   # Vertical impact
                    if dist_from_x_center > 0:                              # Left of center
                        rotation_direction = "counter_clockwise"
                        x_vel = -relative_vel[0]
                        y_vel = relative_vel[1]
                    else:                                                   # Right of center
                        rotation_direction = "clockwise"
                        x_vel = relative_vel[0]
                        y_vel = relative_vel[1]
                else:                                                   # Horizontal impact
                    if dist_from_y_center > 0:                              # Above center
                        rotation_direction = "clockwise"
                        x_vel = relative_vel[0]
                        y_vel = -relative_vel[1]
                    else:                                                   # Below center
                        rotation_direction = "counter_clockwise"
                        x_vel = relative_vel[0]
                        y_vel = relative_vel[1]


#        print(f"{self}\f{relative_vel = }")
        self.__restore_prev_state(pos_change=(horiz_bump, vert_bump))
#        self.__restore_prev_state()
        self.rotate(rotation_direction, 5)
#        print(f"{self} rotated 5 degrees {rotation_direction}")
        self.thrust_timer = 0
        self.thrust_speed *= 0.8
        self.__set_velocity(Vector2(x_vel, y_vel))

    def fire(self):
        pass

    def start_thrust(self):
        self.thrusting = True
        self.falling = True

    def stop_thrust(self):
        self.thrusting = False
        self.thrust_timer = 0
        self.thrust_speed = 0

    def thrust(self, time_delta: float | int):
        self.thrust_timer += time_delta
#        print(f"{self.thrust_timer = }")
        self.thrust_speed += self.thrust_acceleration * self.thrust_timer
#        self.__change_position(self.direction * min(self.thrust_speed, PLAYER["MAX_THRUST"]))
#        print(f"{self.velocity = }")

    def rotate(self, direction: str, deg_per_sec: float | int | None = None):
        if not self.landed:
            self.__save_state()
            degrees = directions[direction] * (self.rotation_speed if deg_per_sec is None else deg_per_sec)
            self.__change_angle(-degrees)
            self.__change_direction(-degrees)

            old_center = self.rect.center
            self.__rotate_image(self.angle)
            self.__set_rect()
            self.__rect.center = old_center
            self.__set_rect_position()
#            print(f"{self.direction = }\n{self.angle = }")
        else:
            print(f"Can't rotate. {self.landed = }.")

    def __set_rect(self):
        self.__rect = self.image.get_rect()

    def start_fall(self):
        self.falling = True
#        print(f"{self}\f{self.falling = }")

    def stop_fall(self):
        self.falling = False
        self.fall_timer = 0    
#        print(f"{self}\f{self.falling = }")

    def fall(self, time_delta):
        self.fall_timer += time_delta
#        self.__change_position(Vector2(0, G_ACCELERATION))
        return Vector2(0, min(G_ACCELERATION * self.fall_timer, PLAYER["MAX_FALL_VELOCITY"]))

    def __str__(self):
        return f"{'Player 1' if type(self) is PlayerOne else 'Player 2'}"


class PlayerOne(Player):
    def __init__(self, window, spawnpoint: tuple[int | float, int | float]):
        super().__init__(window, spawnpoint, PLAYER["COLOR"]["P1"], PLAYER["CONTROLS"]["P1"])


class PlayerTwo(Player):
    def __init__(self, window, spawnpoint: tuple[int | float, int | float]):
        super().__init__(window, spawnpoint, PLAYER["COLOR"]["P2"], PLAYER["CONTROLS"]["P2"])


class Bullet(MovingObject):
    def __init__(self, start_position: Vector2, direction: Vector2):
        super().__init__()
        self.__radius = BULLET["RADIUS"]
        self.__color = BULLET["COLOR"]
        self.__image = Surface((int(self.radius * 2), int(self.radius * 2)), SRCALPHA)
        self.__rect = self.image.get_rect()
        self.__position = Vector2(start_position)
        self.__direction = Vector2(direction)

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def color(self):
        return self.__color

    @property
    def radius(self):
        return self.__radius

    @property
    def position(self):
        return self.__position

    @property
    def direction(self):
        return self.__direction

    @property
    def velocity(self):
        return self.__direction * BULLET["SPEED"]

    def __change_position(self, delta: Vector2):
        self.__position += delta

    def __set_rect_position(self):
        self.__rect.center = self.position

    def update(self, time_delta: float | int):
        self.__change_position(self.velocity * time_delta)
        self.__set_rect_position()

    def collide(self, offset: tuple[int, int], other_object):
        pass

    def draw(self):
        draw.circle(self.image, self.color, self.position, self.radius)

    def __str__(self):
        return f"Bullet at {self.position} with velocity {self.velocity}"



class StaticObject(sprite.Sprite):
    def __init__(self):
        super().__init__()

class OuterBoundary(StaticObject):
    def __init__(self, window, type: str):
        self.window = window
        self.name = type + " boundary"
        super().__init__()

        window_w, window_h = self.window.get_size()
        types = {
            "Top": ((0, 0), (window_w, BORDER_THICKNESS)),
            "Bottom": ((0, window_h - BORDER_THICKNESS), (window_w, BORDER_THICKNESS)),
            "Left": ((0, BORDER_THICKNESS), (BORDER_THICKNESS, window_h - BORDER_THICKNESS * 2)),
            "Right": ((window_w - BORDER_THICKNESS, BORDER_THICKNESS), (BORDER_THICKNESS, window_h - BORDER_THICKNESS * 2))
        }
        self.__position = types[type][0]
        self.__size = types[type][1]
        self.__image = Surface(self.size)
        self.__image.fill((155, 155, 155))
        self.__rect = self.__image.get_rect(topleft=self.__position)

    @property
    def position(self):
        return self.__position    
    @property
    def size(self):
        return self.__size
    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    def draw(self):
        self.window.blit(self.image, self.position)
    
    def __str__(self):
        return self.name