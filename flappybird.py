import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Bird properties
bird_width, bird_height = 40, 40
bird_x = 50
bird_y = HEIGHT // 2 - bird_height // 2
bird_jump = -10
bird_gravity = 0.5

# Pipe properties
pipe_width = 70
pipe_gap = 150
pipe_speed = 4
pipes = []

# Score
score = 0
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)

# Functions
def draw_bird(x, y):
    pygame.draw.rect(win, BLACK, (x, y, bird_width, bird_height))

def draw_pipe(x, gap_start, gap_size):
    pygame.draw.rect(win, BLACK, (x, 0, pipe_width, gap_start))
    pygame.draw.rect(win, BLACK, (x, gap_start + gap_size, pipe_width, HEIGHT - gap_start - gap_size))

def collision(pipe):
    if bird_x + bird_width > pipe[0] and bird_x < pipe[0] + pipe_width:
        if bird_y < pipe[1] or bird_y + bird_height > pipe[1] + pipe_gap:
            return True
    return False

def show_end_screen():
    win.fill(WHITE)
    score_text = font.render(f"Score: {score}", True, BLACK)
    restart_text = small_font.render("Press SPACE to restart", True, RED)
    win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 50))
    win.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    
def reset_game():
    global bird_y, pipes, score
    bird_y = HEIGHT // 2 - bird_height // 2
    pipes = []
    score = 0

# Game loop
clock = pygame.time.Clock()
running = True
game_active = True

while running:
    clock.tick(30)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_y += bird_jump
                else:
                    game_active = True
                    reset_game()
                    
    if game_active:
        # Move bird
        bird_y += bird_gravity
        
        # Generate pipes
        if len(pipes) == 0 or pipes[-1][0] < WIDTH - 200:
            gap_start = random.randint(50, HEIGHT - pipe_gap - 50)
            pipes.append((WIDTH, gap_start, pipe_gap))

        # Move pipes
        for i, pipe in enumerate(pipes):
            pipes[i] = (pipe[0] - pipe_speed, pipe[1], pipe[2])

            # Remove pipes that have passed
            if pipe[0] + pipe_width < 0:
                pipes.pop(i)
                score += 1

        # Check for collisions
        for pipe in pipes:
            if collision(pipe):
                game_active = False
                break

        # Draw everything
        win.fill(WHITE)
        draw_bird(bird_x, bird_y)
        for pipe in pipes:
            draw_pipe(pipe[0], pipe[1], pipe[2])
        text = font.render(str(score), True, BLACK)
        win.blit(text, (10, 10))
    else:
        show_end_screen()

    pygame.display.update()

# Quit pygame
pygame.quit()
