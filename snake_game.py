import pygame
import random
import sys

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

# -----------------------------
# Screen settings
# -----------------------------
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic Snake Game")

# -----------------------------
# Colors
# -----------------------------
BLACK = (20, 20, 20)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 50, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
GRAY = (100, 100, 100)

# -----------------------------
# Fonts
# -----------------------------
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 55)

# -----------------------------
# Clock
# -----------------------------
clock = pygame.time.Clock()


# -----------------------------
# Create food
# -----------------------------
def create_food(snake):
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)

        food = (x, y)

        if food not in snake:
            return food


# -----------------------------
# Draw snake
# -----------------------------
def draw_snake(snake):
    for index, segment in enumerate(snake):

        x, y = segment

        if index == 0:
            # Snake head
            pygame.draw.rect(
                screen,
                DARK_GREEN,
                (x, y, CELL_SIZE, CELL_SIZE)
            )
        else:
            # Snake body
            pygame.draw.rect(
                screen,
                GREEN,
                (x, y, CELL_SIZE, CELL_SIZE)
            )

        # Border around each segment
        pygame.draw.rect(
            screen,
            BLACK,
            (x, y, CELL_SIZE, CELL_SIZE),
            1
        )


# -----------------------------
# Draw food
# -----------------------------
def draw_food(food):
    x, y = food

    pygame.draw.rect(
        screen,
        RED,
        (x, y, CELL_SIZE, CELL_SIZE)
    )


# -----------------------------
# Display score
# -----------------------------
def draw_score(score, level):
    score_text = font.render(
        f"Score: {score}   Level: {level}",
        True,
        WHITE
    )

    screen.blit(score_text, (10, 10))


# -----------------------------
# Game Over screen
# -----------------------------
def game_over_screen(score):
    screen.fill(BLACK)

    game_over_text = big_font.render(
        "GAME OVER",
        True,
        RED
    )

    score_text = font.render(
        f"Final Score: {score}",
        True,
        WHITE
    )

    restart_text = font.render(
        "Press R to Restart",
        True,
        YELLOW
    )

    quit_text = font.render(
        "Press Q to Quit",
        True,
        GRAY
    )

    screen.blit(
        game_over_text,
        (
            WIDTH // 2 - game_over_text.get_width() // 2,
            180
        )
    )

    screen.blit(
        score_text,
        (
            WIDTH // 2 - score_text.get_width() // 2,
            270
        )
    )

    screen.blit(
        restart_text,
        (
            WIDTH // 2 - restart_text.get_width() // 2,
            330
        )
    )

    screen.blit(
        quit_text,
        (
            WIDTH // 2 - quit_text.get_width() // 2,
            380
        )
    )

    pygame.display.update()


# -----------------------------
# Main game function
# -----------------------------
def run_game():

    # Snake starting position
    snake = [
        (300, 300),
        (280, 300),
        (260, 300)
    ]

    # Starting direction
    direction = (CELL_SIZE, 0)

    # Food
    food = create_food(snake)

    # Score
    score = 0

    # Starting speed
    speed = 8

    # Game state
    game_over = False

    # -------------------------
    # Game loop
    # -------------------------
    while True:

        # -------------------------
        # Event handling
        # -------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # Move Up
                if event.key in (pygame.K_UP, pygame.K_w):
                    if direction != (0, CELL_SIZE):
                        direction = (0, -CELL_SIZE)

                # Move Down
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if direction != (0, -CELL_SIZE):
                        direction = (0, CELL_SIZE)

                # Move Left
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if direction != (CELL_SIZE, 0):
                        direction = (-CELL_SIZE, 0)

                # Move Right
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if direction != (-CELL_SIZE, 0):
                        direction = (CELL_SIZE, 0)

                # Restart
                elif event.key == pygame.K_r and game_over:
                    return

                # Quit
                elif event.key == pygame.K_q and game_over:
                    pygame.quit()
                    sys.exit()

        # -------------------------
        # Stop game when game over
        # -------------------------
        if game_over:
            game_over_screen(score)
            clock.tick(10)
            continue

        # -------------------------
        # Calculate new head
        # -------------------------
        head_x, head_y = snake[0]

        new_head = (
            head_x + direction[0],
            head_y + direction[1]
        )

        # Add new head
        snake.insert(0, new_head)

        # -------------------------
        # Food collision
        # -------------------------
        if new_head == food:

            score += 1

            # Create new food
            food = create_food(snake)

            # -------------------------
            # Difficulty progression
            # -------------------------
            # Speed increases every 3 points
            speed = 8 + (score // 3)

        else:
            # Remove tail
            snake.pop()

        # -------------------------
        # Wall collision
        # -------------------------
        if (
            new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        ):
            game_over = True

        # -------------------------
        # Self collision
        # -------------------------
        if new_head in snake[1:]:
            game_over = True

        # -------------------------
        # Level calculation
        # -------------------------
        level = 1 + (score // 3)

        # -------------------------
        # Drawing
        # -------------------------
        screen.fill(BLACK)

        draw_snake(snake)
        draw_food(food)
        draw_score(score, level)

        pygame.display.update()

        # -------------------------
        # Control game speed
        # -------------------------
        clock.tick(speed)


# -----------------------------
# Start the game
# -----------------------------
while True:
    run_game()