import pygame
import pygame_gui
import sys
import math
import json

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MyInfiniteCanvas")

# Initialize pygame_gui
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Drawing settings
drawing = False
camera_x, camera_y = 0, 0
zoom = 0.01
brush_size = 5
current_color = BLACK

# Auto-zoom settings
auto_zoom = None
zoom_speed = 1.05  # Adjust this value to change zoom speed

# Color picker settings
show_color_picker = False
color_picker = None

# Data structure to store drawn points
# Key: (zoom_level, x, y), Value: color as tuple (r, g, b)
points = {}

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
    points[(zoom_level, round(x), round(y))] = current_color

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

    manager.draw_ui(screen)
    pygame.display.flip()

def save_drawing():
    data = {str(k): list(v) for k, v in points.items()}
    with open('drawing.json', 'w') as f:
        json.dump(data, f)
    print("Drawing saved!")

def load_drawing():
    global points
    try:
        with open('drawing.json', 'r') as f:
            data = json.load(f)
        points = {tuple(map(int, k[1:-1].split(','))): tuple(v) for k, v in data.items()}
        print("Drawing loaded!")
    except FileNotFoundError:
        print("No saved drawing found.")

def toggle_color_picker():
    global color_picker, show_color_picker
    if show_color_picker:
        if color_picker:
            color_picker.kill()
            color_picker = None
    else:
        color_picker = pygame_gui.windows.UIColourPickerDialog(
            rect=pygame.Rect(50, 50, 420, 400),
            manager=manager,
            initial_colour=pygame.Color(*current_color),
            visible=True
        )
    show_color_picker = not show_color_picker

# Main loop
clock = pygame.time.Clock()
while True:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                current_color = (event.colour.r, event.colour.g, event.colour.b)

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
            elif event.key == pygame.K_i:
                auto_zoom = 'in' if auto_zoom != 'in' else None
            elif event.key == pygame.K_o:
                auto_zoom = 'out' if auto_zoom != 'out' else None
            elif event.key == pygame.K_c:
                toggle_color_picker()

        manager.process_events(event)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= 10 / zoom
    if keys[pygame.K_RIGHT]:
        camera_x += 10 / zoom
    if keys[pygame.K_UP]:
        camera_y -= 10 / zoom
    if keys[pygame.K_DOWN]:
        camera_y += 10 / zoom

    # Apply auto-zoom
    if auto_zoom == 'in':
        zoom *= zoom_speed
    elif auto_zoom == 'out':
        zoom /= zoom_speed

    manager.update(time_delta)
    render()
