from __future__ import annotations
import typing as t
import dataclasses

from stringbuilder import StringBuilder

# -1 - no info
#  0 - no edge present
#  1 - edge present
type _Edge = int
EDGE_UNK: t.Final[_Edge] = -1
EDGE_0: t.Final[_Edge] = 0
EDGE_1: t.Final[_Edge] = 1

# -1 - no info
# 0-3 - number
type _Num = int
NUM_UNK: t.Final[_Num] = -1

type _Vertex = t.Any
VERTEX_UNK: t.Final[_Vertex] = 0


@dataclasses.dataclass
class Cell:
    x: int
    y: int
    _board: Board

    @property
    def value(self) -> _Num:
        return self._board._get_num(self.x, self.y)

    @value.setter
    def value(self, value: _Num) -> None:
        self._board._set_num(self.x, self.y, value)


@dataclasses.dataclass
class Vertex:
    x: int
    y: int
    _board: Board

    @property
    def value(self) -> Vertex:
        return self._board._get_vtx(self.x, self.y)

    @property
    def edges(self) -> list[_Edge]:
        return [
            self._board.edges[self.x, self.y].left,
            self._board.edges[self.x, self.y].top,
            self._board.edges[self.x-1, self.y-1].right,
            self._board.edges[self.x-1, self.y-1].bottom,
        ]



@dataclasses.dataclass
class Edge:
    x: int
    y: int
    _board: Board

    @property
    def left(self) -> _Edge:
        return self._board._get_edge_v(self.x, self.y)

    @left.setter
    def left(self, value: _Edge) -> None:
        self._board._set_edge_v(self.x, self.y, value)

    @property
    def right(self) -> _Edge:
        return self._board._get_edge_v(self.x + 1, self.y)

    @right.setter
    def right(self, value: _Edge) -> None:
        self._board._set_edge_v(self.x + 1, self.y, value)

    @property
    def top(self) -> _Edge:
        return self._board._get_edge_h(self.x, self.y)

    @top.setter
    def top(self, value: _Edge) -> None:
        self._board._set_edge_h(self.x, self.y, value)

    @property
    def bottom(self) -> _Edge:
        return self._board._get_edge_h(self.x, self.y + 1)

    @bottom.setter
    def bottom(self, value: _Edge) -> None:
        self._board._set_edge_h(self.x, self.y + 1, value)

    @property
    def edges(self) -> list[_Edge]:
        return [
            self.top,
            self.right,
            self.bottom,
            self.left,
        ]


@dataclasses.dataclass
class _Cells:
    _board: Board

    def __getitem__(self, xy: tuple[int, int]) -> Cell:
        x, y = xy
        return Cell(x, y, self._board)


@dataclasses.dataclass
class _Vertices:
    _board: Board

    def __getitem__(self, xy: tuple[int, int]) -> Vertex:
        x, y = xy
        return Vertex(x, y, self._board)


@dataclasses.dataclass
class _Edges:
    _board: Board

    def __getitem__(self, xy: tuple[int, int]) -> Edge:
        x, y = xy
        return Edge(x, y, self._board)


