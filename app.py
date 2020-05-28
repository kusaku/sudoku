import operator
import random
from collections import Counter, defaultdict
from functools import reduce
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
        return self.row, self.col, self.box == other.row, other.col, other.box

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


class Unit(Atom):

    def check(self):
        c = Counter(chain(*self))
        return all(v == 1 for v in c.values())

    def naked_tuples(self):
        changed = False
        c = Counter(map(tuple, self))  # noqa - tuple(set(...))
        for v, count in c.items():
            if count == len(v):
                vs = set(v)
                for e in self:
                    if e != vs:
                        changed |= e.exclude(vs)
        return changed

    def hidden_tuples(self):
        changed = False
        c = Counter(chain(*self))
        d = defaultdict(dict)
        for v, count in c.items():
            d[count][v] = {e for e in self if v in e}
        for count, vs in d.items():
            if count == 1:
                for v, es in vs.items():
                    for e in es:
                        changed |= e.intersect({v})
            elif count == len(vs):
                a = reduce(operator.or_, vs.values())
                b = reduce(operator.and_, vs.values())
                c = set(chain(*a))
                if c != vs.keys() and a == b:
                    for e in a:
                        ch = e.intersect(vs.keys())
                        changed |= ch
        return changed

    def intersections(self, other):
        changed = False
        for v in set(chain(*(self & other))):
            c = {e for e in self | other if v in e}
            if c & self == c & self & other:
                for e in c - self:
                    changed |= e.exclude({v})
            if c & other == c & self & other:
                for e in c - other:
                    changed |= e.exclude({v})
        return changed


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
    NAKED_TUPLES = 1
    HIDDEN_TUPLES = 2
    INTERSECTIONS = 3
    XWING = 4
    XYWING = 5
    XYZWING = 6
    SWORDFISH = 7

    def __init__(self, initial=None):
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

    def solve_naked_tuples(self):
        changed = False
        loop_changed = True
        while loop_changed:
            loop_changed = False
            for num in range(self.RANK):
                loop_changed |= self.box(num).naked_tuples()
                loop_changed |= self.row(num).naked_tuples()
                loop_changed |= self.col(num).naked_tuples()
            changed |= loop_changed
        return changed

    def solve_hidden_tuples(self):
        changed = False
        loop_changed = True
        while loop_changed:
            loop_changed = False
            for num in range(self.RANK):
                loop_changed |= self.box(num).hidden_tuples()
                loop_changed |= self.row(num).hidden_tuples()
                loop_changed |= self.col(num).hidden_tuples()
            changed |= loop_changed
        return changed

    def solve_intersections(self):
        changed = False
        loop_changed = True
        while loop_changed:
            loop_changed = False
            for b in range(self.RANK):
                box = self.box(b)
                for num in {e.row for e in box}:
                    loop_changed |= box.intersections(self.row(num))
                for num in {e.col for e in box}:
                    loop_changed |= box.intersections(self.col(num))
            changed |= loop_changed
        return changed

    def solve_x_wing(self):
        changed = False
        f = lambda items: {
            v: set(e for e in items if v in e)
            for v, count in Counter(chain(*items)).items()
            if count == 2
        }
        for num1 in range(self.RANK - 1):
            row1 = f(self.row(num1))
            col1 = f(self.col(num1))
            for num2 in range(num1 + 1, self.RANK):
                row2 = f(self.row(num2))
                col2 = f(self.col(num2))
                for v in row1.keys() & row2.keys():
                    cols = {e.col for e in row1[v]} & {e.col for e in row2[v]}
                    if len(cols) == 2:
                        for c in cols:
                            for e in self.col(c) - row1[v] - row2[v]:
                                changed |= e.exclude({v})
                for v in col1.keys() & col2.keys():
                    rows = {e.row for e in col1[v]} & {e.row for e in col2[v]}
                    if len(rows) == 2:
                        for r in rows:
                            for e in self.row(r) - col1[v] - col2[v]:
                                changed |= e.exclude({v})
        return changed

    def solve_swordfish(self):
        changed = False
        f = lambda items: {
            v: set(e for e in items if v in e)
            for v, count in Counter(chain(*items)).items()
            if count in {2, 3}
        }
        for num1 in range(self.RANK - 2):
            row1 = f(self.row(num1))
            col1 = f(self.col(num1))
            for num2 in range(num1 + 1, self.RANK - 1):
                row2 = f(self.row(num2))
                col2 = f(self.col(num2))
                for num3 in range(num2 + 1, self.RANK):
                    row3 = f(self.row(num3))
                    col3 = f(self.col(num3))
                    for v in row1.keys() & row2.keys() & row3.keys():
                        cols = {e.col for e in row1[v]} | {e.col for e in row2[v]} | {e.col for e in row3[v]}
                        if len(cols) in {2, 3}:
                            for c in cols:
                                for e in self.col(c) - row1[v] - row2[v] - row3[v]:
                                    changed |= e.exclude({v})
                    for v in col1.keys() & col2.keys() & col3.keys():
                        rows = {e.row for e in col1[v]} | {e.row for e in col2[v]} | {e.row for e in col3[v]}
                        if len(rows) in {2, 3}:
                            for r in rows:
                                for e in self.row(r) - col1[v] - col2[v] - col3[v]:
                                    changed |= e.exclude({v})
        return changed

    def solve_xy_wing(self):
        changed = False
        es = {e for e in self if len(e) == 2}
        graph = defaultdict(set)
        for e1 in es:
            for e2 in es:
                if len(e1 & e2) == 1 and (e1.row == e2.row or e1.col == e2.col or e1.box == e2.box):
                    graph[e1].add(e2)
        for e1, es in graph.items():
            seen = set()
            for e2 in es:
                seen.add(e2)
                for e3 in es - seen:
                    v = e2 & e3
                    if len(v) == 1 and len(e1 & v) == 0 and e2.row != e3.row and e2.col != e3.col and e2.box != e3.box:
                        # print({0}<-{1}->{2}.format(
                        #     {0} at [{1},{2}][{3}].format(tuple(e2), e2.row, e2.col, e2.box),
                        #     {0} at [{1},{2}][{3}].format(tuple(e1), e1.row, e1.col, e1.box),
                        #     {0} at [{1},{2}][{3}].format(tuple(e3), e3.row, e3.col, e3.box),
                        # ))
                        e2cells = self.row(e2.row) | self.col(e2.col) | self.box(e2.box)
                        e3cells = self.row(e3.row) | self.col(e3.col) | self.box(e3.box)
                        for e in e2cells & e3cells - {e2, e3}:
                            # print(excluding {0} from {1} because it is on intersection of {2} and {3}.format(
                            #     v,
                            #     [{1}, {2}][{3}].format(tuple(e), e.row, e.col, e.box),
                            #     {0} at [{1},{2}][{3}].format(tuple(e2), e2.row, e2.col, e2.box),
                            #     {0} at [{1},{2}][{3}].format(tuple(e3), e3.row, e3.col, e3.box)
                            # ))
                            changed |= e.exclude(v)
        return changed

    def solve_xyz_wing(self):
        changed = False
        graph = defaultdict(set)
        for e1 in (e for e in self if len(e) == 3):
            for e2 in (e for e in self if len(e) == 2):
                if len(e1 & e2) == 2 and (e1.row == e2.row or e1.col == e2.col or e1.box == e2.box):
                    graph[e1].add(e2)
        for e1, es in graph.items():
            seen = set()
            for e2 in es:
                seen.add(e2)
                for e3 in es - seen:
                    v = e2 & e3
                    if len(v) == 1 and len(e1 | v) == 3:
                        # print({0}<-{1}->{2}.format(
                        #     {0} at [{1},{2}][{3}].format(tuple(e2), e2.row, e2.col, e2.box),
                        #     {0} at [{1},{2}][{3}].format(tuple(e1), e1.row, e1.col, e1.box),
                        #     {0} at [{1},{2}][{3}].format(tuple(e3), e3.row, e3.col, e3.box),
                        # ))
                        e1cells = self.row(e1.row) | self.col(e1.col) | self.box(e1.box)
                        e2cells = self.row(e2.row) | self.col(e2.col) | self.box(e2.box)
                        e3cells = self.row(e3.row) | self.col(e3.col) | self.box(e3.box)
                        for e in e1cells & e2cells & e3cells - {e1, e2, e3}:
                            # print(excluding {0} from {1} because it is on intersection of {2} and {3}.format(
                            #     v,
                            #     [{1}, {2}][{3}].format(tuple(e), e.row, e.col, e.box),
                            #     {0} at [{1},{2}][{3}].format(tuple(e2), e2.row, e2.col, e2.box),
                            #     {0} at [{1},{2}][{3}].format(tuple(e3), e3.row, e3.col, e3.box)
                            # ))
                            changed |= e.exclude(v)
        return changed

    def solve(self, strategies=None):
        if strategies is None:
            strategies = {self.NAKED_TUPLES, self.HIDDEN_TUPLES, self.INTERSECTIONS, self.XWING, self.XYWING,
                          self.XYZWING, self.SWORDFISH}
        changed = True
        while changed:
            changed = False

            if self.NAKED_TUPLES in strategies and not changed:
                changed |= self.solve_naked_tuples()

            if self.HIDDEN_TUPLES in strategies and not changed:
                changed |= self.solve_hidden_tuples()

            if self.INTERSECTIONS in strategies and not changed:
                changed |= self.solve_intersections()

            if self.XWING in strategies and not changed:
                changed |= self.solve_x_wing()

            if self.XYWING in strategies and not changed:
                changed |= self.solve_xy_wing()

            if self.XYZWING in strategies and not changed:
                changed |= self.solve_xyz_wing()

            if self.SWORDFISH in strategies and not changed:
                changed |= self.solve_swordfish()

    def solved(self):
        return all(e.ready for e in self)

    def failed(self):
        return any(e.empty for e in self)

    def check(self):
        c = Counter(chain(*self))
        return all(v == self.RANK for v in c.values())


