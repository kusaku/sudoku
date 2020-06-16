import solver
import sudoku


def test_box_display():
    brd = sudoku.Board.from_array([
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
    ])

    brd_str = (
        '| ╔═══╗ | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 |\n'
        '| ║ 1 ║ | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 |\n'
        '| ╚═══╝ | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 |\n'
        '| 1 2 3 | ╔═══╗ | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 |\n'
        '| 4 5 6 | ║ 2 ║ | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 |\n'
        '| 7 8 9 | ╚═══╝ | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 |\n'
        '| 1 2 3 | 1 2 3 | ╔═══╗ | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 |\n'
        '| 4 5 6 | 4 5 6 | ║ 3 ║ | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 |\n'
        '| 7 8 9 | 7 8 9 | ╚═══╝ | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 |\n'
        '| 1 2 3 | 1 2 3 | 1 2 3 | ╔═══╗ | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 |\n'
        '| 4 5 6 | 4 5 6 | 4 5 6 | ║ 4 ║ | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 |\n'
        '| 7 8 9 | 7 8 9 | 7 8 9 | ╚═══╝ | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 |\n'
        '| 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | ╔═══╗ | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 |\n'
        '| 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | ║ 5 ║ | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 |\n'
        '| 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | ╚═══╝ | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 |\n'
        '| 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | ╔═══╗ | 1 2 3 | 1 2 3 | 1 2 3 |\n'
        '| 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | ║ 6 ║ | 4 5 6 | 4 5 6 | 4 5 6 |\n'
        '| 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | ╚═══╝ | 7 8 9 | 7 8 9 | 7 8 9 |\n'
        '| 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | ╔═══╗ | 1 2 3 | 1 2 3 |\n'
        '| 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | ║ 7 ║ | 4 5 6 | 4 5 6 |\n'
        '| 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | ╚═══╝ | 7 8 9 | 7 8 9 |\n'
        '| 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | ╔═══╗ | 1 2 3 |\n'
        '| 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | ║ 8 ║ | 4 5 6 |\n'
        '| 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | ╚═══╝ | 7 8 9 |\n'
        '| 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | 1 2 3 | ╔═══╗ |\n'
        '| 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | 4 5 6 | ║ 9 ║ |\n'
        '| 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | 7 8 9 | ╚═══╝ |\n'
    )

    assert str(brd) == brd_str


