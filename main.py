from sprites import *
from pygame import init, time, RESIZABLE, event as pygame_event, QUIT, quit as pg_quit, key
from pygame_gui import UIManager

class Mayhem():
    def __init__(self):
        self.main()

    def main(self):

        init()
        self.clock = time.Clock()
        self.window = display.set_mode((window_w, window_h), RESIZABLE)
        display.set_caption("\x1b[1mMAYHEM\x1b[0m")
#        self.ui_manager = UIManager((window_w, window_h), THEME_PATH)

        self.player_one = PlayerOne(self.window)
        self.player_two = PlayerTwo(self.window)
        self.player_group = sprite.Group(self.player_one, self.player_two)
        self.run()

    def run(self):

        while True:
            self.window.fill(BG_COLOR)
            self.time_delta = self.clock.tick(FRAMERATE) / 1000

            self.handle_events()

            self.player_group.draw(self.window)
            self.player_group.update()
            display.flip()
            display.update()
            self.clock.tick(FRAMERATE)

    def handle_events(self):
        for event in pygame_event.get():
            if event.type == QUIT:
                print("\nQuitting...\n")
                self.quit()
        
        self.check_keys()

    def check_keys(self):
        keys_pressed = key.get_pressed()
        
        if keys_pressed[p1_controls["thrust"]]:
            self.player_one.thrust()
        if keys_pressed[p1_controls["rotate_counter_clockwise"]]:
            self.player_one.rotate("counter_clockwise")
        if keys_pressed[p1_controls["rotate_clockwise"]]:
            self.player_one.rotate("clockwise")
        if keys_pressed[p1_controls["fire"]]:
            self.player_one.fire()

        if keys_pressed[p2_controls["thrust"]]:
            self.player_two.thrust()
        if keys_pressed[p2_controls["rotate_counter_clockwise"]]:
            self.player_two.rotate("counter_clockwise")
        if keys_pressed[p2_controls["rotate_clockwise"]]:
            self.player_two.rotate("clockwise")
        if keys_pressed[p2_controls["fire"]]:
            self.player_two.fire()
            
    def quit(self):
        pg_quit()
        exit()

if __name__ == "__main__":

    Mayhem()











