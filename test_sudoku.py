from app import Board, Solver


def test_board_solved():
    brd = Board.from_array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    assert brd.solved() is False

    brd = Board.from_array([
        [8, 7, 0, 0, 0, 1, 4, 0, 0],
        [3, 0, 0, 2, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 1, 0, 0, 6, 0, 9, 4],
        [9, 0, 0, 3, 0, 7, 0, 0, 8],
        [2, 8, 0, 4, 0, 0, 6, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 9, 0, 0, 3],
        [0, 0, 4, 5, 0, 0, 0, 2, 7],
    ])

    assert brd.solved() is False

    brd = Board.from_array([
        [1, 4, 7, 2, 5, 8, 3, 6, 9],
        [2, 5, 8, 3, 6, 9, 4, 7, 1],
        [3, 6, 9, 4, 7, 1, 5, 8, 2],
        [4, 7, 1, 5, 8, 2, 6, 9, 3],
        [5, 8, 2, 6, 9, 3, 7, 1, 4],
        [6, 9, 3, 7, 1, 4, 8, 2, 5],
        [7, 1, 4, 8, 2, 5, 9, 3, 6],
        [8, 2, 5, 9, 3, 6, 1, 4, 7],
        [9, 3, 6, 1, 4, 7, 2, 5, 8],
    ])

    assert brd.solved() is True


def test_board_check():
    brd = Board.from_array([
        [1, 4, 7, 2, 5, 8, 3, 6, 9],
        [2, 5, 8, 3, 6, 9, 4, 7, 1],
        [3, 6, 9, 4, 7, 1, 5, 8, 2],
        [4, 7, 1, 5, 8, 2, 6, 9, 3],
        [5, 8, 2, 6, 9, 3, 7, 1, 4],
        [6, 9, 3, 7, 1, 4, 8, 2, 5],
        [7, 1, 4, 8, 2, 5, 9, 3, 6],
        [8, 2, 5, 9, 3, 6, 1, 4, 7],
        [9, 3, 6, 1, 4, 7, 2, 5, 8],
    ])

    assert brd.check() is True

    brd = Board.from_array([
        [1, 4, 7, 2, 5, 8, 3, 6, 1],
        [2, 5, 8, 3, 6, 9, 4, 7, 1],
        [3, 6, 9, 4, 7, 1, 5, 8, 1],
        [4, 7, 1, 5, 8, 2, 6, 9, 1],
        [5, 8, 2, 6, 9, 3, 7, 1, 1],
        [6, 9, 3, 7, 1, 4, 8, 2, 1],
        [7, 1, 4, 8, 2, 5, 9, 3, 1],
        [8, 2, 5, 9, 3, 6, 1, 4, 1],
        [9, 3, 6, 1, 4, 7, 2, 5, 1],
    ])

    assert brd.check() is False


def test_board_solve_naked_tuples():
    brd = Board.from_array([
        [1, 4, 7, 2, 5, 8, 3, 6, 0],
        [2, 5, 8, 3, 6, 9, 4, 7, 0],
        [3, 6, 9, 4, 7, 1, 5, 8, 0],
        [4, 7, 1, 5, 8, 2, 6, 9, 0],
        [5, 8, 2, 6, 9, 3, 7, 1, 0],
        [6, 9, 3, 7, 1, 4, 8, 2, 0],
        [7, 1, 4, 8, 2, 5, 9, 3, 0],
        [8, 2, 5, 9, 3, 6, 1, 4, 0],
        [9, 3, 6, 1, 4, 7, 2, 5, 0],
    ])

    Solver.solve(brd, strategies={Solver.NAKED_TUPLES})

    assert brd.solved()


def test_board_solve_hidden_tuples():
    a = {2, 3}
    b = {4, 5, 6}
    c = {7, 8, 9}
    z = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    brd = Board.from_array([
        [z, a, a, b, b, b, c, c, c],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
    ])

    Solver.solve(brd, strategies={Solver.HIDDEN_TUPLES})

    assert set(next(iter(brd.get(row=0, col=0)))) == z - (a | b | c)