def simplify_q(q):
    for r in range(9):
        for c in range(9):
            v = q[r][c]
            if v == 0:
                continue
            try:
                q[r][c] = 0
                d = Board.from_array(q)
                d.solve()
                if not d.solved():
                    raise Exception
            except:
                q[r][c] = v


flag = False

if __name__ == '__main__':

    b = Board()
    q = b.to_array()


    def randomize_board(q, b):
        # n = random.choice([0, 1, 2, 3, 5, 6, 7, 8])
        # s = b.row(n)
        try:
            e = random.choice([e for e in b if not e.ready])
            v = random.choice(list(e))
        except:
            print(e)
            # print(v)
            raise
        e.intersect({v})
        q[e.row][e.col] = v


    while not b.solved():
        randomize_board(q, b)
        # print(b)
        b.solve(strategies={Board.HIDDEN_TUPLES})

    # b = Board.from_array([
    #     [1, 0, 0, 6, 0, 2, 0, 7, 0],
    #     [2, 6, 0, 9, 0, 0, 1, 0, 0],
    #     [0, 0, 7, 0, 0, 0, 0, 0, 0],
    #     [0, 8, 0, 4, 0, 0, 0, 0, 7],
    #     [0, 7, 1, 3, 0, 8, 2, 5, 0],
    #     [9, 0, 0, 0, 0, 7, 0, 1, 0],
    #     [0, 0, 0, 0, 0, 0, 4, 0, 0],
    #     [0, 0, 4, 0, 0, 6, 0, 2, 3],
    #     [0, 2, 0, 1, 0, 4, 0, 0, 6],
    # ])
    #
    # print(b)
    # b.solve()
    # print(repr(b.to_string()))
    # print(b.solved(), b.check())
    #
    # print(b)
    # print(repr(b.to_string()))
    # print(b.solved(), b.check())
    #
    # b = Board.from_string(   5 fe    a 4 7  3     9c4g  d  f    6g3d152 ab a b2  d6 fec g3      f7 b      3d7  1   ga4b6 f  a g528 9c6ed 1  9 3 b6    4 2c  de ba      3   34c   fge  62  g2 f5  1   87 ea      3   9c      f2    a      d8 63  1   2     c9 db  5e        4    d   7f  8 )
    # b.solve(True)
    # print(b)

    # # X-wing & XY-wing
    # q = [
    #     [1, 0, 0, 6, 0, 2, 0, 7, 0],
    #     [2, 6, 0, 9, 0, 0, 1, 0, 0],
    #     [0, 0, 7, 0, 0, 0, 0, 0, 0],
    #     [0, 8, 0, 4, 0, 0, 0, 0, 7],
    #     [0, 7, 1, 3, 0, 8, 2, 5, 0],
    #     [9, 0, 0, 0, 0, 7, 0, 1, 0],
    #     [0, 0, 0, 0, 0, 0, 4, 0, 0],
    #     [0, 0, 4, 0, 0, 6, 0, 2, 3],
    #     [0, 2, 0, 1, 0, 4, 0, 0, 6],
    # ]
    #
    # a = Board.from_array(q)
    # b = Board.from_array(q)
    #
    # b.solve()
    #
    # # while not b.solved():
    # #     randomize_board(b)
    # #     b.solve()
    #
    # # simplify_q(q)
    #
    # print(b.solved(), b.check())
    # print(tabulate([[a, -->\n * 27, b]], tablefmt='plain'))
    #
    # print(repr(a.to_string()))
    # print(repr(b.to_string()))