def test_unit_display():
    sudoku.Element(row=0, col=0, box=0, initial=set({1}))

    row = sudoku.Row({
        sudoku.Element(row=0, col=0, box=0, initial=set({1})),
        sudoku.Element(row=0, col=1, box=0, initial=set({2})),
        sudoku.Element(row=0, col=2, box=0, initial=set({3})),
        sudoku.Element(row=0, col=3, box=1, initial=set({4})),
        sudoku.Element(row=0, col=4, box=1, initial=set({5})),
        sudoku.Element(row=0, col=5, box=1, initial=set({6})),
        sudoku.Element(row=0, col=6, box=2, initial=set({7})),
        sudoku.Element(row=0, col=7, box=2, initial=set({8})),
        sudoku.Element(row=0, col=8, box=2, initial=set({9})),
    })

    row_str = (
        '| ╔═══╗ | ╔═══╗ | ╔═══╗ | ╔═══╗ | ╔═══╗ | ╔═══╗ | ╔═══╗ | ╔═══╗ | ╔═══╗ |\n'
        '| ║ 1 ║ | ║ 2 ║ | ║ 3 ║ | ║ 4 ║ | ║ 5 ║ | ║ 6 ║ | ║ 7 ║ | ║ 8 ║ | ║ 9 ║ |\n'
        '| ╚═══╝ | ╚═══╝ | ╚═══╝ | ╚═══╝ | ╚═══╝ | ╚═══╝ | ╚═══╝ | ╚═══╝ | ╚═══╝ |\n'
    )

    assert str(row) == row_str

    col = sudoku.Col({
        sudoku.Element(row=0, col=0, box=0, initial=set({1})),
        sudoku.Element(row=1, col=0, box=0, initial=set({2})),
        sudoku.Element(row=2, col=0, box=0, initial=set({3})),
        sudoku.Element(row=3, col=0, box=3, initial=set({4})),
        sudoku.Element(row=4, col=0, box=3, initial=set({5})),
        sudoku.Element(row=5, col=0, box=3, initial=set({6})),
        sudoku.Element(row=6, col=0, box=6, initial=set({7})),
        sudoku.Element(row=7, col=0, box=6, initial=set({8})),
        sudoku.Element(row=8, col=0, box=6, initial=set({9})),
    })

    col_str = (
        '| ╔═══╗ |\n'
        '| ║ 1 ║ |\n'
        '| ╚═══╝ |\n'
        '| ╔═══╗ |\n'
        '| ║ 2 ║ |\n'
        '| ╚═══╝ |\n'
        '| ╔═══╗ |\n'
        '| ║ 3 ║ |\n'
        '| ╚═══╝ |\n'
        '| ╔═══╗ |\n'
        '| ║ 4 ║ |\n'
        '| ╚═══╝ |\n'
        '| ╔═══╗ |\n'
        '| ║ 5 ║ |\n'
        '| ╚═══╝ |\n'
        '| ╔═══╗ |\n'
        '| ║ 6 ║ |\n'
        '| ╚═══╝ |\n'
        '| ╔═══╗ |\n'
        '| ║ 7 ║ |\n'
        '| ╚═══╝ |\n'
        '| ╔═══╗ |\n'
        '| ║ 8 ║ |\n'
        '| ╚═══╝ |\n'
        '| ╔═══╗ |\n'
        '| ║ 9 ║ |\n'
        '| ╚═══╝ |\n'
    )

    assert str(col) == col_str

    box = sudoku.Box({
        sudoku.Element(row=0, col=0, box=0, initial=set({1})),
        sudoku.Element(row=0, col=1, box=0, initial=set({2})),
        sudoku.Element(row=0, col=2, box=0, initial=set({3})),
        sudoku.Element(row=1, col=0, box=0, initial=set({4})),
        sudoku.Element(row=1, col=1, box=0, initial=set({5})),
        sudoku.Element(row=1, col=2, box=0, initial=set({6})),
        sudoku.Element(row=2, col=0, box=0, initial=set({7})),
        sudoku.Element(row=2, col=1, box=0, initial=set({8})),
        sudoku.Element(row=2, col=2, box=0, initial=set({9})),
    })

    box_str = (
        '| ╔═══╗ | ╔═══╗ | ╔═══╗ |\n'
        '| ║ 1 ║ | ║ 2 ║ | ║ 3 ║ |\n'
        '| ╚═══╝ | ╚═══╝ | ╚═══╝ |\n'
        '| ╔═══╗ | ╔═══╗ | ╔═══╗ |\n'
        '| ║ 4 ║ | ║ 5 ║ | ║ 6 ║ |\n'
        '| ╚═══╝ | ╚═══╝ | ╚═══╝ |\n'
        '| ╔═══╗ | ╔═══╗ | ╔═══╗ |\n'
        '| ║ 7 ║ | ║ 8 ║ | ║ 9 ║ |\n'
        '| ╚═══╝ | ╚═══╝ | ╚═══╝ |\n'
    )

    assert str(box) == box_str


def test_element_display():
    empty = sudoku.Element(row=0, col=0, box=0, initial=set())

    empty_str = (
        'X X X\n'
        'X X X\n'
        'X X X\n'
    )

    assert str(empty) == empty_str

    full = sudoku.Element(row=0, col=0, box=0, initial={1, 2, 3, 4, 5, 6, 7, 8, 9})

    full_str = (
        '1 2 3\n'
        '4 5 6\n'
        '7 8 9\n'
    )

    assert str(full) == full_str

    partial = sudoku.Element(row=0, col=0, box=0, initial={1, 3, 5, 7, 9})

    partial_str = (
        '1 . 3\n'
        '. 5 .\n'
        '7 . 9\n'
    )

    assert str(partial) == partial_str

    single = sudoku.Element(row=0, col=0, box=0, initial={5})

    single_str = (
        '╔═══╗\n'
        '║ 5 ║\n'
        '╚═══╝\n'
    )

    assert str(single) == single_str


def test_board_solved():
    brd = sudoku.Board.from_array([
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

    brd = sudoku.Board.from_array([
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

    brd = sudoku.Board.from_array([
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
    brd = sudoku.Board.from_array([
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

    brd = sudoku.Board.from_array([
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
    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.naked_tuples})

    assert brd.solved()


def test_board_solve_hidden_tuples():
    a = {2, 3}
    b = {4, 5, 6}
    c = {7, 8, 9}
    z = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.hidden_tuples})

    assert set(next(iter(brd.get(row=0, col=0)))) == z - (a | b | c)


def test_board_solve_intersections():
    a = {1, 2, 3}
    b = {2, 3}
    z = set()

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.intersections})

    assert set(next(iter(brd.get(row=1, col=1)))) == a - b


def test_board_solve_xwing():
    a = {1, 2, 3}
    b = {1, 2}
    z = set()

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.x_wing})

    assert set(next(iter(brd.get(row=8, col=0)))) == a - b

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.x_wing})

    assert set(next(iter(brd.get(row=8, col=0)))) == a
    assert set(next(iter(brd.get(row=0, col=8)))) == a

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.x_wing})

    assert set(next(iter(brd.get(row=0, col=8)))) == a - b


