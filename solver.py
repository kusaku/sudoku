import operator
from collections import Counter, defaultdict
from functools import reduce
from itertools import chain


def _naked_tuples(unit):
    changed = False
    c = Counter(map(tuple, unit))  # noqa - tuple(set(...))
    for v, count in c.items():
        if count == len(v):
            vs = set(v)
            for e in unit:
                if set(e) != vs:
                    changed |= e.exclude(vs)
    return changed


def naked_tuples(brd):
    changed = False
    loop_changed = True
    while loop_changed:
        loop_changed = False
        for num in range(brd.RANK):
            loop_changed |= _naked_tuples(brd.box(num))
            loop_changed |= _naked_tuples(brd.row(num))
            loop_changed |= _naked_tuples(brd.col(num))
        changed |= loop_changed
    return changed


def _hidden_tuples(unit):
    changed = False
    c = Counter(chain(*unit))
    d = defaultdict(dict)
    for v, count in c.items():
        d[count][v] = {e for e in unit if v in e}
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


def hidden_tuples(brd):
    changed = False
    loop_changed = True
    while loop_changed:
        loop_changed = False
        for num in range(brd.RANK):
            loop_changed |= _hidden_tuples(brd.box(num))
            loop_changed |= _hidden_tuples(brd.row(num))
            loop_changed |= _hidden_tuples(brd.col(num))
        changed |= loop_changed
    return changed


def _intersections(unit1, unit2):
    changed = False
    for v in set(chain(*(unit1 & unit2))):
        c = {e for e in unit1 | unit2 if v in e}
        if c & unit1 == c & unit1 & unit2:
            for e in c - unit1:
                changed |= e.exclude({v})
        if c & unit2 == c & unit1 & unit2:
            for e in c - unit2:
                changed |= e.exclude({v})
    return changed


def intersections(brd):
    changed = False
    loop_changed = True
    while loop_changed:
        loop_changed = False
        for b in range(brd.RANK):
            box = brd.box(b)
            for num in {e.row for e in box}:
                loop_changed |= _intersections(box, brd.row(num))
            for num in {e.col for e in box}:
                loop_changed |= _intersections(box, brd.col(num))
        changed |= loop_changed
    return changed


def _x_wing_filter(unit):
    return {
        v: set(e for e in unit if v in e)
        for v, count in Counter(chain(*unit)).items()
        if count == 2
    }


def x_wing(brd):
    changed = False

    for num1 in range(brd.RANK - 1):
        row1 = _x_wing_filter(brd.row(num1))
        col1 = _x_wing_filter(brd.col(num1))
        for num2 in range(num1 + 1, brd.RANK):
            row2 = _x_wing_filter(brd.row(num2))
            col2 = _x_wing_filter(brd.col(num2))
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


def _swordfish_filter(unit):
    return {
        v: set(e for e in unit if v in e)
        for v, count in Counter(chain(*unit)).items()
        if count in {2, 3}
    }


def swordfish(brd):
    changed = False
    for num1 in range(brd.RANK - 2):
        row1 = _swordfish_filter(brd.row(num1))
        col1 = _swordfish_filter(brd.col(num1))
        for num2 in range(num1 + 1, brd.RANK - 1):
            row2 = _swordfish_filter(brd.row(num2))
            col2 = _swordfish_filter(brd.col(num2))
            for num3 in range(num2 + 1, brd.RANK):
                row3 = _swordfish_filter(brd.row(num3))
                col3 = _swordfish_filter(brd.col(num3))
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


def xy_wing(brd):
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


def xyz_wing(brd):
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


def coloring(brd):
    changed = False
    for v, es in ((v, {e for e in brd if v in e}) for v in set(chain(*brd))):

        def bilocation(e1, e2):
            return (
                e1 != e2 and
                (
                    e1.row == e2.row and es & brd.row(e1.row) == {e1, e2}
                    or
                    e1.col == e2.col and es & brd.col(e1.col) == {e1, e2}
                    or
                    e1.box == e2.box and es & brd.box(e1.box) == {e1, e2}
                )
            )

        graph = defaultdict(set)
        for e1 in es:
            for e2 in es:
                if bilocation(e1, e2):
                    graph[e1].add(e2)
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


naked_tuples.merit = 1
hidden_tuples.merit = 2
intersections.merit = 3
x_wing.merit = 4
xy_wing.merit = 5
xyz_wing.merit = 6
swordfish.merit = 7
coloring.merit = 9

STRATEGIES = {
    naked_tuples,
    hidden_tuples,
    intersections,
    x_wing,
    xy_wing,
    xyz_wing,
    swordfish,
    coloring,
}


def solve(brd, strategies=STRATEGIES):
    changed = True
    while changed:
        changed = False
        for strategy in sorted(strategies, key=lambda x: x.merit):
            changed |= strategy(brd)
