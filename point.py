from __future__ import annotations
import typing as t

from math import sin, cos, atan2, hypot, pi, trunc, floor, ceil

__all__ = (
    'Point',
    'MPoint',
    # comparators:
    'xy_cmp',
    'yx_cmp',
    'angle_cmp',
    'dist_cmp',
)

class _PointCommon:
    __slots__ = ('x', 'y')
    __match_args__ = ('x', 'y')

    x: float
    y: float

    def __init__(self, x: float, y: float, /) -> None:
        raise NotImplementedError

    def __str__(self, /) -> str:
        return f'<{self.__class__.__name__}: x={self.x!r}, y={self.y!r}>'

    def __repr__(self, /) -> str:
        return f'{self.__class__.__name__}({self.x!r},{self.y!r})'

    def __eq__(self, other: object, /) -> bool:
        """=="""
        if isinstance(other, _PointCommon):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other: object, /) -> bool:
        """!="""
        if isinstance(other, _PointCommon):
            return self.x != other.x or self.y != other.y
        return NotImplemented

    def __iter__(self, /) -> t.Iterator[float]:
        yield self.x
        yield self.y

    def __complex__(self, /) -> complex:
        return self.x + self.y * 1j

    def __abs__(self, /) -> float:
        return self.abs()

    def __neg__(self, /) -> t.Self:
        """-p"""
        return self.__class__(-self.x, -self.y)

    def __pos__(self, /) -> t.Self:
        """+p"""
        return self.__class__(self.x, self.y)

    def __invert__(self, /) -> t.Self:
        """~p"""
        return self.__class__(self.y, self.x)

    def __add__(self, other: _PointCommon, /) -> t.Self:
        """p1 + p2"""
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: _PointCommon, /) -> t.Self:
        """p1 - p2"""
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float, /) -> t.Self:
        """p * x"""
        return self.__class__(self.x * other, self.y * other)

    def __rmul__(self, other: float, /) -> t.Self:
        """x * p"""
        return self.__class__(other * self.x, other * self.y)

    def __truediv__(self, other: float, /) -> t.Self:
        """p / x"""
        return self.__class__(self.x / other, self.y / other)

    def __matmul__(self, other: _PointCommon, /) -> float:
        """p1 @ p2"""
        return self.x * other.x + self.y * other.y

    def __mod__(self, other: float | _PointCommon, /) -> t.Self:
        """p1 % p2  p % x"""
        if isinstance(other, _PointCommon):
            return self.__class__(self.x % other.x, self.y % other.y)
        # if isinstance(other, (int, float)):
        return self.__class__(self.x % other, self.y % other)

    # def __round__(self, ndigits: int | None = None, /) -> t.Self:
    #     if ndigits is not None:
    #         return self.__class__(self.x.__round__(ndigits), self.y.__round__(ndigits))
    #     else:
    #         return self.__class__(self.x.__round__(), self.y.__round__())

    # def __ceil__(self, /) -> t.Self:
    #     return self.__class__(self.x.__ceil__(), self.y.__ceil__())

    # def __floor__(self, /) -> t.Self:
    #     return self.__class__(self.x.__floor__(), self.y.__floor__())

    # def __trunc__(self, /) -> t.Self:
    #     return self.__class__(self.x.__trunc__(), self.y.__trunc__())

    def __reduce__(self, /) -> tuple[type[t.Self], tuple[float, float]]:
        return self.__class__, (self.x, self.y)

    @classmethod
    def from_angle(cls, angle: float, magn: float = 1.0, /) -> t.Self:
        return cls(cos(angle) * magn, sin(angle) * magn)

    @classmethod
    def from_complex(cls, val: complex, /) -> t.Self:
        return cls(val.real, val.imag)

    @classmethod
    def from_tuple(cls, tup: tuple[float, float], /) -> t.Self:
        return cls(tup[0], tup[1])

    @classmethod
    def from_point(cls, p: _PointCommon, /) -> t.Self:
        return cls(p.x, p.y)

    def to_tuple(self, /) -> tuple[float, float]:
        return (self.x, self.y)

    def map[T](self, f: t.Callable[[float], T], /) -> tuple[T, T]:
        return (f(self.x), f(self.y))

    def round(self, /) -> tuple[int, int]:
        return self.map(round)

    def trunc(self, /) -> tuple[int, int]:
        return self.map(trunc)

    def floor(self, /) -> tuple[int, int]:
        return self.map(floor)

    def ceil(self, /) -> tuple[int, int]:
        return self.map(ceil)

    def abs(self, /) -> float:
        return hypot(self.x, self.y)

    def angle(self, /) -> float:
        return atan2(self.y, self.x)

    def norm(self, /) -> t.Self:
        return self / self.abs()

    def rotate(self, angle: float, /) -> t.Self:
        return self.__class__.from_angle(self.angle() + angle, self.abs())

    def angle_to(self, other: _PointCommon, /) -> float:
        return (other.angle() - self.angle()) % (2 * pi)
        # return other.rotate(-self.angle()).angle()

    def dist(self, other: _PointCommon, /) -> float:
        return hypot(self.x - other.x, self.y - other.y)

    def dist2(self, other: _PointCommon, /) -> float:
        return (self.x - other.x) ** 2.0 + (self.y - other.y) ** 2.0

    def flip_x(self, /) -> t.Self:
        return self.__class__(-self.x, self.y)

    def flip_y(self, /) -> t.Self:
        return self.__class__(self.x, -self.y)


