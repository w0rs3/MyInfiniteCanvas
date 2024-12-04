import pygame
import sys
from collections import defaultdict
import math
import json

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Canvas Drawing App")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Drawing settings
drawing = False
camera_x, camera_y = 0, 0
zoom = 1.0
brush_size = 5

# Data structure to store drawn points
# Key: (zoom_level, x, y), Value: color
points = defaultdict(lambda: BLACK)

def world_to_screen(x, y):
    screen_x = (x - camera_x) * zoom + WIDTH // 2
    screen_y = (y - camera_y) * zoom + HEIGHT // 2
    return screen_x, screen_y

def screen_to_world(x, y):
    world_x = (x - WIDTH // 2) / zoom + camera_x
    world_y = (y - HEIGHT // 2) / zoom + camera_y
    return world_x, world_y

def draw_point(x, y):
    zoom_level = math.floor(math.log2(zoom))
    points[(zoom_level, round(x), round(y))] = BLACK

def render():
    screen.fill(WHITE)
    zoom_level = math.floor(math.log2(zoom))
    visible_range = 10

    min_x, min_y = screen_to_world(0, 0)
    max_x, max_y = screen_to_world(WIDTH, HEIGHT)

    center_x, center_y = camera_x, camera_y

    for level in range(zoom_level - visible_range, zoom_level + visible_range):
        for (z, x, y), color in points.items():
            if z == level and min_x <= x <= max_x and min_y <= y <= max_y:
                screen_x, screen_y = world_to_screen(x, y)

                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)

                base_size = brush_size * zoom / (2 ** abs(level - zoom_level))
                distance_factor = 1 / (1 + distance * 0.01 * zoom)
                size = max(1, base_size * distance_factor)

                pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), int(size))

    pygame.display.flip()

def save_drawing():
    data = {str(k): v for k, v in points.items()}
    with open('drawing.json', 'w') as f:
        json.dump(data, f)
    print("Drawing saved!")

def load_drawing():
    global points
    try:
        with open('drawing.json', 'r') as f:
            data = json.load(f)
        points = defaultdict(lambda: BLACK, {tuple(map(int, k[1:-1].split(','))): tuple(v) for k, v in data.items()})
        print("Drawing loaded!")
    except FileNotFoundError:
        print("No saved drawing found.")

# Main loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                drawing = True
                x, y = screen_to_world(*event.pos)
                draw_point(x, y)
            elif event.button == 4:  # Scroll up
                zoom *= 1.1
            elif event.button == 5:  # Scroll down
                zoom /= 1.1

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                x, y = screen_to_world(*event.pos)
                draw_point(x, y)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_drawing()
            elif event.key == pygame.K_l:
                load_drawing()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= 10 / zoom
    if keys[pygame.K_RIGHT]:
        camera_x += 10 / zoom
    if keys[pygame.K_UP]:
        camera_y -= 10 / zoom
    if keys[pygame.K_DOWN]:
        camera_y += 10 / zoom

    render()
    clock.tick(60)
