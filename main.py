import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 540, 540
CELL_SIZE = SCREEN_WIDTH // 9
GRID_SIZE = 9
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku Solver")

# Colours
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
TRANSPARENT_YELLOW = (255, 255, 0, 50)


# Sudoku grid
def draw_grid():
    SCREEN.fill(BLACK)
    for i in range(GRID_SIZE + 1):
        color = LIGHT_GRAY
        pygame.draw.line(SCREEN, color, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT))
        pygame.draw.line(SCREEN, color, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE))


# numbers on the grid
def grid_numbers(grid, font):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != 0:
                num = font.render(str(grid[row][col]), True, WHITE)
                x = col * CELL_SIZE + CELL_SIZE // 3
                y = row * CELL_SIZE + CELL_SIZE // 3
                SCREEN.blit(num, (x, y))


def is_possible(grid, row, column, number):
    for i in range(GRID_SIZE):
        if grid[row][i] == number:
            return False

    for i in range(GRID_SIZE):
        if grid[i][column] == number:
            return False

    x0 = (column // 3) * 3
    y0 = (row // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[y0 + i][x0 + j] == number:
                return False

    return True


def highlight_cell(row, col):
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    pygame.draw.rect(SCREEN, TRANSPARENT_YELLOW, (x, y, CELL_SIZE, CELL_SIZE))


def display_message(message, font):
    message_text = font.render(message, True, WHITE)
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(message_text, message_rect)
    pygame.display.update()




# solve the Sudoku
def solve(grid):
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            if grid[row][column] == 0:
                for number in range(1, 10):
                    if is_possible(grid, row, column, number):
                        grid[row][column] = number
                        if solve(grid):
                            return grid
                        grid[row][column] = 0

                return None

    return grid



def main():
    # empty grid
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    font = pygame.font.Font(None, 36)

    selected_cell = None

    # loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    if selected_cell is not None:
                        row, col = selected_cell
                        grid[row][col] = event.key - pygame.K_0
                elif event.key == pygame.K_RETURN:
                    solved_grid = solve(
                        [row[:] for row in grid])
                    if solved_grid:
                        grid = solved_grid
                        display_message("Solved!", font)
                        selected_cell = None  # stop highlighting

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # highlight the cell
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = mouse_y // CELL_SIZE
                col = mouse_x // CELL_SIZE
                selected_cell = (row, col)

        # grid and numbers
        draw_grid()
        grid_numbers(grid, font)

        if selected_cell is not None:
            highlight_cell(*selected_cell)

        pygame.display.update()


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
