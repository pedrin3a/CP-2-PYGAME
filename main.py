
import pygame
import random
import math

pygame.init()

# =========================================
# CONFIG
# =========================================
WIDTH = 1200
HEIGHT = 700
FPS = 60
GRAVITY = 0.8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TRANSOFORMOUSE")

clock = pygame.time.Clock()

# =========================================
# FUNDO
# =========================================
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
# =========================================
# SPRITE DO RATINHO
# =========================================
mouse_img = pygame.image.load("mouse.png").convert_alpha()
mouse_img = pygame.transform.scale(mouse_img, (60, 60))
# =========================================
# SPRITE DO QUEIJO
# =========================================
cheese_img = pygame.image.load("cheese.png").convert_alpha()
cheese_img = pygame.transform.scale(cheese_img, (40, 40))
# =========================================
# SPRITE DA TOCA
# =========================================
hole_img = pygame.image.load("hole.png").convert_alpha()
hole_img = pygame.transform.scale(hole_img, (55, 55))
# =========================================
# CORES
# =========================================
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
BLUE = (70, 170, 255)
GREEN = (0, 255, 120)
RED = (255, 80, 80)
YELLOW = (255, 220, 0)
BROWN = (140, 90, 50)
GRAY = (150, 150, 160)
PURPLE = (160, 80, 255)

font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 72, bold=True)

# =========================================
# FASES DIFÍCEIS
# =========================================
levels = [

    # =========================================
    # FASE 1
    # =========================================
    {
        "platforms": [
            pygame.Rect(0, 650, 1200, 50),

            pygame.Rect(120, 560, 120, 20),
            pygame.Rect(320, 500, 120, 20),
            pygame.Rect(520, 440, 120, 20),
            pygame.Rect(720, 380, 120, 20),
            pygame.Rect(920, 320, 120, 20),
        ],

        "traps": [
            pygame.Rect(250, 630, 120, 20),
            pygame.Rect(560, 630, 120, 20),
            pygame.Rect(860, 630, 120, 20),
        ],

        "cheese": pygame.Rect(960, 270, 30, 30),

        "hole": pygame.Rect(70, 580, 60, 60)
    },

    # =========================================
    # FASE 2
    # =========================================
    {
        "platforms": [
            pygame.Rect(0, 650, 1200, 50),

            pygame.Rect(100, 570, 90, 20),
            pygame.Rect(260, 510, 90, 20),
            pygame.Rect(430, 450, 90, 20),
            pygame.Rect(610, 390, 90, 20),
            pygame.Rect(800, 330, 90, 20),
            pygame.Rect(980, 260, 90, 20),
        ],

        "traps": [
            pygame.Rect(180, 630, 140, 20),
            pygame.Rect(480, 630, 140, 20),
            pygame.Rect(780, 630, 140, 20),
        ],

        "cheese": pygame.Rect(1000, 210, 30, 30),

        "hole": pygame.Rect(40, 580, 60, 60)
    },

    # =========================================
    # FASE 3
    # =========================================
    {
        "platforms": [
            pygame.Rect(0, 650, 1200, 50),

            pygame.Rect(150, 560, 80, 20),
            pygame.Rect(300, 500, 80, 20),
            pygame.Rect(450, 440, 80, 20),
            pygame.Rect(600, 380, 80, 20),
            pygame.Rect(750, 320, 80, 20),
            pygame.Rect(900, 260, 80, 20),
            pygame.Rect(1050, 200, 80, 20),
        ],

        "traps": [
            pygame.Rect(0, 630, 200, 20),
            pygame.Rect(300, 630, 200, 20),
            pygame.Rect(600, 630, 200, 20),
            pygame.Rect(900, 630, 200, 20),
        ],

        "cheese": pygame.Rect(1070, 150, 30, 30),

        "hole": pygame.Rect(70, 580, 60, 60)
    },

    # =========================================
    # FASE 4
    # =========================================
    {
        "platforms": [
            pygame.Rect(0, 650, 1200, 50),

            pygame.Rect(90, 560, 70, 20),
            pygame.Rect(220, 480, 70, 20),
            pygame.Rect(350, 400, 70, 20),
            pygame.Rect(480, 320, 70, 20),
            pygame.Rect(610, 240, 70, 20),
            pygame.Rect(760, 320, 70, 20),
            pygame.Rect(900, 400, 70, 20),
            pygame.Rect(1030, 480, 70, 20),
        ],

        "traps": [
            pygame.Rect(150, 630, 180, 20),
            pygame.Rect(450, 630, 180, 20),
            pygame.Rect(750, 630, 180, 20),
        ],

        "cheese": pygame.Rect(1040, 430, 30, 30),

        "hole": pygame.Rect(50, 580, 60, 60)
    },

    # =========================================
    # FASE 5
    # =========================================
    {
        "platforms": [
            pygame.Rect(0, 650, 1200, 50),

            pygame.Rect(80, 560, 60, 20),
            pygame.Rect(200, 500, 60, 20),
            pygame.Rect(320, 440, 60, 20),
            pygame.Rect(440, 380, 60, 20),
            pygame.Rect(560, 320, 60, 20),
            pygame.Rect(680, 260, 60, 20),
            pygame.Rect(800, 200, 60, 20),
            pygame.Rect(920, 140, 60, 20),
            pygame.Rect(1040, 200, 60, 20),
        ],

        "traps": [
            pygame.Rect(100, 630, 250, 20),
            pygame.Rect(450, 630, 250, 20),
            pygame.Rect(800, 630, 250, 20),
        ],

        "cheese": pygame.Rect(1060, 150, 30, 30),

        "hole": pygame.Rect(40, 580, 60, 60)
    }
]

