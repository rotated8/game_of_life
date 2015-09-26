from __future__ import unicode_literals, print_function
from collections import defaultdict, namedtuple
from itertools import product

Offset = namedtuple('Offset', ('x', 'y'))
_neighbor_offsets = {Offset(*offset) for offset in product(range(-1,2), range(-1,2))} - {Offset(0,0)}

class Game:
    def __init__(self, living_cells = None):
        self._top = self._left = self._right = self._bottom = None
        self.board = defaultdict(set)

        if living_cells is not None:
            for x, y in living_cells:
                self.add_cell(x, y)

    def __repr__(self):
        living_cells = []
        for x, column in self.board.items():
            for y in column:
                living_cells.append([x, y])

        return 'Game({})'.format(living_cells)

    def __str__(self):
        board = []
        top = max(1, self._top + 1)
        left = min(0, self._left)
        right = max(1, self._right + 1)
        bottom = min(0, self._bottom)

        for y in range(bottom, top):
            row = []
            for x in range(left, right):
                if y in self.board[x]:
                    row.append('X')
                elif x == 0:
                    if y == 0:
                        row.append('+')
                    else:
                        row.append('|')
                else:
                    row.append('-')
            row.append('\n')
            board.insert(0, ''.join(row))
        return ''.join(board)


    def add_cell(self, x, y):
        self.board[x].add(y)

        if self._left is None or x < self._left:
            self._left = x
        if self._right is None or x > self._right:
            self._right = x
        if self._top is None or y > self._top:
            self._top = y
        if self._bottom is None or y < self._bottom:
            self._bottom = y

    def update(self):
        unchecked_cells = set()
        new_game = Game()

        for x, column in self.board.items():
            for y in column:
                for offset in _neighbor_offsets.union({Offset(0,0)}):
                    unchecked_cells.add((x + offset.x, y + offset.y))

        for x, y in unchecked_cells:
            living_neighbors = self.count_living_neighbors(x, y)
            if (living_neighbors == 3) or (living_neighbors == 2 and y in self.board[x]):
                new_game.add_cell(x, y)

        self.__dict__ = new_game.__dict__

    def count_living_neighbors(self, x, y):
        count = 0

        for offset in _neighbor_offsets:
            if y + offset.y in self.board[x + offset.x]:
                count += 1

        return count

if __name__ == '__main__':
    g = Game([[0,0], [2,1], [2,2], [3,1], [3,2]])
    print(g)
    g.update()
    print(g)
    g.update()
    print(g)
