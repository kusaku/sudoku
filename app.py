import random
from collections import Counter, defaultdict
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
    def check(self):
        c = Counter(chain(*self))
        r = all(v == 1 for v in c.values())
        return r

    def single(self):
        changed = False
        c = Counter(chain(*self))
        for v, count in c.items():
            if count == 1:
                for e in self:
                    if v in e:
                        e.difference_update(e - {v})

        if flag:
            self.double()

        return changed

    def double(self):
        changed = False
        d = defaultdict(set)
        for v in chain(*self):
            for i, e in enumerate(self):
                if v in e:
                    d[v].add(i)

        id = defaultdict(set)

        for k, v in d.items():
            id[tuple(sorted(v))].add(k)

        for k, v in id.items():
            if len(k) > 1 and len(k) == len(v):
                ...

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


class Sec(Uniques):
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

    def sec(self, num):
        row = num // 3
        col = num % 3
        return Sec(self[r][c] for r in range(row * 3, (row + 1) * 3) for c in range(col * 3, (col + 1) * 3))

    def flat(self):
        return [self[r][c] for c in range(9) for r in range(9)]

    def solve(self):
        changed = True
        while changed:
            changed = False
            for num in range(9):
                changed = self.sec(num).single() or changed
                changed = self.sec(num).unique() or changed
                changed = self.row(num).single() or changed
                changed = self.row(num).unique() or changed
                changed = self.col(num).single() or changed
                changed = self.col(num).unique() or changed

    def solved(self):
        return all(e.ready for e in self.flat())

    def failed(self):
        return any(e.empty for e in self.flat())

    def check(self):
        return all(self.row(num).check() and self.col(num).check() and self.sec(num).check() for num in range(9))


def fill_test_board(q, b):
    print(sum(bool(e) for r in q for e in r))
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
    s = b.sec((iii // 3) % 3, iii % 3)
    e = random.choice(s)
    v = random.choice(list(e))
    e.difference_update(e - {v})
    q[e.row][e.col] = v
    iii += 1


flag = False

if __name__ == '__main__':
    # e = [entry(k) for k in range(1, 10)]

    b = Board()

    q = [
        [0, 4, 0, 0, 0, 2, 6, 0, 0],
        [8, 0, 0, 9, 3, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 1, 0, 0, 0],
        [0, 6, 9, 0, 0, 0, 7, 0, 1],
        [4, 0, 0, 0, 0, 0, 0, 0, 2],
        [7, 0, 8, 0, 0, 0, 5, 4, 0],
        [0, 0, 0, 6, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 1, 9, 0, 0, 4],
        [0, 0, 3, 2, 0, 0, 0, 9, 0],
    ]

    fill_test_board(q, b)

    # print(b.check())

    b.solve()

    flag = True

    b.solve()

    print(b.check())

    # while not (b.solved() or b.failed()):
    #     randomize_board(b)
    #     b.solve()

    c = Board()

    fill_test_board(q, c)

    print(tabulate([[str(c), '-->\n' * 27, str(b)]], tablefmt="plain"))
