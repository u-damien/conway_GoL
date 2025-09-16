import pygame

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
CELL_SIZE = 5
BG_COLOR = (255, 255, 255)
CELL_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

black_cells = set()

def draw_grid():
    screen.fill(BG_COLOR)
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.rect(screen, (200, 200, 200), (x, y, CELL_SIZE, CELL_SIZE), 1)

def draw_cells():
    for pos_str in black_cells:
        x, y = map(int, pos_str.split(','))
        pygame.draw.rect(screen, CELL_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

def toggle_cell(pos, alive):
    x = (pos[0] // CELL_SIZE) * CELL_SIZE
    y = (pos[1] // CELL_SIZE) * CELL_SIZE
    pos_str = f"{x},{y}"

    if alive:
        if pos_str not in black_cells:
            black_cells.add(pos_str)
    else:
        if pos_str in black_cells:
            black_cells.remove(pos_str)
    
    # Redessine juste la cellule modifiée
    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    color = CELL_COLOR if alive else BG_COLOR
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (200, 200, 200), rect, 1) # Redessine le contour de la grille

def count_neighbors(x, y):
    count = 0
    for dx in [-CELL_SIZE, 0, CELL_SIZE]:
        for dy in [-CELL_SIZE, 0, CELL_SIZE]:
            if dx == 0 and dy == 0:
                continue
            
            neighbor_x, neighbor_y = x + dx, y + dy
            if f"{neighbor_x},{neighbor_y}" in black_cells:
                count += 1
    return count

def iterate():
    global black_cells
    new_black_cells = set()
    
    cells_to_evaluate = set(black_cells)
    for pos_str in black_cells:
        x, y = map(int, pos_str.split(','))
        for dx in [-CELL_SIZE, 0, CELL_SIZE]:
            for dy in [-CELL_SIZE, 0, CELL_SIZE]:
                cells_to_evaluate.add(f"{x + dx},{y + dy}")

    for pos_str in cells_to_evaluate:
        x, y = map(int, pos_str.split(','))
        neighbor_count = count_neighbors(x, y)
        
        if pos_str in black_cells:
            if neighbor_count == 2 or neighbor_count == 3:
                new_black_cells.add(pos_str)
        else:
            if neighbor_count == 3:
                new_black_cells.add(pos_str)
    

    black_cells = new_black_cells

def reset():
    global black_cells, iteration_status
    iteration_status = False
    black_cells.clear()
    draw_grid()

def redraw_game_window():
    if iteration_status:
        iterate()

        draw_grid()
        draw_cells()
    pygame.display.flip()

running = True
iteration_status = False
draw_grid()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                iteration_status = not iteration_status
            elif event.key == pygame.K_r:
                reset()
            elif event.key == pygame.K_i:
                if not iteration_status:
                    iterate()
            elif event.key == pygame.K_ESCAPE:
                exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not iteration_status:
                if event.button == 1: 
                    toggle_cell(event.pos, True)
                elif event.button == 3:
                    toggle_cell(event.pos, False)
    
    if pygame.mouse.get_pressed()[0] and not iteration_status:
        toggle_cell(pygame.mouse.get_pos(), True)
    elif pygame.mouse.get_pressed()[2] and not iteration_status:
        toggle_cell(pygame.mouse.get_pos(), False)

    redraw_game_window()

pygame.quit()
