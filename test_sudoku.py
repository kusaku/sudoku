from app import Board


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

    brd.solve(strategies={Board.NAKED_TUPLES})

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

    brd.solve(strategies={Board.HIDDEN_TUPLES})

    assert set(next(iter(brd.get(row=0, col=0)))) == z - (a | b | c)


def test_board_solve_intersectionss():
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

    brd.solve(strategies={Board.INTERSECTIONS})

    assert set(next(iter(brd.get(row=1, col=1)))) == a - b
