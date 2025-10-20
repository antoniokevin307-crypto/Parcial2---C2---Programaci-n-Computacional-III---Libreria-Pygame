import pygame
import os
import random
pygame.init()

# === CONFIGURACIÓN DE RUTAS ===
BASE_DIR = os.path.dirname(_file_)        # Carpeta donde está este archivo .py
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")  # Carpeta con las imágenes

# === CONFIGURACIÓN DE LA PANTALLA ===
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1200
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# === CARGA DE IMÁGENES ===
# Imágenes del personaje
RUNNING = [
    pygame.image.load(os.path.join(ASSETS_DIR, "Nayib", "NayibRun1.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "Nayib", "NayibRun2.png"))
]
JUMPING = pygame.image.load(os.path.join(ASSETS_DIR, "Nayib", "NayibJump.png"))
DUCKING = [
    pygame.image.load(os.path.join(ASSETS_DIR, "Nayib", "NayibDuck1.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "Nayib", "NayibDuck2.png"))
]

# Cactus pequeños y grandes
SMALL_CACTUS = [
    pygame.image.load(os.path.join(ASSETS_DIR, "Obstaculos", "SmallCactus1.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "Obstaculos", "SmallCactus2.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "Obstaculos", "SmallCactus3.png"))
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join(ASSETS_DIR, "Obstaculos", "LargeCactus1.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "Obstaculos", "LargeCactus2.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "Obstaculos", "LargeCactus3.png"))
]

# Pájaro enemigo
BIRD = [
    pygame.image.load(os.path.join(ASSETS_DIR, "Bird", "Bird1.png")),
    pygame.image.load(os.path.join(ASSETS_DIR, "Bird", "Bird2.png"))
]

# Nubes y fondo
CLOUD = pygame.image.load(os.path.join(ASSETS_DIR, "Otros", "Cloud1.png"))
BG = pygame.image.load(os.path.join(ASSETS_DIR, "Otros", "Track.png"))


# === CLASE PRINCIPAL DEL PERSONAJE ===
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5  # Velocidad de salto

    def _init_(self):
        # Asigna las imágenes del personaje
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        # Estados del personaje
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        # Variables de movimiento
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        # Dependiendo de la acción del jugador, el dinosaurio hace algo
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        # Reinicia el ciclo de movimiento
        if self.step_index >= 10:
            self.step_index = 0

        # Controles del teclado
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        # Cuando el dinosaurio se agacha
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        # Cuando el dinosaurio corre
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        # Movimiento del salto
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


# === CLASE DE LAS NUBES ===
class Cloud:
    def _init_(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(100, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(100, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


# === CLASE BASE DE OBSTÁCULOS (CACTUS Y PÁJARO) ===
class Obstacle:
    def _init_(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


# === DIFERENTES TIPOS DE OBSTÁCULOS ===
class SmallCactus(Obstacle):
    def _init_(self, image):
        self.type = random.randint(0, 2)
        super()._init_(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def _init_(self, image):
        self.type = random.randint(0, 2)
        super()._init_(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def _init_(self, image):
        self.type = 0
        super()._init_(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        # Hace que las alas se muevan
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


# === FUNCIÓN PRINCIPAL DEL JUEGO ===
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()

    # Variables del juego
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    # Puntuación
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    # Fondo en movimiento
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # === LOOP PRINCIPAL ===
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        # Crea obstáculos aleatorios
        if len(obstacles) == 0:
            choice = random.randint(0, 2)
            if choice == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif choice == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD))

        # Mueve los obstáculos
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()

            # Detecta colisión
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()
        cloud.draw(SCREEN)
        cloud.update()
        score()

        clock.tick(30)
        pygame.display.update()


# === MENÚ PRINCIPAL Y REINICIO ===
def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Presioná cualquier tecla para iniciar", True, (0, 0, 0))
        else:
            text = font.render("Presioná cualquier tecla para reiniciar", True, (0, 0, 0))
            score = font.render("Tu Puntaje: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()

        # Espera a que se presione una tecla
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()


# === INICIO DEL JUEGO ===
menu(death_count=0)
pygame.quit()