# =========================================
# LEVEL ATUAL
# =========================================
current_level = 0

platforms = levels[current_level]["platforms"]
traps = levels[current_level]["traps"]
cheese = levels[current_level]["cheese"]
hole = levels[current_level]["hole"]

# =========================================
# PLAYER
# =========================================
player = pygame.Rect(100, 500, 48, 48)

player_vel_y = 0
player_speed = 5
jump_force = -13
on_ground = False

# =========================================
# GAME
# =========================================
cheese_collected = False
score = 0
victory = False
running = True

game_state = "menu"

# =========================================
# PARTÍCULAS
# =========================================
particles = []

# =========================================
# FUNÇÕES
# =========================================
def create_particles(x, y, color):

    for _ in range(20):

        particles.append({
            "x": x,
            "y": y,
            "dx": random.uniform(-4, 4),
            "dy": random.uniform(-4, 4),
            "life": random.randint(20, 40),
            "color": color
        })


def load_level():

    global platforms
    global traps
    global cheese
    global hole

    platforms = levels[current_level]["platforms"]
    traps = levels[current_level]["traps"]
    cheese = levels[current_level]["cheese"]
    hole = levels[current_level]["hole"]


def reset_player():

    global player_vel_y
    global cheese_collected

    player.x = 100
    player.y = 500

    player_vel_y = 0
    cheese_collected = False


def draw_gradient():

    for y in range(HEIGHT):

        r = 20 + int(y * 0.05)
        g = 30 + int(y * 0.08)
        b = 70 + int(y * 0.15)

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