# direct setters for attributes to prevent AttributeError on immutable instances
_set_x: Callable[[_PointCommon, float], None] = _PointCommon.x.__set__  # type: ignore[attr-defined, misc]
_set_y: Callable[[_PointCommon, float], None] = _PointCommon.y.__set__  # type: ignore[attr-defined, misc]


class Point(_PointCommon):
    """
    Immutable
    """

    __slots__ = ()

    p00: t.ClassVar[Point]
    p10: t.ClassVar[Point]
    p01: t.ClassVar[Point]
    p11: t.ClassVar[Point]
    i: t.ClassVar[Point]
    j: t.ClassVar[Point]

    def __init__(self, x: float, y: float, /) -> None:
        _set_x(self, x)
        _set_y(self, y)

    def __hash__(self, /) -> int:
        return hash((self.x, self.y))

    def __copy__(self, /) -> t.Self:
        return self

    def __pos__(self, /) -> t.Self:
        return self

    def __setattr__(self, attr: str, val: t.Any, /) -> None:
        if hasattr(self, attr):
            raise AttributeError(
                f'{self.__class__.__name__!r} object attribute {attr!r} is read-only'
            )
        else:
            raise AttributeError(f'{self.__class__.__name__} object has no attribute {attr!r}')


Point.p00 = Point(0, 0)
Point.p10 = Point(1, 0)
Point.p01 = Point(0, 1)
Point.p11 = Point(1, 1)
Point.i = Point(1, 0)
Point.j = Point(0, 1)


class MPoint(_PointCommon):
    """
    Mutable
    """

    __slots__ = ()

    __hash__ = None  # type: ignore[assignment]

    def __init__(self, x: float, y: float, /) -> None:
        self.x = x
        self.y = y

    def __copy__(self, /) -> t.Self:
        return self.__class__(self.x, self.y)

    def __iadd__(self, other: _PointCommon, /) -> t.Self:
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: _PointCommon, /) -> t.Self:
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other: float, /) -> t.Self:
        self.x *= other
        self.y *= other
        return self

    def __itruediv__(self, other: float, /) -> t.Self:
        self.x /= other
        self.y /= other
        return self

    def __imod__(self, other: float | _PointCommon, /) -> t.Self:
        if isinstance(other, _PointCommon):
            self.x %= other.x
            self.y %= other.y
            return self
        if isinstance(other, float):
            self.x %= other
            self.y %= other
            return self
        raise TypeError

    def inorm(self, /) -> t.Self:
        self /= self.abs()
        return self

    def irotate(self, angle: float, /) -> t.Self:
        magn = self.abs()
        newang = self.angle() + angle
        self.x = cos(newang) * magn
        self.y = sin(newang) * magn
        return self


# comparators:
def xy_cmp(p: _PointCommon, /) -> tuple[float, float]:
    return (p.x, p.y)


def yx_cmp(p: _PointCommon, /) -> tuple[float, float]:
    return (p.y, p.x)


def angle_cmp(p: _PointCommon, /) -> tuple[float, float]:
    return (p.angle(), p.abs())


def dist_cmp(p: _PointCommon | None = None, /) -> t.Callable[[_PointCommon], float]:
    if p is None:
        return _PointCommon.abs  # compare by dist from origin
    else:
        return p.dist  # compare by dist from p
