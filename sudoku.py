from collections import Counter, defaultdict
from itertools import chain

from tabulate import tabulate


class Atom(set):
    ORDER = 3
    RANK = ORDER ** 2


class Element(Atom):
    VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, row, col, box, initial=None):
        self.row = row
        self.col = col
        self.box = box
        if initial is None:
            super().__init__(self.VALUES)
        else:
            super().__init__(initial)

    @property
    def ready(self):
        return len(self) == 1

    @property
    def empty(self):
        return len(self) == 0

    def exclude(self, values):
        if set(self) != self.difference(values):
            self.difference_update(values)
            return True
        return False

    def intersect(self, values):
        if set(self) != self.intersection(values):
            self.intersection_update(values)
            return True
        return False

    def __hash__(self):
        return hash((self.row, self.col, self.box))

    def __eq__(self, other):
        return (self.row, self.col, self.box) == (other.row, other.col, other.box)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        s = ''
        if self.ready:
            s += '╔═══╗\n║ %s ║\n╚═══╝' % next(iter(self))
        elif self.empty:
            s = 'X X X\nX X X\nX X X'
        else:
            # s = '...\n...\n...'
            for i, v in enumerate(self.VALUES):
                if v in self:
                    s += str(v)
                else:
                    s += '.'
                if (i + 1) % self.ORDER == 0:
                    s += '\n'
                else:
                    s += ' '

        return s

    def __repr__(self):
        return 'Element(%d, %d, %d)' % (self.row, self.col, self.box)


class Unit(Atom):

    def check(self):
        c = Counter(chain(*self))
        return all(v == 1 for v in c.values())


class Row(Unit):

    def __str__(self):
        table = sorted(self, key=lambda e: e.col)
        return tabulate([table], tablefmt='orgtbl')


class Col(Unit):

    def __str__(self):
        table = sorted(self, key=lambda e: e.row)
        return tabulate([[e] for e in table], tablefmt='orgtbl')


class Box(Unit):

    def __str__(self):
        table = sorted(self, key=lambda e: e.row * self.RANK + e.col)
        return tabulate([[table[r * self.ORDER + c] for c in range(self.ORDER)] for r in range(3)], tablefmt='orgtbl')


class Board(Atom):
    def __init__(self, initial=None):
        super().__init__()
        self.rows = defaultdict(set)
        self.cols = defaultdict(set)
        self.boxs = defaultdict(set)
        for r in range(self.RANK):
            for c in range(self.RANK):
                box = r // self.ORDER * self.ORDER + c // self.ORDER
                e = Element(r, c, box, None if initial is None else initial[r][c])
                self.rows[r].add(e)
                self.cols[c].add(e)
                self.boxs[box].add(e)
                self.add(e)

    @classmethod
    def from_array(cls, q):
        initial = []
        for r in range(cls.RANK):
            row = []
            for c in range(cls.RANK):
                v = q[r][c]
                if v in Element.VALUES:
                    v = {v}
                elif type(v) is set:
                    v = set(v)
                else:
                    v = None
                row.append(v)
            initial.append(row)
        return Board(initial)

    def to_array(self):
        return [
            [
                next(iter(e)) if e.ready else 0
                for e in sorted(self.rows[r], key=lambda e: e.col)
            ]
            for r in range(self.RANK)
        ]

    @classmethod
    def from_string(self, q):
        initial = []
        for r in range(self.RANK):
            row = []
            for c in range(self.RANK):
                v = int(q[r * self.RANK + c])
                if v in Element.VALUES:
                    v = {v}
                else:
                    v = None
                row.append(v)
            initial.append(row)
        return Board(initial)

    def to_string(self):
        return ''.join(
            str(next(iter(e))) if e.ready else ' '
            for e in sorted(self, key=lambda e: e.row * self.RANK + e.col)
        )

    def __str__(self):
        return tabulate([[str(self.row(r))] for r in range(self.RANK)], tablefmt='plain')

    def get(self, row=None, col=None, box=None):
        es = set(self)
        if row is not None:
            es &= self.rows[row]
        if col is not None:
            es &= self.cols[col]
        if box is not None:
            es &= self.boxs[box]
        return es

    def update(self, v, row=None, col=None, box=None):
        for e in self.get(row, col, box):
            e.clear()
            e.add(v)

    def row(self, num):
        return Row(self.rows[num])

    def col(self, num):
        return Col(self.cols[num])

    def box(self, num):
        return Box(self.boxs[num])

    def solved(self):
        return all(e.ready for e in self)

    def check(self):
        c = Counter(chain(*self))
        return all(v == self.RANK for v in c.values())
