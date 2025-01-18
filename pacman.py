import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 10

# Fonts
font = pygame.font.Font(None, 36)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")


# Player (Pac-Man) class
class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)
        self.score = 0

    def move(self, grid):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and grid[new_y][new_x] != 1:  # Check walls
            self.x = new_x
            self.y = new_y

    def draw(self):
        pygame.draw.circle(
            screen, YELLOW, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2
        )


# Ghost class
class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def move(self, grid):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]

        if 0 <= new_x < COLS and 0 <= new_y < ROWS and grid[new_y][new_x] != 1:  # Check walls
            self.x = new_x
            self.y = new_y
        else:  # Change direction randomly on collision
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def draw(self):
        pygame.draw.circle(
            screen, self.color, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2
        )


# Helper function to draw the grid
def draw_grid(grid):
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] == 1:  # Wall
                pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif grid[y][x] == 2:  # Pellet
                pygame.draw.circle(
                    screen, WHITE, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 6
                )
            elif grid[y][x] == 3:  # Power-up
                pygame.draw.circle(
                    screen, GREEN, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3
                )


# Generate a simple grid (1 = wall, 0 = empty, 2 = pellet, 3 = power-up)
def generate_grid():
    grid = [[0] * COLS for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLS):
            if x == 0 or y == 0 or x == COLS - 1 or y == ROWS - 1 or random.random() < 0.1:
                grid[y][x] = 1  # Walls
            elif random.random() < 0.02:
                grid[y][x] = 3  # Power-ups
            else:
                grid[y][x] = 2  # Pellets
    return grid


# Main game loop
def main():
    grid = generate_grid()
    pacman = PacMan(COLS // 2, ROWS // 2)
    ghosts = [
        Ghost(random.randint(1, COLS - 2), random.randint(1, ROWS - 2), RED),
        Ghost(random.randint(1, COLS - 2), random.randint(1, ROWS - 2), BLUE),
    ]

    running = True
    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    pacman.direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    pacman.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    pacman.direction = (1, 0)

        # Move Pac-Man
        pacman.move(grid)

        # Check for collisions with pellets or power-ups
        if grid[pacman.y][pacman.x] == 2:  # Pellet
            pacman.score += 10
            grid[pacman.y][pacman.x] = 0
        elif grid[pacman.y][pacman.x] == 3:  # Power-up
            pacman.score += 50
            grid[pacman.y][pacman.x] = 0

        # Move ghosts
        for ghost in ghosts:
            ghost.move(grid)
            # Check for collision with Pac-Man
            if ghost.x == pacman.x and ghost.y == pacman.y:
                running = False  # Game over

        # Draw everything
        draw_grid(grid)
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()

        # Display score
        score_text = font.render(f"Score: {pacman.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    # Game Over screen
    screen.fill(BLACK)
    game_over_text = font.render("Game Over! Press any key to exit.", True, WHITE)
    final_score_text = font.render(f"Final Score: {pacman.score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()