def test_board_solve_swordfish():
    a = {1, 2, 3, 4}
    b = {1, 2, 3}
    z = set()

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.swordfish})

    assert set(next(iter(brd.get(row=8, col=1)))) == a - b
    assert set(next(iter(brd.get(row=5, col=4)))) == a - b
    assert set(next(iter(brd.get(row=0, col=7)))) == a - b

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.swordfish})

    assert set(next(iter(brd.get(row=5, col=1)))) == a - b
    assert set(next(iter(brd.get(row=8, col=4)))) == a - b
    assert set(next(iter(brd.get(row=0, col=7)))) == a - b


def test_board_solve_xywing():
    r = {1, 2}
    a = {2, 3}
    b = {1, 3}
    c = {1, 2, 3, 4, 5, 6, 7, 8, 9} - (a & b)

    assert len(r & a) == len(r & b) == len(a & b) == 1

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.xy_wing})

    ers = brd.get(row=0, col=0)
    eas = brd.get(row=8) | brd.get(col=0) | brd.get(box=6)
    ebs = brd.get(row=0) | brd.get(col=8) | brd.get(box=2)

    assert all(set(e) == c for e in eas & ebs - ers)

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.xy_wing})

    ers = brd.get(row=0, col=3)
    eas = brd.get(row=2) | brd.get(col=0) | brd.get(box=3)
    ebs = brd.get(row=0) | brd.get(col=5) | brd.get(box=1)

    assert all(set(e) == c for e in eas & ebs - ers)

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.xy_wing})

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

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.xyz_wing})

    ers = (brd.get(row=0) | brd.get(col=0) | brd.get(box=0)) - brd.get(row=0, col=0, box=0)
    eas = (brd.get(row=2) | brd.get(col=0) | brd.get(box=0)) - brd.get(row=2, col=0, box=0)
    ebs = (brd.get(row=0) | brd.get(col=8) | brd.get(box=2)) - brd.get(row=0, col=8, box=2)

    assert all(set(e) == c for e in eas & ebs & ers)

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.xyz_wing})

    ers = (brd.get(row=0) | brd.get(col=6) | brd.get(box=2)) - brd.get(row=0, col=6, box=2)
    eas = (brd.get(row=0) | brd.get(col=0) | brd.get(box=0)) - brd.get(row=0, col=0, box=0)
    ebs = (brd.get(row=0) | brd.get(col=8) | brd.get(box=2)) - brd.get(row=0, col=8, box=2)

    assert all(set(e) == c for e in eas & ebs & ers)

    brd = sudoku.Board.from_array([
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

    solver.solve(brd, strategies={solver.xyz_wing})

    ers = (brd.get(row=0) | brd.get(col=0) | brd.get(box=0)) - brd.get(row=0, col=0, box=0)
    eas = (brd.get(row=0) | brd.get(col=2) | brd.get(box=0)) - brd.get(row=0, col=2, box=0)
    ebs = (brd.get(row=2) | brd.get(col=1) | brd.get(box=0)) - brd.get(row=2, col=1, box=0)

    assert all(set(e) == c for e in eas & ebs & ers)


# TODO: rewrite to synthetic test
def test_board_solve_coloring():
    # https://www.sudokuwiki.org/sudoku.htm?bd=062900000004308000709000400600801000003000200000207003001000904000709300000004120
    brd = sudoku.Board.from_string('000000070000090810500203004800020000045000720000000003400308006072010000030000000')

    solver.solve(brd, strategies=solver.STRATEGIES - {solver.coloring})
    assert brd.solved() is False

    solver.solve(brd)
    assert brd.solved() is True

# if __name__ == '__main__':
#     brd = sudoku.Board.from_string('000000070000090810500203004800020000045000720000000003400308006072010000030000000')
#     solver.solve(brd, strategies=solver.STRATEGIES - {solver.coloring})
#     print(brd)
#     print()
#     solver.solve(brd)
#     print(brd)
#     print()
#     assert brd.solved() is True
