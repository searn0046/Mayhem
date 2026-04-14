import pygame

class PolygonSprite(pygame.sprite.Sprite):
    def __init__(self, color, points):
        super().__init__()
        
        # 1. Determine the size needed for the surface
        # We find the max X and Y coordinates to know how big the 'canvas' should be
        width = max(p[0] for p in points)
        height = max(p[1] for p in points)
        
        # 2. Create the 'image' (the Surface)
        # pygame.SRCALPHA makes it support transparency
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # 3. Draw the polygon onto THIS sprite's image, not the main screen
        pygame.draw.polygon(self.image, color, points)
        
        # 4. Define the 'rect' (the position and boundaries)
        # The Group needs this to know WHERE to draw the image
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100) # Set your starting position


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    # Example usage:
    points = [(0, 0), (50, 0), (25, 50)]  # A simple triangle
    my_sprite = PolygonSprite((255, 0, 0), points)
    my_group = pygame.sprite.Group(my_sprite)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((255, 255, 255))  # Clear the screen with white
        my_group.draw(screen)  # Draw all sprites in the group
        pygame.display.flip()  # Update the display