import pygame
import random
import numpy as np
import os

pygame.init()
pygame.mixer.init()

# Window setup
screen_width, screen_height = 1300, 750
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snakes with Safiya")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green_light = (0, 180, 0)
green_dark = (0, 100, 0)
red = (255, 0, 0)
grass_green = (100, 220, 100)

# Fonts & clock
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()

# High score file
HIGH_SCORE_FILE = "high_score.txt"

def get_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    else:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

# Sounds
def create_beep(frequency=440, duration_ms=150, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n_samples, False)
    wave = 32767 * np.sin(2 * np.pi * frequency * t)
    wave = wave.astype(np.int16)
    stereo_wave = np.column_stack((wave, wave))
    sound = pygame.sndarray.make_sound(stereo_wave)
    sound.set_volume(volume)
    return sound

menu_sound = create_beep(500, 300, 0.5)
start_sound = create_beep(600, 300, 0.6)
eat_sound = create_beep(800, 150, 0.5)
game_over_sound = create_beep(200, 500, 0.5)

# Text rendering
def text_screen(text, color, x, y, size="small"):
    screen_text = font.render(text, True, color) if size == "small" else big_font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Snake drawing
def plot_snake(snake_list, size):
    for i, (x, y) in enumerate(snake_list):
        ratio = i / len(snake_list) if len(snake_list) > 0 else 0
        color = (
            int(green_dark[0] + ratio * (green_light[0] - green_dark[0])),
            int(green_dark[1] + ratio * (green_light[1] - green_dark[1])),
            int(green_dark[2] + ratio * (green_light[2] - green_dark[2]))
        )
        pygame.draw.rect(gameWindow, color, [x, y, size, size], border_radius=6)

# Animated grass background
def draw_grass(offset):
    blade_width = 6
    blade_height = 15
    space = 10
    for x in range(0, screen_width, space):
        # Animate the height to sway gently
        sway = (offset + x) % 30
        if sway > 15:
            sway = 30 - sway
        blade_height_mod = blade_height - sway // 2
        # Draw a simple vertical blade of grass
        pygame.draw.rect(gameWindow, grass_green, (x, screen_height - blade_height_mod, blade_width, blade_height_mod))

# Obstacle walls with entrance
def draw_obstacles():
    walls = []

    # Top wall with entrance gap
    walls.append(pygame.Rect(300, 200, 300, 20))  # left part
    walls.append(pygame.Rect(700, 200, 300, 20))  # right part

    # Bottom wall (solid)
    walls.append(pygame.Rect(300, 530, 700, 20))

    # Side walls
    walls.append(pygame.Rect(300, 200, 20, 350))
    walls.append(pygame.Rect(980, 200, 20, 350))

    # Draw walls
    for wall in walls:
        pygame.draw.rect(gameWindow, black, wall)

    return walls

# Show menu screen
def show_menu():
    menu_sound.play()
    menu_running = True
    while menu_running:
        gameWindow.fill(white)
        text_screen("Welcome to Snakes with Safiya!", black, 420, 300, "big")
        text_screen("Press Enter to Start", black, 540, 380, "big")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False

# Game loop
def gameloop():
    start_sound.play()
    snake_x, snake_y = 100, 100
    velocity_x, velocity_y = 0, 0
    snake_size = 20
    snake_list = []
    snake_length = 1
    food_x = random.randint(20, screen_width - 40)
    food_y = random.randint(20, screen_height - 40)
    score = 0
    fps = 15
    offset = 0

    high_score = get_high_score()

    exit_game = False
    game_over = False

    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter to Restart", red, 400, 330, "big")
            text_screen(f"Final Score: {score * 2}", black, 480, 380)
            text_screen(f"High Score: {high_score * 2}", black, 480, 430)
            pygame.display.update()
            game_over_sound.play()
            save_high_score(max(score, high_score))
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and velocity_x == 0:
                        velocity_x = 5
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT and velocity_x == 0:
                        velocity_x = -5
                        velocity_y = 0
                    elif event.key == pygame.K_UP and velocity_y == 0:
                        velocity_y = -5
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN and velocity_y == 0:
                        velocity_y = 5
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # Food collision
            if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
                score += 1
                eat_sound.play()
                food_x = random.randint(20, screen_width - 40)
                food_y = random.randint(20, screen_height - 40)
                snake_length += 5

            # Update snake body
            head = [snake_x, snake_y]
            snake_list.append(head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            # Self collision
            if head in snake_list[:-1]:
                game_over = True

            # Wall collision
            if snake_x < 0 or snake_x > screen_width - snake_size or snake_y < 0 or snake_y > screen_height - snake_size:
                game_over = True

            # Obstacle collision
            walls = draw_obstacles()
            for wall in walls:
                if wall.colliderect(pygame.Rect(snake_x, snake_y, snake_size, snake_size)):
                    game_over = True

            # Update animation offset
            offset += 1

            # Draw background and grass
            gameWindow.fill(white)
            draw_grass(offset)

            # Draw obstacles
            draw_obstacles()

            # Draw food
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            # Draw snake
            plot_snake(snake_list, snake_size)

            # Draw score and high score
            text_screen(f"Score: {score * 2}", black, 10, 10)
            text_screen(f"High Score: {high_score * 2}", black, 1100, 10)

            pygame.display.update()
            clock.tick(fps)

    pygame.quit()
    quit()

# Show menu first
show_menu()

# Then start the game
gameloop()
