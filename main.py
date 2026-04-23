from sprites import *
from pygame import init, display, time, RESIZABLE, event as pygame_event, QUIT, quit as pg_quit, key
from pygame_gui import UIManager

class Mayhem():
    def __init__(self):
        self.p1_spawnpoint = (WINDOW_W - WINDOW_W // 1.618, WINDOW_H // 1.618)
        self.p2_spawnpoint = (WINDOW_W // 1.618, WINDOW_H // 1.618)
        self.main()

    def main(self):

        init()
        self.clock = time.Clock()
        self.window = display.set_mode((WINDOW_W, WINDOW_H), RESIZABLE)
        display.set_caption(CAPTION)
#        self.ui_manager = UIManager((WINDOW_W, WINDOW_H), THEME_PATH)

        self.object_group = sprite.Group()
        self.create_map()
        self.create_movable_objects()
        self.run()

    def create_map(self):
        top_boundary = OuterBoundary(self.window, type="Top")
        bottom_boundary = OuterBoundary(self.window, type="Bottom")
        left_boundary = OuterBoundary(self.window, type="Left")
        right_boundary = OuterBoundary(self.window, type="Right")
        self.static_objects = sprite.Group(top_boundary, bottom_boundary, left_boundary, right_boundary)
        self.object_group.add(obj for obj in self.static_objects)

    def create_movable_objects(self):
        self.player_one = PlayerOne(self.window, self.p1_spawnpoint)
        self.player_two = PlayerTwo(self.window, self.p2_spawnpoint)
        self.movable_objects = sprite.Group(self.player_one, self.player_two)
        self.object_group.add(obj for obj in self.movable_objects)

    def run(self):
        runtime = 0
        while True:
            self.window.fill(COLORS["BACKGROUND"])
            time_delta = self.clock.tick(FRAMERATE) / 1000
            runtime += time_delta
            prev_runtime_int = int(runtime - time_delta)
            [print(f"{int(runtime) = }") if int(runtime) != prev_runtime_int and int(runtime) % 2 == 0 else None]

            self.handle_events(time_delta)
            self.object_group.update(time_delta)
            self.handle_collisions()
            self.object_group.draw(self.window)
            display.flip()
#            self.clock.tick(FRAMERATE)

    def handle_events(self, time_delta):
        events = pygame_event.get()
        for event in events:
            if event.type == QUIT:
                print("\nQuitting...\n")
                self.quit()

            if event.type == WINDOWRESIZED:
                self.window = display.set_mode((max(event.x, WINDOW_W),
                                                max(event.y, WINDOW_H)),
                                                RESIZABLE)

            if event.type == KEYDOWN:
                if event.key == PLAYER["CONTROLS"]["P1"]["thrust"]:
                    self.player_one.start_thrust()
#                    print(f"{self.player_one.thrusting = }")
                elif event.key == PLAYER["CONTROLS"]["P2"]["thrust"]:
                    self.player_two.start_thrust()
#                    print(f"{self.player_two.thrusting = }")
            elif event.type == KEYUP:
                if event.key == PLAYER["CONTROLS"]["P1"]["thrust"]:
                    self.player_one.stop_thrust()
#                    print(f"{self.player_one.thrusting = }")
                elif event.key == PLAYER["CONTROLS"]["P2"]["thrust"]:
                    self.player_two.stop_thrust()
#                    print(f"{self.player_two.thrusting = }")
                                                
        self.check_pressed_keys(time_delta)

    def handle_collisions(self):
        collided_objects = []
        for movable_object in self.movable_objects:
            for any_object in self.object_group:
#                print(f"Checking collision between {movable_object} and {any_object}...")

                # Checks rect collision first to save unnecessary pixel-perfect collision checks.
                if sprite.collide_rect(movable_object, any_object) and (movable_object is not any_object):
                    if sprite.collide_mask(movable_object, any_object):
                        collided_objects.append((movable_object, any_object))
#                        print(f"{collided_objects[-1][0]} colliding with {collided_objects[-1][1]}\
#                              {sprite.collide_mask(movable_object, any_object)}")
                        movable_object.collide(sprite.collide_mask(movable_object, any_object),
                                               any_object)
                else:
                    movable_object.landed = False

    def check_pressed_keys(self, time_delta):
        keys_pressed = key.get_pressed()
        
        if keys_pressed[PLAYER["CONTROLS"]["P1"]["thrust"]]:
            self.player_one.thrust(time_delta)
        if keys_pressed[PLAYER["CONTROLS"]["P1"]["rotate_counter_clockwise"]]:
            self.player_one.rotate("counter_clockwise")
        if keys_pressed[PLAYER["CONTROLS"]["P1"]["rotate_clockwise"]]:
            self.player_one.rotate("clockwise")
        if keys_pressed[PLAYER["CONTROLS"]["P1"]["fire"]]:
            self.player_one.fire()

        if keys_pressed[PLAYER["CONTROLS"]["P2"]["thrust"]]:
            self.player_two.thrust(time_delta)
        if keys_pressed[PLAYER["CONTROLS"]["P2"]["rotate_counter_clockwise"]]:
            self.player_two.rotate("counter_clockwise")
        if keys_pressed[PLAYER["CONTROLS"]["P2"]["rotate_clockwise"]]:
            self.player_two.rotate("clockwise")
        if keys_pressed[PLAYER["CONTROLS"]["P2"]["fire"]]:
            self.player_two.fire()
            
    def quit(self):
        pg_quit()
        exit()

if __name__ == "__main__":

    Mayhem()
