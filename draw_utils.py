from __future__ import annotations
import typing as t
import functools

import pygame as pg
from point import Point, MPoint

DEFAULT_FONT: t.Final = 'fira code'


Color = tuple[int, int, int]


def draw_surface_centered(
    sur1: pg.surface.Surface,
    sur2: pg.surface.Surface,
    xy1: Point,
    xy2: Point,
    /,
) -> None:
    size = Point.from_tuple(sur2.get_size())
    dest = xy1 + (xy2 - xy1 - size) / 2
    sur1.blit(sur2, dest.round())


def draw_dashed_line(
    surf: pg.surface.Surface,
    color: Color,
    p1: Point,
    p2: Point,
    /,
    *,
    dash_count: int = 3,
    width: float = 1,
) -> None:
    for i in range(0, dash_count, 2):
        ps = p1 + (p2 - p1) * i / dash_count
        pe = p1 + (p2 - p1) * (i + 1) / dash_count
        pg.draw.line(
            surf,
            color,
            ps.round(),
            pe.round(),
            width=round(width),
        )
    # TODO: fix it :)

    # width = max(1, round(width))

    # d = MPoint.from_point(p2 - p1)
    # dist = d.abs()
    # n = int(dist / dash_length)
    # d /= n / 2

    # ps = MPoint.from_point(p1)
    # pe = ps + d / 2

    # for _ in range(0, n - 1, 2):
    #     pg.draw.line(surf, color, ps.round(), pe.round(), width=width)
    #     ps += d
    #     pe += d
    # ps += d
    # if ps.dist(p1) <= dist:
    #     pg.draw.line(surf, color, (ps + d).round(), p2.round(), width=width)


def draw_line(
    surf: pg.surface.Surface,
    color: Color,
    p1: Point,
    p2: Point,
    /,
    *,
    width: float = 1,
) -> None:
    width = max(1, round(width))

    pg.draw.line(
        surf,
        color,
        p1.to_tuple(),
        p2.to_tuple(),
        width=width,
    )


@functools.cache
def get_font(size: int, name: str = DEFAULT_FONT, /) -> pg.font.Font:
    return pg.font.SysFont(name, size)
