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
    for y, row in enumerate(board.grid(shape)):
        for x, cell in enumerate(row):
            pygame.draw.rect(screen, cell_colors[cell], (x * 20 + 1, y * 20 + 1, 18, 18))

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True
board = Board()
moves = [
    Shape.rotate_clockwise,
    Shape.rotate_counterclockwise,
    Shape.move_left,
    Shape.move_right,
    Shape.move_down,
    None
]
shape = Shape.create_random_shape().move(4, 0)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    new_shape = None
    random_move = random.choice(moves)
    if random_move:
        new_shape = random_move(shape)
        if not board.is_colliding(new_shape):
            shape = new_shape

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray33")

    # RENDER YOUR GAME HERE
    render(board, shape)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(5)  # limits FPS to 60

    moved_shape = shape.move(0, 1)
    if not board.is_colliding(moved_shape):
        shape = moved_shape
    else:
        board.fuse(shape)
        shape = Shape.create_random_shape().move(4, 0)
        if board.is_topped_out(shape):
            # Game over
            running = False
        else:
            log.debug("New shape")
print("Game over")
clock.tick(1)
pygame.quit()
