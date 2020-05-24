import operator
import random
from collections import Counter, defaultdict
from functools import reduce
from itertools import chain

from tabulate import tabulate


class Entry(set):
    def __init__(self, row, col, value=None):
        self.row = row
        self.col = col
        self.sec = row // 3 * 3 + col // 3
        if value is None:
            super().__init__([1, 2, 3, 4, 5, 6, 7, 8, 9])
        else:
            super().__init__([value])

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
        return hash((self.row, self.col))

    def __eq__(self, other):
        return self.row, self.col == other.row, other.col

    def __str__(self):
        s = ''
        if self.ready:
            s += '╔═══╗\n║ %d ║\n╚═══╝' % next(iter(self))
        elif self.empty:
            s = 'X X X\nX X X\nX X X'
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
        return all(v == 1 for v in c.values())

    def naked_tuples(self):
        changed = False
        c = Counter(map(tuple, self))
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
                        changed |= e.intersect(vs.keys())
        return changed

    def intersect(self, other):
        changed = False
        a = set(self)
        b = set(other)
        for v in set(chain(*(a & b))):
            c = {e for e in a | b if v in e}
            if c & a == c & a & b:
                for e in c - a:
                    changed |= e.exclude({v})
            if c & b == c & a & b:
                for e in c - b:
                    changed = e.exclude({v})
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
        return [self[r][c] for r in range(9) for c in range(9)]

    def solve_naked_tuples(self):
        changed = False
        loop_changed = True
        while loop_changed:
            for num in range(9):
                loop_changed = False
                loop_changed |= self.sec(num).naked_tuples()
                loop_changed |= self.row(num).naked_tuples()
                loop_changed |= self.col(num).naked_tuples()
            changed |= loop_changed
        return changed

    def solve_hidden_tuples(self):
        changed = False
        loop_changed = True
        while loop_changed:
            loop_changed = False
            for num in range(9):
                loop_changed |= self.sec(num).hidden_tuples()
                loop_changed |= self.row(num).hidden_tuples()
                loop_changed |= self.col(num).hidden_tuples()
            changed |= loop_changed
        return changed

    def solve_pointing(self):
        changed = False
        loop_changed = True
        while loop_changed:
            loop_changed = False
            for s in range(9):
                sec = self.sec(s)
                for num in range(s // 3 * 3, (s // 3 + 1) * 3):
                    loop_changed |= sec.intersect(self.row(num))
                for num in range(s % 3 * 3, (s % 3 + 1) * 3):
                    loop_changed |= sec.intersect(self.col(num))
            changed |= loop_changed
        return changed

    def solve_x_wing(self):
        changed = False
        loop_changed = True
        while loop_changed:
            loop_changed = False
            f = lambda items: {
                v: set(e for e in items if v in e)
                for v, count in Counter(chain(*items)).items()
                if count == 2
            }
            for num1 in range(8):
                row1 = f(self.row(num1))
                col1 = f(self.col(num1))
                for num2 in range(num1 + 1, 9):
                    row2 = f(self.row(num2))
                    col2 = f(self.col(num2))
                    for v in row1.keys() & row2.keys():
                        cols = {e.col for e in row1[v]} & {e.col for e in row2[v]}
                        if len(cols) == 2:
                            for c in cols:
                                col = set(self.col(c))
                                for e in col - row1[v] - row2[v]:
                                    loop_changed |= e.exclude({v})
                    for v in col1.keys() & col2.keys():
                        rows = {e.row for e in col1[v]} & {e.row for e in col2[v]}
                        if len(rows) == 2:
                            for r in rows:
                                row = set(self.row(r))
                                for e in row - col1[v] - col2[v]:
                                    loop_changed |= e.exclude({v})
            changed |= loop_changed
        return changed

    def solve_xy_wing(self):
        changed = False
        loop_changed = True
        while loop_changed:
            loop_changed = False
            es = {e for e in self.flat() if len(e) == 2}
            graph = defaultdict(set)
            for e1 in es:
                for e2 in es:
                    if len(e1 & e2) == 1 and (e1.row == e2.row or e1.col == e2.col or e1.sec == e2.sec):
                        graph[e1].add(e2)


            for e1, es in graph.items():
                seen = set()
                for e2 in es:
                    seen.add(e2)
                    for e3 in es - seen:
                        v = e2 & e3
                        if len(v) == 1 and len(e1 & v) == 0 and e2.row != e3.row and e2.col != e3.col and e2.sec != e3.sec:
                            # print('{0}<-{1}->{2}'.format(
                            #     '{0} at [{1},{2}][{3}]'.format(tuple(e2), e2.row, e2.col, e2.sec),
                            #     '{0} at [{1},{2}][{3}]'.format(tuple(e1), e1.row, e1.col, e1.sec),
                            #     '{0} at [{1},{2}][{3}]'.format(tuple(e3), e3.row, e3.col, e3.sec),
                            # ))
                            e2cells = set(chain(self.row(e2.row), self.col(e2.col), self.sec(e2.sec)))
                            e3cells = set(chain(self.row(e3.row), self.col(e3.col), self.sec(e3.sec)))
                            for e in e2cells & e3cells - {e2, e3}:
                                # print('excluding {0} from {1} because it is on intersection of {2} and {3}'.format(
                                #     v,
                                #     '[{1}, {2}][{3}]'.format(tuple(e), e.row, e.col, e.sec),
                                #     '{0} at [{1},{2}][{3}]'.format(tuple(e2), e2.row, e2.col, e2.sec),
                                #     '{0} at [{1},{2}][{3}]'.format(tuple(e3), e3.row, e3.col, e3.sec)
                                # ))
                                loop_changed |= e.exclude(v)
            changed |= loop_changed
        return changed

    def solve(self):
        changed = True
        while changed:
            changed = False
            changed |= self.solve_naked_tuples()

            if changed:
                print('\nnaked_tuples changes:')
                print(b)

            if not changed:
                changed |= self.solve_hidden_tuples()
                if changed:
                    print('\nhidden_tuples changes:')
                    print(b)

            if not changed:
                changed |= self.solve_pointing()
                if changed:
                    print('\npointing changes:')
                    print(b)

            if not changed:
                changed |= self.solve_x_wing()
                if changed:
                    print('\nx wing changes:')
                    print(b)

            if not changed:
                changed |= self.solve_xy_wing()
                if changed:
                    print('\nxy wing changes:')
                    print(b)

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


def randomize_board(b):
    # n = random.choice([0, 1, 2, 3, 5, 6, 7, 8])
    # s = b.row(n)
    e = random.choice([e for e in b.flat() if not e.ready])
    v = random.choice(list(e))
    e.difference_update(e - {v})
    q[e.row][e.col] = v


def simplify_q(q):
    for r in range(8, -1, -1):
        for c in range(8, -1, -1):
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
        [1, 0, 0, 6, 0, 2, 0, 7, 0],
        [2, 6, 0, 9, 0, 0, 1, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 4, 0, 0, 0, 0, 7],
        [0, 7, 1, 3, 0, 8, 2, 5, 0],
        [9, 0, 0, 0, 0, 7, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 4, 0, 0],
        [0, 0, 4, 0, 0, 6, 0, 2, 3],
        [0, 2, 0, 1, 0, 4, 0, 0, 6],
    ]

    b = Board()
    fill_test_board(q, b)

    b.solve()

    # while not b.solved():
    #     randomize_board(b)
    #     b.solve()

    simplify_q(q)

    e = Board()
    fill_test_board(q, e)

    print()
    print(b.solved(), b.check())
    print(tabulate([[str(e), '-->\n' * 27, str(b)]], tablefmt="plain"))

    print()
    print(repr(''.join(map(str, chain(*q))).replace('0', ' ')))
    print(repr(''.join(map(str, chain(*(e if e.ready else {0} for e in b.flat())))).replace('0', ' ')))
