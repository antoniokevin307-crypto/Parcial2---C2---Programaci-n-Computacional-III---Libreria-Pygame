import pygame
import os

pygame.init()

# Global Constants
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1200
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BG = pygame.image.load(os.path.join("Assets/Otros", "Track.png"))

def main():
    show_start_screen()  # Mostrar pantalla de inicio
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

def show_start_screen():
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render("Press any key to start", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.fill((255, 255, 255))
    SCREEN.blit(text, textRect)
    pygame.display.update()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def background():
    SCREEN.blit(BG, (0, 0))

x_pos_bg = 0
y_pos_bg = 380

main()

pygame.quit()
