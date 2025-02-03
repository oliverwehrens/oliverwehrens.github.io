import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_img = pygame.image.load('bird.png').convert_alpha()
pipe_img = pygame.image.load('pipe.png').convert_alpha()
background_img = pygame.image.load('background.png').convert_alpha()

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Game variables
gravity = 0.5
bird_jump = -5
pipe_speed = 3
gap_height = 150

# Bird class
class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 2
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.velocity = 0

    def jump(self):
        self.velocity = bird_jump

    def update(self):
        self.velocity += gravity
        self.y += self.velocity
        self.rect.y = self.y

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.top = self.height - 300
        self.bottom = self.height + gap_height
        self.passed = False
        self.top_pipe = pygame.Rect(self.x, 0, 60, self.height)
        self.bottom_pipe = pygame.Rect(self.x, self.bottom, 60, SCREEN_HEIGHT - self.bottom)

    def update(self):
        self.x -= pipe_speed
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x

# Score
def display_score(score):
    font = pygame.font.SysFont('Arial', 30)
    text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (10, 10))

# Game loop
def main():
    bird = Bird()
    pipes = []
    score = 0
    running = True

    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Bird update
        bird.update()

        # Spawn pipes
        if len(pipes) < 4:
            pipes.append(Pipe())

        # Update pipes
        for pipe in pipes[:]:
            pipe.update()
            if pipe.x < -60:
                pipes.remove(pipe)
            if bird.x > pipe.x and not pipe.passed:
                pipe.passed = True
                score += 1

        # Collision detection
        for pipe in pipes:
            if bird.rect.colliderect(pipe.top_pipe) or bird.rect.colliderect(pipe.bottom_pipe):
                running = False
        if bird.y < 0 or bird.y > SCREEN_HEIGHT:
            running = False

        # Draw everything
        screen.blit(background_img, (0, 0))
        screen.blit(bird_img, (bird.x, bird.y))
        for pipe in pipes:
            screen.blit(pipe_img, (pipe.x, pipe.top))
            screen.blit(pipe_img, (pipe.x, pipe.bottom))
        display_score(score)
        pygame.display.update()

        # Game over
        if not running:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont('Arial', 40)
            text = font.render(f'Game Over! Score: {score}', True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 20))
            pygame.display.update()
            pygame.time.wait(2000)

if __name__ == '__main__':
    main()
