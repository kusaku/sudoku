import random
from collections import Counter
from itertools import chain

from tabulate import tabulate


class Entry(set):
    def __init__(self, row, col, value=None):
        self.row = row
        self.col = col
        if value is None:
            return super().__init__([1, 2, 3, 4, 5, 6, 7, 8, 9])
        else:
            return super().__init__([value])

    @property
    def ready(self):
        return len(self) == 1

    @property
    def empty(self):
        return len(self) == 0

    def __str__(self):
        s = ''
        if self.ready:
            s += '╔═╗\n║%d║\n╚═╝' % next(iter(self))
        elif self.empty:
            s = 'XXX\nXXX\nXXX'
        else:
            for i in range(1, 10):
                if i in self:
                    s += str(i)
                else:
                    s += '.'
                if i in {3, 6, 9}:
                    s += '\n'

        return s


class Uniques(list):
    def single(self):
        changed = False
        c = Counter(chain(*self))
        for v, count in c.items():
            if count == 1:
                for e in self:
                    if v in e:
                        e.difference_update(e - {v})
        return changed

    def unique(self):
        changed = False
        c = Counter(map(tuple, self))
        for v, count in c.items():
            if count == len(v):
                s = set(v)
                for e in self:
                    if e != s and s.issubset(e):
                        e.difference_update(s)
                        changed = True
        return changed


class Row(Uniques):
    def __str__(self):
        return tabulate([self], tablefmt="plain")


class Col(Uniques):
    def __str__(self):
        return tabulate([[r] for r in self], tablefmt="plain")


class Sector(Uniques):
    def __str__(self):
        return tabulate([[self[r * 3 + c] for c in range(3)] for r in range(3)], tablefmt="plain")


class Board(list):
    def __init__(self):
        super().__init__([[Entry(row, col) for col in range(9)] for row in range(9)])

    def __str__(self):
        return tabulate(self, tablefmt="plain")

    def update(self, row, col, value):
        self[row][col] = Entry(row, col, value)

    def row(self, num):
        return Row(self[num])

    def col(self, num):
        return Col(r[num] for r in self)

    def sector(self, row, col):
        l = []
        for r in range(row * 3, (row + 1) * 3):
            for c in range(col * 3, (col + 1) * 3):
                l.append(self[r][c])
        return Sector(l)

    def flat(self):
        return [self[r][c] for c in range(9) for r in range(9)]

    def solve(self):
        changed = True
        while changed:
            changed = False
            for row in range(9):
                changed = self.row(row).single() or changed
                changed = self.row(row).unique() or changed
            for col in range(9):
                changed = self.col(col).single() or changed
                changed = self.col(col).unique() or changed
            for row in range(3):
                for col in range(3):
                    changed = self.sector(row, col).single() or changed
                    changed = self.sector(row, col).unique() or changed

    def solved(self):
        return all(e.ready for e in self.flat())

    def failed(self):
        return any(e.empty for e in self.flat())


def fill_test_board(q, b):
    for r in range(9):
        for c in range(9):
            if q[r][c]:
                b.update(r, c, q[r][c])


used = set((r, c) for c in range(3) for r in range(3))

q = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

iii = 0

def randomize_board(b):
    global iii
    s = b.sector((iii//3)%3, iii%3)
    e = random.choice(s)
    v = random.choice(list(e))
    e.difference_update(e - {v})
    q[e.row][e.col] = v
    iii += 1


if __name__ == '__main__':
    # e = [entry(k) for k in range(1, 10)]

    b = Board()

    q = [
        [0, 0, 0, 0, 0, 0, 3, 0, 2],
        [0, 0, 0, 7, 3, 0, 0, 4, 0],
        [8, 0, 0, 5, 0, 0, 7, 0, 0],
        [0, 0, 4, 0, 9, 0, 0, 0, 5],
        [2, 0, 0, 0, 0, 0, 0, 0, 4],
        [3, 0, 0, 0, 8, 0, 6, 0, 0],
        [0, 0, 7, 0, 0, 6, 0, 0, 9],
        [0, 3, 0, 0, 4, 9, 0, 0, 0],
        [5, 0, 6, 0, 0, 0, 0, 0, 0],
    ]
    fill_test_board(q, b)

    b.solve()

    # while not (b.solved() or b.failed()):
    #     randomize_board(b)
    #     b.solve()

    print(sum(bool(e) for r in q for e in r))

    c = Board()

    fill_test_board(q, c)

    print(tabulate([[str(c), '-->' ,str(b)]], tablefmt="plain"))