# =========================================
# LOOP PRINCIPAL
# =========================================
while running:

    clock.tick(FPS)

    # =========================================
    # EVENTOS
    # =========================================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "menu":

                if event.key == pygame.K_RETURN:
                    game_state = "playing"

            elif game_state == "playing":

                if event.key == pygame.K_SPACE and on_ground:
                    player_vel_y = jump_force

                if event.key == pygame.K_r:

                    current_level = 0
                    score = 0
                    victory = False

                    load_level()
                    reset_player()

            if victory:

                if event.key == pygame.K_r:

                    current_level = 0
                    score = 0
                    victory = False

                    load_level()
                    reset_player()

                    game_state = "menu"

    # =========================================
    # MENU
    # =========================================
    if game_state == "menu":

        draw_gradient()

        title = big_font.render(
            "TRANSOFORMOUSE",
            True,
            YELLOW
        )


        start_text = font.render(
            "PRESSIONE ENTER PARA JOGAR",
            True,
            GREEN
        )

        pygame.draw.rect(
            screen,
            (15, 15, 30),
            (250, 160, 700, 350),
            border_radius=25
        )

        pygame.draw.rect(
            screen,
            PURPLE,
            (250, 160, 700, 350),
            4,
            border_radius=25
        )

        screen.blit(title, (290, 210))

        screen.blit(start_text, (350, 400))

    # =========================================
    # GAMEPLAY
    # =========================================
    elif game_state == "playing":

        keys = pygame.key.get_pressed()

        if not victory:

            if keys[pygame.K_a]:
                player.x -= player_speed

            if keys[pygame.K_d]:
                player.x += player_speed

        # gravidade
        player_vel_y += GRAVITY
        player.y += player_vel_y

        on_ground = False

        # colisão
        for platform in platforms:

            if player.colliderect(platform):

                if player_vel_y > 0:

                    player.bottom = platform.top
                    player_vel_y = 0
                    on_ground = True

        # limites
        if player.left < 0:
            player.left = 0

        if player.right > WIDTH:
            player.right = WIDTH

        # armadilhas
        for trap in traps:

            if player.colliderect(trap):

                create_particles(
                    player.centerx,
                    player.centery,
                    RED
                )

                reset_player()


        # toca
        if player.colliderect(hole) and cheese_collected:

            create_particles(
                hole.centerx,
                hole.centery,
                GREEN
            )

            if current_level < len(levels) - 1:

                current_level += 1

                load_level()
                reset_player()

            else:

                victory = True

        # partículas
        for particle in particles[:]:

            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]

            particle["life"] -= 1

            if particle["life"] <= 0:
                particles.remove(particle)

        # =========================================
        # FUNDO
        # =========================================
        screen.blit(background, (0, 0))

        # plataformas
        for platform in platforms:

            pygame.draw.rect(
                screen,
                (90, 90, 120),
                platform,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                WHITE,
                platform,
                2,
                border_radius=10
            )

        # armadilhas
        for trap in traps:

            pygame.draw.rect(screen, RED, trap)

            for i in range(trap.x, trap.x + trap.width, 15):

                pygame.draw.polygon(
                    screen,
                    WHITE,
                    [
                        (i, trap.y),
                        (i + 7, trap.y - 15),
                        (i + 14, trap.y)
                    ]
                )
        # =========================================
        # PEGAR QUEIJO
        # =========================================
        if player.colliderect(cheese) and not cheese_collected:
            cheese_collected = True
            score += 100

            create_particles(
                cheese.centerx,
                cheese.centery,
                YELLOW
            )

        # =========================================
        # QUEIJO IMAGEM
        # =========================================
        if not cheese_collected:
            screen.blit(
                cheese_img,
                (cheese.x - 5, cheese.y - 5)
            )
        # =========================================
        # TOCA IMAGEM
        # =========================================
        screen.blit(
            hole_img,
            (hole.x + 2, hole.y + 2)
        )
        # =========================================
        # RATINHO IMAGEM
        # =========================================
        screen.blit(mouse_img, (player.x - 6, player.y - 6))
        # partículas
        for particle in particles:

            pygame.draw.circle(
                screen,
                particle["color"],
                (int(particle["x"]), int(particle["y"])),
                3
            )

        # HUD
        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        level_text = font.render(
            f"FASE: {current_level + 1}",
            True,
            BLUE
        )

        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (20, 60))

        # vitória
        if victory:

            victory_text = big_font.render(
                "VOCÊ ZEROU!",
                True,
                GREEN
            )

            restart_text = font.render(
                "Pressione R para reiniciar",
                True,
                WHITE
            )

            screen.blit(victory_text, (320, 260))
            screen.blit(restart_text, (390, 360))

    pygame.display.flip()

pygame.quit()