def test_board_solve_intersections():
    a = {1, 2, 3}
    b = {2, 3}
    z = set()

    brd = Board.from_array([
        [b, b, z, z, z, z, z, z, z],
        [b, a, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
    ])

    Solver.solve(brd, strategies={Solver.INTERSECTIONS})

    assert set(next(iter(brd.get(row=1, col=1)))) == a - b


def test_board_solve_xwing():
    a = {1, 2, 3}
    b = {1, 2}
    z = set()

    brd = Board.from_array([
        [b, z, z, z, b, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [b, z, z, z, b, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [a, z, z, z, z, z, z, z, z],
    ])

    Solver.solve(brd, strategies={Solver.XWING})

    assert set(next(iter(brd.get(row=8, col=0)))) == a - b

    brd = Board.from_array([
        [b, z, z, z, b, z, z, z, a],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [b, z, z, z, b, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [a, z, z, z, z, z, z, z, z],
    ])

    Solver.solve(brd, strategies={Solver.XWING})

    assert set(next(iter(brd.get(row=8, col=0)))) == a
    assert set(next(iter(brd.get(row=0, col=8)))) == a

    brd = Board.from_array([
        [b, z, z, z, b, z, z, z, a],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [b, z, z, z, b, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
    ])

    Solver.solve(brd, strategies={Solver.XWING})

    assert set(next(iter(brd.get(row=0, col=8)))) == a - b


def test_board_solve_swordfish():
    a = {1, 2, 3, 4}
    b = {1, 2, 3}
    z = set()

    brd = Board.from_array([
        [z, z, z, z, z, z, z, a, z],
        [z, b, z, z, b, z, z, b, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, b, z, z, b, z, z, b, z],
        [z, z, z, z, a, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, b, z, z, b, z, z, b, z],
        [z, a, z, z, z, z, z, z, z],
    ])

    Solver.solve(brd, strategies={Solver.SWORDFISH})

    assert set(next(iter(brd.get(row=8, col=1)))) == a - b
    assert set(next(iter(brd.get(row=5, col=4)))) == a - b
    assert set(next(iter(brd.get(row=0, col=7)))) == a - b

    brd = Board.from_array([
        [z, z, z, z, z, z, z, a, z],
        [z, b, z, z, z, z, z, b, z],
        [z, z, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, b, z, z, b, z, z, b, z],
        [z, a, z, z, z, z, z, z, z],
        [z, z, z, z, z, z, z, z, z],
        [z, b, z, z, b, z, z, z, z],
        [z, z, z, z, a, z, z, z, z],
    ])

    Solver.solve(brd, strategies={Solver.SWORDFISH})

    assert set(next(iter(brd.get(row=5, col=1)))) == a - b
    assert set(next(iter(brd.get(row=8, col=4)))) == a - b
    assert set(next(iter(brd.get(row=0, col=7)))) == a - b


def test_board_solve_xywing():
    r = {1, 2}
    a = {2, 3}
    b = {1, 3}
    c = {1, 2, 3, 4, 5, 6, 7, 8, 9} - (a & b)

    assert len(r & a) == len(r & b) == len(a & b) == 1

    brd = Board.from_array([
        [r, 0, 0, 0, 0, 0, 0, 0, b],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [a, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    Solver.solve(brd, strategies={Solver.XYWING})

    ers = brd.get(row=0, col=0)
    eas = brd.get(row=8) | brd.get(col=0) | brd.get(box=6)
    ebs = brd.get(row=0) | brd.get(col=8) | brd.get(box=2)

    assert all(set(e) == c for e in eas & ebs - ers)

    brd = Board.from_array([
        [0, 0, r, 0, 0, b, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [a, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    Solver.solve(brd, strategies={Solver.XYWING})

    ers = brd.get(row=0, col=3)
    eas = brd.get(row=2) | brd.get(col=0) | brd.get(box=3)
    ebs = brd.get(row=0) | brd.get(col=5) | brd.get(box=1)

    assert all(set(e) == c for e in eas & ebs - ers)

    brd = Board.from_array([
        [a, 0, 0, r, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, b, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    Solver.solve(brd, strategies={Solver.XYWING})

    ers = brd.get(row=0, col=2)
    eas = brd.get(row=0) | brd.get(col=0) | brd.get(box=0)
    ebs = brd.get(row=2) | brd.get(col=5) | brd.get(box=4)

    assert all(set(e) == c for e in eas & ebs - ers)


def test_board_solve_xyzwing():
    r = {1, 2, 3}
    a = {2, 3}
    b = {1, 3}
    c = {1, 2, 3, 4, 5, 6, 7, 8, 9} - (a & b)

    assert len(r & a) == len(r & b) == 2
    assert len(a & b) == 1

    brd = Board.from_array([
        [r, 0, 0, 0, 0, 0, 0, 0, b],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [a, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    Solver.solve(brd, strategies={Solver.XYZWING})

    ers = (brd.get(row=0) | brd.get(col=0) | brd.get(box=0)) - brd.get(row=0, col=0, box=0)
    eas = (brd.get(row=2) | brd.get(col=0) | brd.get(box=0)) - brd.get(row=2, col=0, box=0)
    ebs = (brd.get(row=0) | brd.get(col=8) | brd.get(box=2)) - brd.get(row=0, col=8, box=2)

    assert all(set(e) == c for e in eas & ebs & ers)

    brd = Board.from_array([
        [a, 0, 0, 0, 0, 0, r, 0, b],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    Solver.solve(brd, strategies={Solver.XYZWING})

    ers = (brd.get(row=0) | brd.get(col=6) | brd.get(box=2)) - brd.get(row=0, col=6, box=2)
    eas = (brd.get(row=0) | brd.get(col=0) | brd.get(box=0)) - brd.get(row=0, col=0, box=0)
    ebs = (brd.get(row=0) | brd.get(col=8) | brd.get(box=2)) - brd.get(row=0, col=8, box=2)

    assert all(set(e) == c for e in eas & ebs & ers)

    brd = Board.from_array([
        [r, 0, a, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, b, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    Solver.solve(brd, strategies={Solver.XYZWING})

    ers = (brd.get(row=0) | brd.get(col=0) | brd.get(box=0)) - brd.get(row=0, col=0, box=0)
    eas = (brd.get(row=0) | brd.get(col=2) | brd.get(box=0)) - brd.get(row=0, col=2, box=0)
    ebs = (brd.get(row=2) | brd.get(col=1) | brd.get(box=0)) - brd.get(row=2, col=1, box=0)

    assert all(set(e) == c for e in eas & ebs & ers)
