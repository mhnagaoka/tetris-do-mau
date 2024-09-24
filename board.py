import copy

from shape import Shape

class Board:

    def __init__(self, width = 10, height = 20):
        self.width = width
        self.height = height
        self._grid = self._empty_grid()
    
    def _empty_row(self) -> list[str]:
        return [" "] * self.width

    def _empty_grid(self) -> list[list[str]]:
        return [self._empty_row() for _ in range(self.height)]

    def grid(self, shape: Shape = None) -> list[list[str]]:
        new_grid = copy.deepcopy(self._grid)
        if shape:
            for y, row in enumerate(shape.grid):
                for x, cell in enumerate(row):
                    if cell != " ":
                        new_grid[y + shape.y][x + shape.x] = cell
        return new_grid

    def set_grid(self, new_grid: list[list[str]]):
        if len(new_grid) != self.height:
            raise ValueError("Invalid grid height")
        for row in new_grid:
            if len(row) != self.width:
                raise ValueError("Invalid grid width")
        self._grid = copy.deepcopy(new_grid)

    def is_colliding(self, shape: Shape):
        # Check if the shape is out of bounds
        if shape.y < 0 \
            or shape.x < 0 \
                or shape.x + len(shape.grid[0]) > self.width \
                    or shape.y + len(shape.grid) > self.height:
            return True
        # Check if the shape is colliding with the grid filled cells
        for y, row in enumerate(shape.grid):
            for x, cell in enumerate(row):
                if cell != " ":
                    if self._grid[y + shape.y][x + shape.x] != " ":
                        return True
        return False

    def can_move(self, shape: Shape, dx: int, dy: int):
        moved_shape = shape.move(dx, dy)
        return not self.is_colliding(moved_shape)

    def can_fall(self, shape: Shape):
        return self.can_move(shape, 0, 1)

    def fuse(self, shape: Shape):
        for y, row in enumerate(shape.grid):
            for x, cell in enumerate(row):
                if cell != " ":
                    self._grid[y + shape.y][x + shape.x] = cell

    def is_topped_out(self, new_shape: Shape):
        return self.is_colliding(new_shape)

    def clear_lines(self):
        new_grid = []
        for row in self._grid:
            if " " not in row:
                new_grid.insert(0, self._empty_row())
            else:
                new_grid.append(row)
        self._grid = new_grid
