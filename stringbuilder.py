from __future__ import annotations
import typing as t
import dataclasses


@dataclasses.dataclass(slots=True, frozen=True)
class _Node:
    val: str
    next: _Node | None = None

    def __iter__(self) -> t.Iterator[str]:
        node = self
        while node is not None:
            yield node.val
            node = node.next


class StringBuilder:
    __slots__ = ('_node',)
    _node: _Node

    def __init__(self, _node: _Node = _Node('', None)) -> None:
        self._node = _node

    def __iadd__(self, s: str) -> t.Self:
        self._node = _Node(s, self._node)
        return self

    def __getitem__(self, index: slice) -> t.Self:
        if index != slice(None):
            raise ValueError(f'only [::] slice allowed')
        return self.__class__(self._node)

    def __str__(self) -> str:
        s = ''.join(reversed([*self._node])) # is there a better way?
        self._node = _Node(s)
        return s


s = StringBuilder()
s += 'a'
s += 'bc'
assert str(s) == 'abc'

s2 = s[::]
s2 += 'd'
assert str(s) == 'abc'
assert str(s2) == 'abcd'
