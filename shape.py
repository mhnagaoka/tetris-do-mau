from __future__ import annotations
import random

class Shape:

    @staticmethod
    def create_j() -> Shape:
        return Shape([
            ["J", " ", " "],
            ["J", "J", "J"],
        ])


    @staticmethod
    def create_l() -> Shape:
        return Shape([
            ["L", "L", "L"],
            ["L", " ", " "],
        ])

    @staticmethod
    def create_o() -> Shape:
        return Shape([
            ["O", "O"],
            ["O", "O"],
        ])

    @staticmethod
    def create_i() -> Shape:
        return Shape([
            ["I", "I", "I", "I"],
        ])

    @staticmethod
    def create_z() -> Shape:
        return Shape([
            ["Z", "Z", " "],
            [" ", "Z", "Z"],
        ])

    @staticmethod
    def create_s() -> Shape:
        return Shape([
            [" ", "S", "S"],
            ["S", "S", " "],
        ])

    @staticmethod
    def create_t() -> Shape:
        return Shape([
            ["T", "T", "T"],
            [" ", "T", " "],
        ])

    @staticmethod
    def create_shape(shape: str) -> Shape:
        return _creators[shape.lower()]()

    @staticmethod
    def create_random_shape() -> Shape:
        return random.choice(list(_creators.values()))()

    def __init__(self, grid: list[list[str]], x:int = 0, y:int = 0):
        self._grid = grid
        self.x = x
        self.y = y

    def __str__(self):
        return f"Shape at ({self.x}, {self.y})"

    # getter
    @property
    def grid(self):
        return self._grid

    def rotate_clockwise(self) -> Shape:
        return Shape([list(row) for row in zip(*self._grid[::-1])], self.x, self.y)

    def rotate_counterclockwise(self) -> Shape:
        return Shape([list(row) for row in zip(*self._grid)][::-1], self.x, self.y)
    
    def move(self, dx: int, dy: int) -> Shape:
        return Shape(self._grid, self.x + dx, self.y + dy)


_creators = {
    "j": Shape.create_j,
    "l": Shape.create_l,
    "o": Shape.create_o,
    "i": Shape.create_i,
    "z": Shape.create_z,
    "s": Shape.create_s,
    "t": Shape.create_t,
}
