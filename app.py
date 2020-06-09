import operator
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
        return (self.row, self.col, self.box) == (other.row, other.col, other.box)

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

    def solved(self):
        return all(e.ready for e in self)

    def failed(self):
        return any(e.empty for e in self)

    def check(self):
        c = Counter(chain(*self))
        return all(v == self.RANK for v in c.values())


class Solver:
    def solve_naked_tuples(brd):
        changed = False
        loop_changed = True
        while loop_changed:
            loop_changed = False
            for num in range(brd.RANK):
                loop_changed |= brd.box(num).naked_tuples()
                loop_changed |= brd.row(num).naked_tuples()
                loop_changed |= brd.col(num).naked_tuples()
            changed |= loop_changed
        return changed

    def solve_hidden_tuples(brd):
        changed = False
        loop_changed = True
        while loop_changed:
            loop_changed = False
            for num in range(brd.RANK):
                loop_changed |= brd.box(num).hidden_tuples()
                loop_changed |= brd.row(num).hidden_tuples()
                loop_changed |= brd.col(num).hidden_tuples()
            changed |= loop_changed
        return changed

    def solve_intersections(brr):
        changed = False
        loop_changed = True
        while loop_changed:
            loop_changed = False
            for b in range(brr.RANK):
                box = brr.box(b)
                for num in {e.row for e in box}:
                    loop_changed |= box.intersections(brr.row(num))
                for num in {e.col for e in box}:
                    loop_changed |= box.intersections(brr.col(num))
            changed |= loop_changed
        return changed

    def solve_x_wing(brd):
        changed = False
        f = lambda items: {
            v: set(e for e in items if v in e)
            for v, count in Counter(chain(*items)).items()
            if count == 2
        }
        for num1 in range(brd.RANK - 1):
            row1 = f(brd.row(num1))
            col1 = f(brd.col(num1))
            for num2 in range(num1 + 1, brd.RANK):
                row2 = f(brd.row(num2))
                col2 = f(brd.col(num2))
                for v in row1.keys() & row2.keys():
                    cols = {e.col for e in row1[v]} & {e.col for e in row2[v]}
                    if len(cols) == 2:
                        for c in cols:
                            for e in brd.col(c) - row1[v] - row2[v]:
                                changed |= e.exclude({v})
                for v in col1.keys() & col2.keys():
                    rows = {e.row for e in col1[v]} & {e.row for e in col2[v]}
                    if len(rows) == 2:
                        for r in rows:
                            for e in brd.row(r) - col1[v] - col2[v]:
                                changed |= e.exclude({v})
        return changed

    def solve_swordfish(brd):
        changed = False
        f = lambda items: {
            v: set(e for e in items if v in e)
            for v, count in Counter(chain(*items)).items()
            if count in {2, 3}
        }
        for num1 in range(brd.RANK - 2):
            row1 = f(brd.row(num1))
            col1 = f(brd.col(num1))
            for num2 in range(num1 + 1, brd.RANK - 1):
                row2 = f(brd.row(num2))
                col2 = f(brd.col(num2))
                for num3 in range(num2 + 1, brd.RANK):
                    row3 = f(brd.row(num3))
                    col3 = f(brd.col(num3))
                    for v in row1.keys() & row2.keys() & row3.keys():
                        cols = {e.col for e in row1[v]} | {e.col for e in row2[v]} | {e.col for e in row3[v]}
                        if len(cols) in {2, 3}:
                            for c in cols:
                                for e in brd.col(c) - row1[v] - row2[v] - row3[v]:
                                    changed |= e.exclude({v})
                    for v in col1.keys() & col2.keys() & col3.keys():
                        rows = {e.row for e in col1[v]} | {e.row for e in col2[v]} | {e.row for e in col3[v]}
                        if len(rows) in {2, 3}:
                            for r in rows:
                                for e in brd.row(r) - col1[v] - col2[v] - col3[v]:
                                    changed |= e.exclude({v})
        return changed

    def solve_xy_wing(brd):
        changed = False
        es = {e for e in brd if len(e) == 2}
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
                        e2cells = brd.row(e2.row) | brd.col(e2.col) | brd.box(e2.box)
                        e3cells = brd.row(e3.row) | brd.col(e3.col) | brd.box(e3.box)
                        for e in e2cells & e3cells - {e2, e3}:
                            changed |= e.exclude(v)
        return changed

    def solve_xyz_wing(brd):
        changed = False
        graph = defaultdict(set)
        for e1 in (e for e in brd if len(e) == 3):
            for e2 in (e for e in brd if len(e) == 2):
                if len(e1 & e2) == 2 and (e1.row == e2.row or e1.col == e2.col or e1.box == e2.box):
                    graph[e1].add(e2)
        for e1, es in graph.items():
            seen = set()
            for e2 in es:
                seen.add(e2)
                for e3 in es - seen:
                    v = e2 & e3
                    if len(v) == 1 and len(e1 | v) == 3:
                        e1cells = brd.row(e1.row) | brd.col(e1.col) | brd.box(e1.box)
                        e2cells = brd.row(e2.row) | brd.col(e2.col) | brd.box(e2.box)
                        e3cells = brd.row(e3.row) | brd.col(e3.col) | brd.box(e3.box)
                        for e in e1cells & e2cells & e3cells - {e1, e2, e3}:
                            changed |= e.exclude(v)
        return changed

    def solve_coloring(brd):
        changed = False
        # unsolved = {e for e in self if not e.ready}
        unsolved = {e for e in brd}
        vs = set(chain(*unsolved))
        for v in vs:
            es = {e for e in unsolved if v in e}

            def bilocation(e1, e2):
                if e1 == e2:
                    return False
                if e1.row == e2.row:
                    return {e1, e2} == es & brd.row(e1.row)
                if e1.col == e2.col:
                    return {e1, e2} == es & brd.col(e1.col)
                if e1.box == e2.box:
                    return {e1, e2} == es & brd.box(e1.box)

            graph = defaultdict(set)
            for e1 in es:
                for e2 in es:
                    if bilocation(e1, e2):
                        graph[e1].add(e2)
                        graph[e2].add(e1)
            seen = set()
            while graph.keys() - seen:
                a, b = set(), set()
                e = next(iter(graph.keys() - seen))
                stack = [(a, b, e)]
                while stack:
                    a, b, e = stack.pop()
                    if e in a | b:
                        continue
                    a.add(e)
                    if e in graph:
                        stack.extend((b, a, e) for e in graph[e])
                # rule 4
                for e1 in a:
                    for e2 in b:
                        e1cells = brd.row(e1.row) | brd.col(e1.col) | brd.box(e1.box)
                        e2cells = brd.row(e2.row) | brd.col(e2.col) | brd.box(e2.box)
                        for e in es & e1cells & e2cells - a - b:
                            changed |= e.exclude({v})
                seen |= a | b
                # rule 2
                for side in (a, b):
                    if {len(side)} != set(map(len, map(set, zip(*((e.row, e.col, e.box) for e in side))))):
                        for e in side:
                            changed |= e.exclude({v})
        return changed

    NAKED_TUPLES = 1
    HIDDEN_TUPLES = 2
    INTERSECTIONS = 3
    XWING = 4
    XYWING = 5
    XYZWING = 6
    SWORDFISH = 7
    COLORING = 8

    STRATEGIES = {
        NAKED_TUPLES: solve_naked_tuples,
        HIDDEN_TUPLES: solve_hidden_tuples,
        INTERSECTIONS: solve_intersections,
        XWING: solve_x_wing,
        XYWING: solve_xy_wing,
        XYZWING: solve_xyz_wing,
        SWORDFISH: solve_swordfish,
        COLORING: solve_coloring,
    }

    @classmethod
    def solve(cls, brd, strategies=None):
        if strategies is None:
            strategies = cls.STRATEGIES.keys()
        changed = True
        while changed:
            changed = False

            for strategy in strategies:
                solve_method = cls.STRATEGIES[strategy]
                changed |= solve_method(brd)
