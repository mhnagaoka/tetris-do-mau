import pytest
import logging

from board import Board
from shape import Shape

log = logging.getLogger(__name__)

def print_grid(grid):
    for row in grid:
        line = ""
        for cell in row:
            # line += "⬜" if cell != " " else "⬛"
            line += cell if cell != " " else "."
        log.debug(line)

class TestBoard:

    @pytest.fixture
    def board(self) -> Board:
        return Board(6, 7) 
   
    def test_grid_should_be_empty(self, board: Board):
        expected = [
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
        ]
        assert board.grid(None) == expected
    
    def test_grid_with_a_shape(self, board: Board):
        shape = Shape.create_j()
        expected = [
            ["J", " ", " ", " ", " ", " "],
            ["J", "J", "J", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
        ]
        assert board.grid(shape) == expected

    def test_fuse_shape_on_empty_board(self, board: Board):
        shape = Shape.create_j()
        board.fuse(shape)
        expected = [
            ["J", " ", " ", " ", " ", " "],
            ["J", "J", "J", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
        ]
        assert board.grid(None) == expected


    def test_fuse_shape_on_non_empty_board(self, board: Board):
        base = [
            [" ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
        ]
        board.set_grid(base)
        shape = Shape.create_t()
        board.fuse(shape)
        expected = [
            ["T", "T", "T", " ", " ", " "],
            ["X", "T", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
        ]
        assert board.grid(None) == expected

    def test_set_grid(self, board: Board):
        base = [
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            ["X", "X", "X", "X", "X", "X"],
        ]
        board.set_grid(base)
        assert board.grid(None) == base

    def test_should_fall_from_top_of_empty_grid(self, board: Board):
        shape = Shape.create_j()
        assert board.can_fall(shape)

    def test_should_not_fall_from_bottom_of_empty_grid(self, board: Board):
        shape = Shape.create_j()
        shape.y = board.height - len(shape.grid)
        assert not board.can_fall(shape)

    def test_should_fall_if_not_colliding(self, caplog, board: Board):
        base = [
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", "X", "X"],
        ]
        board.set_grid(base)
        shape = Shape.create_j()
        shape.y = board.height - len(shape.grid) - 1
        assert board.can_fall(shape)

    def test_should_fall_if_not_colliding_2(self, caplog, board: Board):
        base = [
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
        ]
        board.set_grid(base)
        shape = Shape.create_j()
        shape = shape.rotate_clockwise()
        shape = shape.rotate_clockwise()
        shape.y = board.height - len(shape.grid) - 1
        print_grid(board.grid(shape))
        assert board.can_fall(shape)

    def test_should_not_fall_if_colliding(self, caplog, board: Board):
        base = [
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            ["X", "X", "X", "X", "X", "X"],
        ]
        board.set_grid(base)
        shape = Shape.create_j()
        shape.y = board.height - len(shape.grid) - 1
        assert not board.can_fall(shape)

    def test_should_not_fall_if_colliding_a_single_cell(self, caplog, board: Board):
        base = [
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
        ]
        board.set_grid(base)
        shape = Shape.create_j()
        shape.y = board.height - len(shape.grid) - 1
        assert not board.can_fall(shape)


    def test_should_not_fall_if_colliding_a_single_cell_2(self, caplog, board: Board):
        base = [
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", "X", " ", " ", " "],
        ]
        board.set_grid(base)
        shape = Shape.create_j()
        shape = shape.rotate_clockwise()
        shape = shape.rotate_clockwise()
        shape.y = board.height - len(shape.grid) - 1
        assert not board.can_fall(shape)
    
    def test_could_move_right_if_not_out_of_bounds(self, board: Board):
        shape = Shape.create_j()
        assert board.can_move(shape, 1, 0)

    def test_could_not_move_right_if_out_of_bounds(self, board: Board):
        shape = Shape.create_j()
        shape.x = board.width - len(shape.grid[0])
        assert not board.can_move(shape, 1, 0)

    def test_could_not_move_right_if_colliding(self, board: Board):
        base = [
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "X", " ", " "],
            [" ", " ", " ", "X", " ", " "],
            [" ", " ", " ", "X", " ", " "],
            [" ", " ", " ", "X", " ", " "],
            [" ", " ", " ", "X", " ", " "],
            [" ", " ", " ", "X", " ", " "],
        ]
        board.set_grid(base)
        shape = Shape.create_j()
        assert not board.can_move(shape, 1, 0)

    def test_could_move_left_if_not_out_of_bounds(self, board: Board):
        shape = Shape.create_j()
        shape.x = 1
        assert board.can_move(shape, -1, 0)
    
    def test_could_not_move_left_if_out_of_bounds(self, board: Board):
        shape = Shape.create_j()
        assert not board.can_move(shape, -1, 0)
    
    def test_could_not_move_left_if_colliding(self, board: Board):
        base = [
            [" ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " "],
        ]
        board.set_grid(base)    
        shape = Shape.create_j()
        shape.x = 1
        assert not board.can_move(shape, -1, 0)
