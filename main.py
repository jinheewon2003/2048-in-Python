import pygame
import random

# Constants
GRID_SIZE = 4
TILE_SIZE = 100
PADDING = 10
SCREEN_WIDTH = GRID_SIZE * (TILE_SIZE + PADDING) + PADDING
SCREEN_HEIGHT = SCREEN_WIDTH
FONT_SIZE = 36
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048")
font = pygame.font.SysFont(None, FONT_SIZE)

# Function to draw a tile
def draw_tile(x, y, value):
    color = (255, 255, 255)
    if value != 0:
        color = (187, 173, 160)  # Adjust color as needed
    pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
    if value != 0:
        text = font.render(str(value), True, BLACK)
        text_rect = text.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
        screen.blit(text, text_rect)

# Function to initialize the grid
def initialize_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(grid)
    add_new_tile(grid)
    return grid

# Function to add a new tile (2 or 4) to a random empty cell
def add_new_tile(grid):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])

# Function to merge tiles in a row or column
def merge(row):
    merged = [False] * GRID_SIZE
    for i in range(GRID_SIZE - 1):
        if row[i] == row[i + 1] and not merged[i]:
            row[i] *= 2
            row[i + 1] = 0
            merged[i] = True
    return row

# Function to move tiles in a row or column
def move(row):
    new_row = [cell for cell in row if cell != 0] + [0] * row.count(0)
    return new_row

# Function to handle movement in a specific direction
def move_grid(grid, direction):
    if direction == pygame.K_LEFT:
        for i in range(GRID_SIZE):
            row = move(grid[i])
            merged_row = merge(row)
            grid[i] = merged_row
    elif direction == pygame.K_RIGHT:
        for i in range(GRID_SIZE):
            row = move(grid[i][::-1])[::-1]
            merged_row = merge(row[::-1])[::-1]
            grid[i] = merged_row
    elif direction == pygame.K_UP:
        transposed_grid = [[grid[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            row = move(transposed_grid[i])
            merged_row = merge(row)
            for j in range(GRID_SIZE):
                grid[j][i] = merged_row[j]
    elif direction == pygame.K_DOWN:
        transposed_grid = [[grid[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            row = move(transposed_grid[i][::-1])[::-1]
            merged_row = merge(row[::-1])[::-1]
            for j in range(GRID_SIZE):
                grid[j][i] = merged_row[j]
    
    return grid



# Function to check if the game is over
def is_game_over(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return False
            if j > 0 and grid[i][j] == grid[i][j - 1]:
                return False
            if i > 0 and grid[i][j] == grid[i - 1][j]:
                return False
    return True

# Main game loop
def main():
    grid = initialize_grid()
    running = True

    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    old_grid = [row[:] for row in grid] 
                    grid = move_grid(grid, event.key)
                    if grid != old_grid:
                        add_new_tile(grid)


        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                draw_tile(j * (TILE_SIZE + PADDING) + PADDING, i * (TILE_SIZE + PADDING) + PADDING, grid[i][j])

        pygame.display.flip()

        if is_game_over(grid):
            print("Game Over!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()


# NEED TO ADD ANIMATIONS AND COLORS