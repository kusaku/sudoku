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

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return self.row, self.col == other.row, other.col

    def __str__(self):
        s = ''
        if self.ready:
            s += '╔═══╗\n║ %d ║\n╚═══╝' % next(iter(self))
        elif self.empty:
            s = 'XXX\nXXX\nXXX'
        else:
            # s = '...\n...\n...'
            for i in range(1, 10):
                if i in self:
                    s += str(i)
                else:
                    s += '.'
                if i in {3, 6, 9}:
                    s += '\n'
                else:
                    s += ' '

        return s


class Uniques(list):
    def check(self):
        c = Counter(chain(*self))
        r = all(v == 1 for v in c.values())
        return r

    def naked_single(self):
        changed = False
        c = Counter(chain(*self))
        for v, count in c.items():
            if count == 1:
                for e in self:
                    if v in e:
                        e.difference_update(e - {v})
        return changed

    def hidden_single(self):
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

    def intersect(self, other):
        changed = False
        a = set(self)
        b = set(other)
        for v in set(chain(*(a & b))):
            c = {e for e in a | b if v in e}
            if c & a == c & a & b:
                for e in c - a:
                    e.difference_update({v})
                    changed = True
            if c & b == c & a & b:
                for e in c - b:
                    e.difference_update({v})
                    changed = True
        return changed


class Row(Uniques):
    def __str__(self):
        return tabulate([self], tablefmt="orgtbl")


class Col(Uniques):
    def __str__(self):
        return tabulate([[r] for r in self], tablefmt="orgtbl")


class Sec(Uniques):
    def __str__(self):
        return tabulate([[self[r * 3 + c] for c in range(3)] for r in range(3)], tablefmt="orgtbl")


class Board(list):
    def __init__(self):
        super().__init__([[Entry(row, col) for col in range(9)] for row in range(9)])

    def __str__(self):
        return tabulate(self, tablefmt="orgtbl")

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
                pass
                changed = self.sec(num).naked_single() or changed
                changed = self.sec(num).hidden_single() or changed
                changed = self.row(num).naked_single() or changed
                changed = self.row(num).hidden_single() or changed
                changed = self.col(num).naked_single() or changed
                changed = self.col(num).hidden_single() or changed

            for s in range(9):
                sec = self.sec(s)
                for num in range(s // 3 * 3, (s // 3 + 1) * 3):
                    changed = sec.intersect(self.row(num)) or changed
                for num in range(s % 3 * 3, (s % 3 + 1) * 3):
                    changed = sec.intersect(self.col(num)) or changed

    def solved(self):
        return all(e.ready for e in self.flat())

    def failed(self):
        return any(e.empty for e in self.flat())

    def check(self):
        return all(self.row(num).check() and self.col(num).check() and self.sec(num).check() for num in range(9))


def fill_test_board(q, b):
    print(sum(bool(e) for r in q for e in r), end=' ')
    for r in range(9):
        for c in range(9):
            if q[r][c]:
                b.update(r, c, q[r][c])


used = set((r, c) for c in range(3) for r in range(3))

iii = 0


def randomize_board(b):
    global iii
    s = b.sec(iii % 7 + 1)
    e = random.choice(s)
    v = random.choice(list(e))
    e.difference_update(e - {v})
    q[e.row][e.col] = v
    iii += 1


def simplify_q(q):
    for r in range(9):
        for c in range(9):
            v = q[r][c]
            if v == 0:
                continue
            try:
                q[r][c] = 0
                d = Board()
                fill_test_board(q, d)
                d.solve()
                if not d.solved():
                    raise Exception
            except:
                q[r][c] = v


flag = False

if __name__ == '__main__':

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

    b = Board()
    fill_test_board(q, b)
    b.solve()

    # print()
    # print(b.sec(6))
    # print(b.row(7))
    #
    # b.sec(6).intersect(b.row(7))
    #
    # print()
    # print(b.sec(6))
    # print(b.row(7))

    # # while not b.solved():
    # #     randomize_board(b)
    # #     b.solve()
    #
    # b.solve()
    #
    # simplify_q(q)

    e = Board()
    fill_test_board(q, e)

    print()
    print(b.solved(), b.check())
    print(tabulate([[str(e), '-->\n' * 27, str(b)]], tablefmt="plain"))
