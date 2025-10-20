import pygame
import os
import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1200
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CLOUD = pygame.image.load(os.path.join("Assets/Otros", "Cloud1.png"))
BG = pygame.image.load(os.path.join("Assets/Otros", "Track.png"))

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        background()

        pygame.display.update()
        clock.tick(30)

def background():
    global x_pos_bg, y_pos_bg
    image_width = BG.get_width()
    SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    if x_pos_bg <= -image_width:
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        x_pos_bg = 0
    x_pos_bg -= 20  # Ajusta la velocidad de desplazamiento

def draw_clouds(clouds):
    for cloud in clouds:
        cloud.draw(SCREEN)
        cloud.update()

class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = CLOUD

    def update(self):
        self.x -= 20  # Ajusta la velocidad de desplazamiento de las nubes
        if self.x < -self.image.get_width():
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(100, 200)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

x_pos_bg = 0
y_pos_bg = 380

clouds = [Cloud(random.randint(0, SCREEN_WIDTH), random.randint(100, 200)) for _ in range(5)]

main()

pygame.quit()
