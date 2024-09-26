# Example file showing a basic pygame "game loop"
import logging
import random
import pygame
import pygame.freetype
from board import Board
from shape import Shape

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

cell_colors = {
    "J": "pink",
    "L": "orange",
    "O": "yellow",
    "I": "cyan",
    "Z": "green",
    "S": "red",
    "T": "purple",
    " ": "black"
}

fall_delay = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]

def render_board(board: Board, shape: Shape, offset_x: int = 2, offset_y: int = 28, cell_size: int = 20, cell_border: int = 2):
    bare_grid = board.grid()
    for y, row in enumerate(board.grid(shape)):
        row_is_full = " " not in bare_grid[y]
        for x, cell in enumerate(row):
            cell_color = cell_colors[cell] if not row_is_full else "white"
            pygame.draw.rect(screen, cell_color, (x * cell_size + offset_x, y * cell_size + offset_y, cell_size - cell_border, cell_size - cell_border))

def render_text(text: str, x: int, y: int):
    game_font.render_to(screen, (x, y), text, "white")

# pygame setup
pygame.init()
screen = pygame.display.set_mode((10 * 20 + 2, 440))
pygame.display.set_caption("Tetris do Mau")
clock = pygame.time.Clock()
game_font = pygame.freetype.Font(None, 18)
running = True
board = Board()
mini_board = Board(4, 2)
shape = None
next_shapes = [Shape.create_random_shape() for _ in range(1)]

keys_monitored = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d, pygame.K_e, pygame.K_q]
prev_keys = pygame.key.get_pressed()

last_right = 0
last_left = 0
last_fall = 0
score = 0
current_frame = 0
total_lines_cleared = 0

while running:
    
    if shape is None:
        shape = next_shapes.pop(0).move(4, 0)
        next_shapes.append(Shape.create_random_shape())
        if board.is_topped_out(shape):
            # Game over
            running = False
            continue

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Detects new key presses
    curr_keys = pygame.key.get_pressed()
    new_keys = [key for key in keys_monitored if curr_keys[key] and not prev_keys[key]]
    prev_keys = curr_keys

    # Add moves to the list of moves to be executed according to the keys pressed
    moves = []
    curr_fall_delay = fall_delay[min(total_lines_cleared // 10, len(fall_delay) - 1)]
    if curr_keys[pygame.K_LEFT] or curr_keys[pygame.K_a]:
        if current_frame - last_left >= 6:
            moves.append(Shape.move_left)
            last_left = current_frame
    if curr_keys[pygame.K_RIGHT] or curr_keys[pygame.K_d]:
        if current_frame - last_right >= 6:
            moves.append(Shape.move_right)
            last_right = current_frame
    if curr_keys[pygame.K_DOWN] or curr_keys[pygame.K_s]:
        curr_fall_delay = min(2, curr_fall_delay)
    if pygame.K_e in new_keys:
        moves.append(Shape.rotate_clockwise)
    if pygame.K_q in new_keys:
        moves.append(Shape.rotate_counterclockwise)
    
    # Tries to move the shape according to the list of moves
    new_shape = shape
    for move in moves:
        new_shape = move(new_shape)
    if not board.is_colliding(new_shape):
        shape = new_shape        

    if current_frame - last_fall >= curr_fall_delay:
        if board.can_move(shape, 0, 1):
            shape = shape.move_down()
        else:
            board.fuse(shape)
            shape = None
        last_fall = current_frame

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray33")

    # RENDER YOUR GAME HERE
    render_board(board, shape)
    render_board(mini_board, next_shapes[0], 160, 4, 10, 1)
    render_text(f"Score: {score} | Level: {total_lines_cleared // 10}", 2, 8)

    lines_cleared = board.clear_lines()
    total_lines_cleared += lines_cleared
    score += lines_cleared ** 2

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    current_frame += 1

    # if board.is_colliding(shape):
    #     board.fuse(shape)
    #     shape = Shape.create_random_shape().move(4, 0)
    #     if board.is_topped_out(shape):
    #         # Game over
    #         running = False
    #     else:
    #         log.debug("New shape")
print("Game over")
clock.tick(1)
pygame.quit()
