import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

# Initial colors
BG_COLOR = [45, 151, 85]  # Background color in RGB
GROUND_COLOR = [33, 112, 63]  # Ground color in RGB
CUBE_COLOR = [255, 255, 255]  # Cube color in RGB

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cube Dash")

font = pygame.font.Font(None, 36)

player_pos = [100, 500]
player_size = [50, 50]
player_velocity = 5
is_jumping = False
jump_height = 10
gravity = 0.5
vertical_velocity = 0

fullscreen = False
camera_offset_x = 0
platforms = []
spikes = []
only_up_mode = False

PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_GAP = 150  # Gap between platforms

def generate_platforms():
    for x in range(0, SCREEN_WIDTH + 200, PLATFORM_WIDTH + 50):
        y = random.randint(2, 10) * PLATFORM_GAP
        platforms.append((x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))

def generate_spikes():
    for x in range(0, SCREEN_WIDTH + 200, 100):
        y = random.randint(2, 10) * PLATFORM_GAP
        spikes.append((x, y))

generate_platforms()
generate_spikes()

def show_menu():
    while True:
        screen.fill(BG_COLOR)
        title_text = font.render("Cube Dash", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        mouse_pos = pygame.mouse.get_pos()
        menu_options = ["Start Game", "Game Modes", "Options", "Exit"]
        for i, option in enumerate(menu_options):
            text = font.render(option, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 50))

            if text_rect.collidepoint(mouse_pos):
                text = pygame.transform.scale(text, (int(text.get_width() * 1.1), int(text.get_height() * 1.1)))
                if pygame.mouse.get_pressed()[0]:
                    return handle_menu_selection(i)
            screen.blit(text, text_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def handle_menu_selection(index):
    if index == 0:
        main_game()
    elif index == 1:
        game_modes_menu()
    elif index == 2:
        options_menu()
    elif index == 3:
        pygame.quit()
        sys.exit()

def game_modes_menu():
    global only_up_mode
    while True:
        screen.fill(BG_COLOR)
        title_text = font.render("Game Modes", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        mouse_pos = pygame.mouse.get_pos()
        text_only_up = font.render(f"ONLY UP: {'Enabled' if only_up_mode else 'Disabled'}", True, WHITE)
        text_back = font.render("Back", True, WHITE)

        screen.blit(text_only_up, (SCREEN_WIDTH // 2 - text_only_up.get_width() // 2, 150))
        screen.blit(text_back, (SCREEN_WIDTH // 2 - text_back.get_width() // 2, 200))

        if text_only_up.get_rect(center=(SCREEN_WIDTH // 2, 150)).collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            only_up_mode = not only_up_mode
        if text_back.get_rect(center=(SCREEN_WIDTH // 2, 200)).collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return  # Go back to the previous menu

        pygame.display.flip()

def options_menu():
    global fullscreen, BG_COLOR, GROUND_COLOR, CUBE_COLOR
    input_boxes = [pygame.Rect(250, 250, 50, 30), pygame.Rect(310, 250, 50, 30), pygame.Rect(370, 250, 30, 30),
                   pygame.Rect(250, 300, 50, 30), pygame.Rect(310, 300, 50, 30), pygame.Rect(370, 300, 30, 30),
                   pygame.Rect(250, 350, 50, 30), pygame.Rect(310, 350, 50, 30), pygame.Rect(370, 350, 30, 30)]
    color_values = [CUBE_COLOR, GROUND_COLOR, BG_COLOR]
    active_input = [False] * 9
    color_labels = ["Cube Color:", "GRND Color:", "BG Color:"]

    while True:
        screen.fill(BG_COLOR)
        title_text = font.render("Options", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        mouse_pos = pygame.mouse.get_pos()
        text_fullscreen = font.render(f"Fullscreen: {'On' if fullscreen else 'Off'}", True, WHITE)
        text_back = font.render("Back", True, WHITE)

        screen.blit(text_fullscreen, (SCREEN_WIDTH // 2 - text_fullscreen.get_width() // 2, 150))
        screen.blit(text_back, (SCREEN_WIDTH // 2 - text_back.get_width() // 2, 200))

        for i, label in enumerate(color_labels):
            label_text = font.render(label, True, WHITE)
            screen.blit(label_text, (100, 250 + i * 50))

        for i, rect in enumerate(input_boxes):
            if active_input[i]:
                color_input = font.render(str(color_values[i // 3][i % 3]), True, WHITE)
                screen.blit(color_input, (rect.x + 5, rect.y + 5))
            pygame.draw.rect(screen, WHITE, rect, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Go back to the previous menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_fullscreen.get_rect(center=(SCREEN_WIDTH // 2, 150)).collidepoint(mouse_pos):
                    toggle_fullscreen()
                elif text_back.get_rect(center=(SCREEN_WIDTH // 2, 200)).collidepoint(mouse_pos):
                    return  # Go back to the previous menu
                for i, rect in enumerate(input_boxes):
                    if rect.collidepoint(mouse_pos):
                        active_input[i] = not active_input[i]
                    else:
                        active_input[i] = False
            if event.type == pygame.KEYDOWN:
                for i, active in enumerate(active_input):
                    if active:
                        if event.unicode.isdigit() or event.unicode == "":
                            if event.unicode == "":
                                color_values[i // 3][i % 3] = 0  # Reset to zero if empty
                            else:
                                color_values[i // 3][i % 3] = min(255, int(event.unicode))
        
        # Update color values
        CUBE_COLOR = color_values[0]
        GROUND_COLOR = color_values[1]
        BG_COLOR = color_values[2]

        pygame.display.flip()

def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def check_platform_collision(player_rect):
    global is_jumping, vertical_velocity
    for x, y, w, h in platforms:
        platform_rect = pygame.Rect(x - camera_offset_x, y, w, h)
        if player_rect.colliderect(platform_rect) and vertical_velocity >= 0:
            player_pos[1] = platform_rect.top - player_size[1]
            is_jumping = False
            vertical_velocity = 0
            return

def generate_infinite_elements():
    # Generate platforms and spikes if needed
    if platforms and platforms[-1][0] - camera_offset_x < SCREEN_WIDTH:
        generate_platforms()
    if spikes and spikes[-1][0] - camera_offset_x < SCREEN_WIDTH:
        generate_spikes()

def main_game():
    global player_pos, is_jumping, vertical_velocity
    clock = pygame.time.Clock()
    player_pos = [100, 500]
    vertical_velocity = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return show_menu()
        if keys[pygame.K_a]:
            player_pos[0] -= player_velocity
        if keys[pygame.K_d]:
            player_pos[0] += player_velocity
        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and not is_jumping:
            is_jumping = True
            vertical_velocity = -jump_height

        if is_jumping:
            player_pos[1] += vertical_velocity
            vertical_velocity += gravity
            if player_pos[1] >= 500:
                player_pos[1] = 500
                is_jumping = False

        camera_offset_x = player_pos[0] - SCREEN_WIDTH // 2
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, GROUND_COLOR, (0 - camera_offset_x, 500, SCREEN_WIDTH, 100))

        # Display FPS
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
        screen.blit(fps_text, (10, 10))

        player_rect = pygame.Rect(player_pos[0] - camera_offset_x, player_pos[1], player_size[0], player_size[1])
        pygame.draw.rect(screen, CUBE_COLOR, player_rect)

        for x, y, w, h in platforms:
            platform_rect = pygame.Rect(x - camera_offset_x, y, w, h)
            pygame.draw.rect(screen, WHITE, platform_rect)

        check_platform_collision(player_rect)
        generate_infinite_elements()

        pygame.display.flip()
        clock.tick(FPS)

show_menu()
