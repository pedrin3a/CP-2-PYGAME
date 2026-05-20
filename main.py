
import pygame
import random

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

font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 60, bold=True)

# =========================================
# FASES
# =========================================
levels = [

    {
        "platforms": [
            pygame.Rect(0, 650, 1200, 50),
            pygame.Rect(200, 550, 200, 25),
            pygame.Rect(500, 470, 220, 25),
            pygame.Rect(850, 380, 180, 25),
            pygame.Rect(950, 250, 180, 25),
        ],

        "traps": [
            pygame.Rect(420, 630, 100, 20),
            pygame.Rect(740, 630, 100, 20),
        ],

        "cheese": pygame.Rect(1020, 190, 30, 30),

        "hole": pygame.Rect(1100, 580, 60, 60)
    },

    {
        "platforms": [
            pygame.Rect(0, 650, 1200, 50),
            pygame.Rect(100, 560, 180, 25),
            pygame.Rect(400, 480, 180, 25),
            pygame.Rect(700, 390, 180, 25),
            pygame.Rect(980, 300, 160, 25),
        ],

        "traps": [
            pygame.Rect(300, 630, 120, 20),
            pygame.Rect(600, 630, 120, 20),
            pygame.Rect(900, 630, 120, 20),
        ],

        "cheese": pygame.Rect(1030, 240, 30, 30),

        "hole": pygame.Rect(80, 580, 60, 60)
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
player_speed = 6
jump_force = -15
on_ground = False

# =========================================
# GAME
# =========================================
cheese_collected = False
score = 0
victory = False
running = True

# ESTADO DO JOGO
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

            # MENU
            if game_state == "menu":

                if event.key == pygame.K_RETURN:
                    game_state = "playing"

            # JOGO
            elif game_state == "playing":

                if event.key == pygame.K_SPACE and on_ground:
                    player_vel_y = jump_force

                if event.key == pygame.K_r:

                    current_level = 0
                    score = 0
                    victory = False

                    load_level()
                    reset_player()

            # REINICIAR APÓS VITÓRIA
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

        screen.fill((25, 25, 40))

        title = big_font.render(
            "Transformouse",
            True,
            YELLOW
        )

        start_text = font.render(
            "Pressione ENTER para jogar",
            True,
            WHITE
        )

        controls1 = font.render(
            "A/D para mover",
            True,
            BLUE
        )

        controls2 = font.render(
            "ESPAÇO para pular",
            True,
            BLUE
        )

        objective = font.render(
            "Pegue o queijo e volte para a toca!",
            True,
            GREEN
        )

        screen.blit(title, (280, 180))
        screen.blit(start_text, (390, 300))
        screen.blit(controls1, (470, 380))
        screen.blit(controls2, (445, 430))
        screen.blit(objective, (300, 520))

    # =========================================
    # GAMEPLAY
    # =========================================
    elif game_state == "playing":

        # =========================================
        # MOVIMENTO
        # =========================================
        keys = pygame.key.get_pressed()

        if not victory:

            if keys[pygame.K_a]:
                player.x -= player_speed

            if keys[pygame.K_d]:
                player.x += player_speed

        # =========================================
        # GRAVIDADE
        # =========================================
        player_vel_y += GRAVITY
        player.y += player_vel_y

        on_ground = False

        # =========================================
        # COLISÃO PLATAFORMAS
        # =========================================
        for platform in platforms:

            if player.colliderect(platform):

                if player_vel_y > 0:

                    player.bottom = platform.top
                    player_vel_y = 0
                    on_ground = True

        # =========================================
        # LIMITES
        # =========================================
        if player.left < 0:
            player.left = 0

        if player.right > WIDTH:
            player.right = WIDTH

        # =========================================
        # ARMADILHAS
        # =========================================
        for trap in traps:

            if player.colliderect(trap):

                create_particles(
                    player.centerx,
                    player.centery,
                    RED
                )

                reset_player()

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
        # TOCA
        # =========================================
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

        # =========================================
        # PARTÍCULAS
        # =========================================
        for particle in particles[:]:

            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]

            particle["life"] -= 1

            if particle["life"] <= 0:
                particles.remove(particle)

        # =========================================
        # CENÁRIO FLORESTA
        # =========================================
        sky_color = (120, 200, 255)
        grass_color = (70, 170, 70)

        # céu
        screen.fill(sky_color)

        # chão
        pygame.draw.rect(
            screen,
            grass_color,
            (0, 620, WIDTH, 80)
        )

        # montanhas
        pygame.draw.polygon(
            screen,
            (90, 120, 90),
            [(0, 620), (250, 300), (500, 620)]
        )

        pygame.draw.polygon(
            screen,
            (70, 100, 70),
            [(300, 620), (650, 250), (900, 620)]
        )

        pygame.draw.polygon(
            screen,
            (80, 110, 80),
            [(700, 620), (1000, 320), (1200, 620)]
        )

        # árvores
        for x in range(0, WIDTH, 120):

            pygame.draw.rect(
                screen,
                (120, 70, 20),
                (x + 40, 520, 25, 100)
            )

            pygame.draw.circle(
                screen,
                (40, 140, 40),
                (x + 52, 500),
                45
            )

            pygame.draw.circle(
                screen,
                (50, 160, 50),
                (x + 25, 515),
                35
            )

            pygame.draw.circle(
                screen,
                (50, 160, 50),
                (x + 80, 515),
                35
            )

        # nuvens
        for x in range(100, WIDTH, 300):

            pygame.draw.circle(screen, WHITE, (x, 100), 30)
            pygame.draw.circle(screen, WHITE, (x + 30, 90), 35)
            pygame.draw.circle(screen, WHITE, (x + 60, 100), 30)

        # =========================================
        # PLATAFORMAS
        # =========================================
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

        # =========================================
        # ARMADILHAS
        # =========================================
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
        # TOCA
        # =========================================
        pygame.draw.ellipse(screen, BROWN, hole)

        pygame.draw.ellipse(
            screen,
            BLACK,
            (hole.x + 10, hole.y + 10, 40, 40)
        )

        # =========================================
        # QUEIJO
        # =========================================
        if not cheese_collected:

            pygame.draw.circle(
                screen,
                YELLOW,
                cheese.center,
                20
            )

        # =========================================
        # RATINHO
        # =========================================
        pygame.draw.line(
            screen,
            (255, 150, 200),
            (player.x + 20, player.y + 25),
            (player.x - 20, player.y + 10),
            5
        )

        pygame.draw.ellipse(screen, GRAY, player)

        pygame.draw.ellipse(
            screen,
            (220, 220, 220),
            (player.x + 10, player.y + 16, 28, 22)
        )

        pygame.draw.circle(screen, GRAY, (player.x + 10, player.y + 8), 10)
        pygame.draw.circle(screen, GRAY, (player.x + 38, player.y + 8), 10)

        pygame.draw.circle(screen, (255, 170, 200), (player.x + 10, player.y + 8), 5)
        pygame.draw.circle(screen, (255, 170, 200), (player.x + 38, player.y + 8), 5)

        pygame.draw.circle(screen, BLACK, (player.x + 16, player.y + 20), 4)
        pygame.draw.circle(screen, BLACK, (player.x + 32, player.y + 20), 4)

        pygame.draw.circle(screen, RED, (player.x + 24, player.y + 28), 4)

        pygame.draw.line(screen, WHITE, (player.x + 24, player.y + 28), (player.x + 45, player.y + 24), 2)
        pygame.draw.line(screen, WHITE, (player.x + 24, player.y + 30), (player.x + 45, player.y + 30), 2)
        pygame.draw.line(screen, WHITE, (player.x + 24, player.y + 32), (player.x + 45, player.y + 36), 2)

        pygame.draw.line(screen, WHITE, (player.x + 24, player.y + 28), (player.x + 3, player.y + 24), 2)
        pygame.draw.line(screen, WHITE, (player.x + 24, player.y + 30), (player.x + 3, player.y + 30), 2)
        pygame.draw.line(screen, WHITE, (player.x + 24, player.y + 32), (player.x + 3, player.y + 36), 2)

        # =========================================
        # PARTÍCULAS
        # =========================================
        for particle in particles:

            pygame.draw.circle(
                screen,
                particle["color"],
                (int(particle["x"]), int(particle["y"])),
                3
            )

        # =========================================
        # HUD
        # =========================================
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

        controls_text = font.render(
            "A/D mover | ESPAÇO pular",
            True,
            WHITE
        )

        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (20, 60))
        screen.blit(controls_text, (20, 100))

        # =========================================
        # VITÓRIA
        # =========================================
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

            screen.blit(victory_text, (380, 280))
            screen.blit(restart_text, (420, 360))

    pygame.display.flip()

pygame.quit()