class Board:
    x: int
    y: int
    data: list[list[t.Any]]

    def __init__(self, x: int, y: int, /) -> None:
        self.x = x
        self.y = y
        empty_row_v = [VERTEX_UNK, EDGE_UNK] * x + [VERTEX_UNK]
        empty_row_m = [EDGE_UNK, NUM_UNK] * x + [EDGE_UNK]
        self.data = [empty_row_v[::] if i % 2 == 0 else empty_row_m[::] for i in range(2 * y + 1)]

    @property
    def vertices(self) -> _Vertices:
        return _Vertices(self)

    @property
    def cells(self) -> _Cells:
        return _Cells(self)

    @property
    def edges(self) -> _Edges:
        return _Edges(self)

    def _get_num(self, x: int, y: int) -> _Num:
        if x not in range(0, self.x): return NUM_UNK
        if y not in range(0, self.y): return NUM_UNK
        return self.data[2 * y + 1][2 * x + 1]

    def _set_num(self, x: int, y: int, val: _Num) -> None:
        if x not in range(0, self.x): raise Exception('TODO: think about it')
        if y not in range(0, self.y): raise Exception('TODO: think about it')
        self.data[2 * y + 1][2 * x + 1] = val

    def _get_vtx(self, x: int, y: int) -> Vertex: # TODO: fix later
        if x not in range(0, self.x + 1): return VERTEX_UNK
        if y not in range(0, self.y + 1): return VERTEX_UNK
        return self.data[2 * y][2 * x]

    def _set_vtx(self, x: int, y: int, val: Vertex) -> None:
        if x not in range(0, self.x + 1): raise Exception('TODO: think about it')
        if y not in range(0, self.y + 1): raise Exception('TODO: think about it')
        self.data[2 * y][2 * x] = val

    def _get_edge_h(self, x: int, y: int) -> _Edge:
        if x not in range(0, self.x): return EDGE_0
        if y not in range(0, self.y + 1): return EDGE_0
        return self.data[2 * y][2 * x + 1]

    def _set_edge_h(self, x: int, y: int, val: _Edge) -> None:
        if x not in range(0, self.x): raise Exception('TODO: think about it')
        if y not in range(0, self.y + 1): raise Exception('TODO: think about it')
        self.data[2 * y][2 * x + 1] = val

    def _get_edge_v(self, x: int, y: int) -> _Edge:
        if x not in range(0, self.x + 1): return EDGE_0
        if y not in range(0, self.y): return EDGE_0
        return self.data[2 * y + 1][2 * x]

    def _set_edge_v(self, x: int, y: int, val: _Edge) -> None:
        if x not in range(0, self.x + 1): raise Exception('TODO: think about it')
        if y not in range(0, self.y): raise Exception('TODO: think about it')
        self.data[2 * y + 1][2 * x] = val

    def __str__(self) -> str:
        edgev2str = {
            EDGE_UNK: ' ',
            EDGE_0: 'x',
            EDGE_1: '|',
        }
        edgeh2str = {
            EDGE_UNK: ' ',
            EDGE_0: 'x',
            EDGE_1: '-',
        }

        num2str = {
            NUM_UNK: ' ',
            0: '0',
            1: '1',
            2: '2',
            3: '3',
        }

        vtx2str = {
            VERTEX_UNK: '+',
        }

        s = StringBuilder()
        for i in range(self.y + 1):
            for j in range(self.x + 1):
                s += vtx2str[self.vertices[j, i].value]
                if j != self.x:
                    s += ' '
                    e = self.edges[j, i].top
                    s += edgeh2str[e]
                    s += ' '

            if i != self.y:
                s += '\n'
                for j in range(self.x + 1):
                    e = self.edges[j, i].left
                    s += edgev2str[e]
                    if j != self.x:
                        n = self.cells[j, i].value
                        s += ' '
                        s += num2str[n]
                        s += ' '
                s += '\n'

        return str(s)


def parse_rule(s: str, initial: bool = True) -> Board:
    lines = s.splitlines()
    lines = [line for line in lines if line]
    lines = [line for line in lines if not line.strip().startswith('#')]
    if initial:
        lines = [line.replace('(x)', '   ') for line in lines]
        lines = [line.replace('(|)', '   ') for line in lines]
        lines = [line.replace('(-)', '   ') for line in lines]

    assert lines
    assert len(set(map(len, lines))) == 1, set(map(len, lines))
    x = (len(lines[0]) - 3) // 4
    y = (len(lines) - 1) // 2

    b = Board(x, y)

    for j in range(y):
        for i in range(x):
            c = lines[j * 2 + 1][4 * i + 3]
            if c == ' ':
                pass
            if c in '0123':
                b._set_num(i, j, int(c))

    for j in range(y):
        for i in range(x + 1):
            c = lines[j * 2 + 1][4 * i + 1]
            if c == ' ':
                pass
            if c == '|':
                b._set_edge_v(i, j, EDGE_1)
            if c == 'x':
                b._set_edge_v(i, j, EDGE_0)

    for j in range(y + 1):
        for i in range(x):
            c = lines[j * 2][4 * i + 3]
            if c == ' ':
                pass
            if c == '-':
                b._set_edge_h(i, j, EDGE_1)
            if c == 'x':
                b._set_edge_h(i, j, EDGE_0)

    return b


def make_random_board(n: int) -> Board:
    b = Board(n, n)
    # b.set_num(2, 2, 3)
    # b.set_edge_h(2, 2, STATE_1)
    # b.set_edge_h(3, 3, STATE_0)
    # b.set_edge_v(4, 4, STATE_1)
    # b.set_edge_v(5, 5, STATE_0)

    import random

    for _ in range(n ** 2 // 2):
        x = random.randrange(0, b.x)
        y = random.randrange(0, b.y)
        v = random.choice([0, 1, 2, 3])
        b._set_num(x, y, v)

    for _ in range(n ** 2 // 2):
        x = random.randrange(0, b.x + 1)
        y = random.randrange(0, b.y)
        v = random.choice([0, 1])
        b._set_edge_v(x, y, v)

    for _ in range(n ** 2 // 2):
        x = random.randrange(0, b.x)
        y = random.randrange(0, b.y + 1)
        v = random.choice([0, 1])
        b._set_edge_h(x, y, v)
    return b

    # print(b)
    # print()


def test_rule() -> None:
    rules = open('rules.sli').read().split('\n\n')
    rules = [r for r in rules if r.strip()]
    rule = rules[38 + 3]
    print(rule)
    print()
    print(parse_rule(rule))
    print('=>')
    print(parse_rule(rule, False))
