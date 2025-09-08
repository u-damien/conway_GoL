"""
main.py
A simple implementation of Conway's Game of Life using Pygame. The program displays a grid where users can toggle cells between alive (black) and dead (white) states using mouse clicks. The simulation can be started, paused, reset, or advanced by one iteration using keyboard controls.
Modules:
    - pygame: Used for rendering the grid and handling user input.
Global Variables:
    - WINDOW_WIDTH (int): Width of the game window in pixels.
    - WINDOW_HEIGHT (int): Height of the game window in pixels.
    - CELL_SIZE (int): Size of each cell in the grid in pixels.
    - BG_COLOR (tuple): Background color of the grid.
    - screen (pygame.Surface): The main display surface.
    - all_cells (dict): Dictionary mapping cell positions to their pygame.Rect objects.
    - black_cells (dict): Dictionary mapping positions of alive cells to their pygame.Rect objects.
    - iteration_status (bool): Indicates whether the simulation is running.
Functions:
    - drawGrid(): Draws the initial grid and returns a dictionary of cell positions.
    - fill_cell_black(pos): Sets the cell at the given position to alive (black).
    - fill_cell_white(pos): Sets the cell at the given position to dead (white).
    - click_detection(): Handles mouse input for toggling cell states.
    - get_black_cells_neighbors(): Returns a list of all neighbor positions for alive cells.
    - iterate(): Advances the simulation by one generation according to Conway's Game of Life rules.
    - reset(): Resets the simulation, clearing all alive cells.
    - redraw_game_window(): Updates the display and advances the simulation if running.
Controls:
    - Left mouse button: Set cell to alive (black).
    - Right mouse button: Set cell to dead (white).
    - SPACE: Start or pause the simulation.
    - R: Reset the simulation.
    - I: Advance the simulation by one iteration.
    - ESC: Exit the program.
"""

import pygame 

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BG_COLOR = (255, 255, 255)
screen.fill(BG_COLOR)
CELL_SIZE = 5


def drawGrid():
    cells = {}
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            button = pygame.draw.rect(screen, "white", pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
            cells[f"{x},{y}"] = button
    return cells


all_cells = drawGrid()
black_cells = {}


def fill_cell_black(pos):
    x = pos[0] // CELL_SIZE * CELL_SIZE
    y = pos[1] // CELL_SIZE * CELL_SIZE
    try:
        cell = all_cells[f"{x},{y}"]
        rect = (cell.x, cell.y, CELL_SIZE, CELL_SIZE)
        screen.fill((0, 0, 0), rect)
        if not black_cells.get(f"{x},{y}"):
            black_cells[f"{x},{y}"] = cell
    except KeyError:
        pass


def fill_cell_white(pos):
    x = pos[0] // CELL_SIZE * CELL_SIZE
    y = pos[1] // CELL_SIZE * CELL_SIZE
    try:
        cell = all_cells[f"{x},{y}"]
        rect = (cell.x, cell.y, CELL_SIZE, CELL_SIZE)
        screen.fill((255, 255, 255), rect)
        del black_cells[f"{x},{y}"]
    except KeyError:
        pass


def click_detection():
    # Left click
    if pygame.mouse.get_pressed()[0]:
        fill_cell_black(pygame.mouse.get_pos())
    # Right click
    if pygame.mouse.get_pressed()[2]:
        fill_cell_white(pygame.mouse.get_pos())

def get_black_cells_neighbors():
    """
    Returns a list of neighboring cell positions for all black cells.
    Iterates over the global `black_cells` collection, where each cell position is represented as a string in the format "x,y".
    For each black cell, computes the positions of its eight immediate neighbors based on the global `CELL_SIZE` value.
    Returns a list of tuples, each representing the (x, y) coordinates of a neighboring cell.
    Returns:
        list of tuple: A list containing the (x, y) positions of all neighbors of the black cells.
    """
    
    neighbor_positions = []
    for pos in black_cells:
        x, y = int(pos.split(',')[0]), int(pos.split(',')[1])
        neighbor_positions += [
            (x - CELL_SIZE, y - CELL_SIZE),
            (x, y - CELL_SIZE),
            (x + CELL_SIZE, y - CELL_SIZE),
            (x - CELL_SIZE, y),
            (x + CELL_SIZE, y),
            (x - CELL_SIZE, y + CELL_SIZE),
            (x, y + CELL_SIZE),
            (x + CELL_SIZE, y + CELL_SIZE)
        ]
    return neighbor_positions


def iterate():
    """
    Advances the state of the Game of Life by one iteration.
    This function evaluates all relevant cells (currently alive and their neighbors)
    to determine which cells should die or be born in the next generation, according to Conway's Game of Life rules:
        - Any live cell with fewer than two or more than three live neighbors dies.
        - Any dead cell with exactly three live neighbors becomes alive.
    The function updates the grid by calling `fill_cell_white` for cells that should die and `fill_cell_black` for cells that should be born.
    Assumes the existence of:
        - `black_cells`: a dictionary mapping cell positions to their state.
        - `CELL_SIZE`: the size of each cell.
        - `get_black_cells_neighbors()`: a function returning positions of all relevant cells.
        - `fill_cell_white(cell)`: a function to set a cell to dead.
        - `fill_cell_black(cell)`: a function to set a cell to alive.
    """

    cells_to_kill = []
    cells_to_born = []
    black_cells_neighbors = get_black_cells_neighbors()
    for pos in black_cells_neighbors:
        x, y = int(pos[0]), int(pos[1])
        # Détection voisinnage
        neighbor_cells = [
            black_cells.get(f"{x - CELL_SIZE},{y - CELL_SIZE}"),
            black_cells.get(f"{x},{y - CELL_SIZE}"),
            black_cells.get(f"{x + CELL_SIZE},{y - CELL_SIZE}"),
            black_cells.get(f"{x - CELL_SIZE},{y}"),
            black_cells.get(f"{x + CELL_SIZE},{y}"),
            black_cells.get(f"{x - CELL_SIZE},{y + CELL_SIZE}"),
            black_cells.get(f"{x},{y + CELL_SIZE}"),
            black_cells.get(f"{x + CELL_SIZE},{y + CELL_SIZE}")
        ]
        # Counting neighbors
        i = 0
        for neighbor in neighbor_cells:
            if neighbor:
                i += 1

        if black_cells.get(f"{x},{y}"):
            if (i < 2) or (i > 3):
                if (x, y) not in cells_to_kill:
                    cells_to_kill.append((x, y))
        else:
            if i == 3:
                if (x, y) not in cells_to_born:
                    cells_to_born.append((x, y))
    for cell in cells_to_kill:
        fill_cell_white(cell)
    for cell in cells_to_born:
        fill_cell_black(cell)


def reset():
    global iteration_status, black_cells
    if iteration_status:
        iteration_status = False
    black_cells = {}
    screen.fill((255, 255, 255))


def redraw_game_window():
    if iteration_status:
        iterate()
    pygame.display.flip()


running = True
iteration_status = False
while running:
    events = pygame.event.get()
    pressed = pygame.key.get_pressed()

    if not iteration_status:
        click_detection()
    for ev in events:
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                iteration_status = not iteration_status
            if ev.key == pygame.K_r:
                reset()
            if ev.key == pygame.K_i:
                if iteration_status:
                    iteration_status = False
                iterate()

    if pressed[pygame.K_ESCAPE]:
        running = False
    redraw_game_window()
