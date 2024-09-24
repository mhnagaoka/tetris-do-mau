# Example file showing a basic pygame "game loop"
import logging
import random
import pygame
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

def render(board: Board, shape: Shape):
    bare_grid = board.grid()
    for y, row in enumerate(board.grid(shape)):
        row_is_full = " " not in bare_grid[y]
        for x, cell in enumerate(row):
            cell_color = cell_colors[cell] if not row_is_full else "white"
            pygame.draw.rect(screen, cell_color, (x * 20 + 1, y * 20 + 1, 18, 18))

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True
board = Board()
shape = Shape.create_random_shape().move(4, 0)

keys_monitored = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d, pygame.K_e, pygame.K_q]
prev_keys = pygame.key.get_pressed()

last_right = 0
last_left = 0
last_down = 0
last_fall = pygame.time.get_ticks()

while running:
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
    current_time = pygame.time.get_ticks()
    
    if curr_keys[pygame.K_LEFT] or curr_keys[pygame.K_a]:
        if current_time - last_left > 100:
            moves.append(Shape.move_left)
            last_left = current_time
    if curr_keys[pygame.K_RIGHT] or curr_keys[pygame.K_d]:
        if current_time - last_right > 100:
            moves.append(Shape.move_right)
            last_right = current_time
    if curr_keys[pygame.K_DOWN] or curr_keys[pygame.K_s]:
        if current_time - last_right > 200:
            moves.append(Shape.move_down)
            last_down = current_time
    # if pygame.K_LEFT in new_keys or pygame.K_a in new_keys:
    #     moves.append(Shape.move_left)
    # if pygame.K_RIGHT in new_keys or pygame.K_d in new_keys:
    #     moves.append(Shape.move_right)
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

    if current_time - last_fall > 1000:
        if board.can_move(shape, 0, 1):
            shape = shape.move_down()
        else:
            board.fuse(shape)
            shape = Shape.create_random_shape().move(4, 0)
            if board.is_topped_out(shape):
                # Game over
                running = False
        last_fall = current_time

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray33")

    # RENDER YOUR GAME HERE
    render(board, shape)

    board.clear_lines()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

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
