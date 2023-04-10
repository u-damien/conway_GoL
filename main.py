import pygame

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BG_COLOR = (255, 255, 255)
screen.fill(BG_COLOR)
CELL_SIZE = 10


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
    # Clic gauche
    if pygame.mouse.get_pressed()[0]:
        fill_cell_black(pygame.mouse.get_pos())
    # Clic droit
    if pygame.mouse.get_pressed()[2]:
        fill_cell_white(pygame.mouse.get_pos())


def iterate():
    cells_to_kill = []
    cells_to_born = []
    for pos in all_cells:
        x, y = int(pos.split(',')[0]), int(pos.split(',')[1])
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
        # Comptage
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


# Boucle principale
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
