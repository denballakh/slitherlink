from __future__ import annotations
from typing import ClassVar, Final
import typing as t

import pygame as pg

from point import Point
import game
from view import View
from draw_utils import (
    draw_dashed_line,
    draw_line,
    draw_surface_centered,
    get_font,
)

Color = tuple[int, int, int]
COLOR_UNK: Final[Color] = (64, 64, 64)
COLOR_0: Final[Color] = (0, 0, 0)
COLOR_1: Final[Color] = (255, 255, 255)
COLOR_BG: Final[Color] = (0, 0, 0)
COLOR_VTX_GOOD: Final[Color] = (127, 127, 127)
COLOR_VTX_BAD: Final[Color] = (255, 0, 0)
COLOR_NUM_GOOD: Final[Color] = (127, 127, 127)
COLOR_NUM_BAD: Final[Color] = (255, 127, 127)


CELL_SIZE = 64
NUM_SIZE: Final = 52
LINE_THICKNESS: Final = 4
VERTEX_SIZE: Final = 6
DASHES_CNT: Final = 5

SCREEN_SIZE: Final = (700, 700)
MIN_ZOOM: Final = CELL_SIZE // 8
MAX_ZOOM: Final = CELL_SIZE * 4
SCALE: Final = 2

# MAX_FPS: Final = 120


state2color: Final = {
    game.EDGE_UNK: COLOR_UNK,
    game.EDGE_0: COLOR_0,
    game.EDGE_1: COLOR_1,
}


# class ev:
#     EVENT_10: ClassVar = pg.event.custom_type()
#     EVENT_100: ClassVar = pg.event.custom_type()
#     EVENT_1000: ClassVar = pg.event.custom_type()


def next_state(s: game._Edge, /) -> game._Edge:
    return {
        game.EDGE_UNK: game.EDGE_1,
        game.EDGE_1: game.EDGE_0,
        game.EDGE_0: game.EDGE_UNK,
    }[s]


class App:
    __slots__ = (
        'board',
        'view',
        'screen',
        'virtual_canvas',
        'virtual_view',
        'click_map',
    )

    def __init__(self, board: game.Board) -> None:
        pg.init()
        self.board = board
        self.view = View(
            CELL_SIZE,
            Point(0, 0),
        )
        self.virtual_view = View(CELL_SIZE, Point(-1, -1))
        self.virtual_canvas = pg.Surface(
            (CELL_SIZE * (board.x + 2), CELL_SIZE * (board.y + 2)),
            flags=pg.SRCALPHA,
        )

        self.screen = pg.display.set_mode(
            SCREEN_SIZE,
            pg.RESIZABLE,
        )
        self.screen.fill(COLOR_BG)

        self.view.pos -= Point.from_tuple(self.screen.get_size()) / self.view.zoom_k / 2
        self.view.pos += Point(self.board.x, self.board.y) / 2

        self.click_map = pg.image.load('./click_map.png').convert_alpha()

    def main_loop(self) -> t.Never:
        while True:
            for event in pg.event.get():
                # print(event)

                match event:
                    case object(type=pg.QUIT):
                        import os

                        os._exit(0)

                    case object(type=pg.MOUSEBUTTONDOWN) if event.button in {4, 5}:
                        scale = SCALE if event.button == 4 else 1 / SCALE
                        new_zoom = round(self.view.zoom_k * scale)
                        if new_zoom > MAX_ZOOM:
                            scale = MAX_ZOOM / self.view.zoom_k
                        if new_zoom < MIN_ZOOM:
                            scale = MIN_ZOOM / self.view.zoom_k
                        p = self.view.unmap(Point.from_tuple(event.pos))
                        self.view.pos, self.view.zoom_k = (
                            p - (p - self.view.pos) / scale,
                            self.view.zoom_k * scale,
                        )
                        self.view.zoom_k = round(self.view.zoom_k)

                    case object(type=pg.MOUSEMOTION, buttons=(0, 0, 1)):
                        self.view.pos -= Point.from_tuple(event.rel) / self.view.zoom_k

                    case object(type=pg.KEYDOWN, scancode=pg.KSCAN_RIGHT, mod=0):
                        self.view.zoom_k += 1

                    case object(type=pg.KEYDOWN, scancode=pg.KSCAN_LEFT, mod=0):
                        self.view.zoom_k -= 1

                    case object(type=pg.KEYDOWN, scancode=pg.KSCAN_RIGHT, mod=pg.KMOD_LSHIFT):
                        self.view.zoom_k += 10

                    case object(type=pg.KEYDOWN, scancode=pg.KSCAN_LEFT, mod=pg.KMOD_LSHIFT):
                        self.view.zoom_k -= 10

                    case object(type=pg.MOUSEBUTTONDOWN) if event.button == 1:
                        p = self.view.unmap(Point.from_tuple(event.pos))
                        r = p % Point.p11
                        x, y = p.floor()

                        if x < -1:
                            continue
                        if x > self.board.x:
                            continue
                        if y < -1:
                            continue
                        if y > self.board.y:
                            continue

                        col = tuple(
                            self.click_map.get_at((r * self.click_map.get_size()[0]).floor())
                        )
                        print(col)

                        color2action = {
                            (255, 0, 0, 255): 'vtx',
                            (0, 255, 0, 255): 'edge',
                            (0, 0, 255, 255): 'num',
                            (0, 0, 0, 0): 'none',
                        }

                        match col:
                            case (130, 0, 0, 255):
                                ...  # top left
                            case (255, 0, 0, 255):
                                ...  # top right
                            case (130, 0, 130, 255):
                                ...  # bottom left
                            case (255, 0, 255, 255):
                                ...  # bottom right
                            #
                            case (0, 0, 255, 255):
                                ...  # num
                            #
                            case (0, 130, 0, 255):
                                ...  # top
                                self.board.edges[x, y].top = next_state(self.board.edges[x, y].top)
                            case (0, 255, 0, 255):
                                ...  # left
                                self.board.edges[x, y].left = next_state(self.board.edges[x, y].left)
                            case (255, 255, 0, 255):
                                ...  # right
                                self.board.edges[x, y].right = next_state(self.board.edges[x, y].right)
                            case (130, 130, 0, 255):
                                ...  # bottom
                                self.board.edges[x, y].bottom = next_state(self.board.edges[x, y].bottom)
                            #
                            case (0, 0, 0, 0):
                                ...  # none
                            case _:
                                raise Exception(f'unknown color: {col}')

                        # if p.x < -1:
                        #     continue
                        # if p.y < -1:
                        #     continue
                        # if p.x > self.board.x + 1:
                        #     continue
                        # if p.y > self.board.y + 1:
                        #     continue

                        # if rel.x < CLICK_ZONE and CLICK_ZONE < rel.y < 1 - CLICK_ZONE:
                        #     self.board.edges[x, y].left = next_state(self.board.edges[x, y].left)
                        # if rel.y < CLICK_ZONE and CLICK_ZONE < rel.x < 1 - CLICK_ZONE:
                        #     self.board.edges[x, y].top = next_state(self.board.edges[x, y].top)
                        # if rel.x > 1 - CLICK_ZONE and CLICK_ZONE < rel.y < 1 - CLICK_ZONE:
                        #     self.board.edges[x, y].right = next_state(self.board.edges[x, y].right)
                        # if rel.y > 1 - CLICK_ZONE and CLICK_ZONE < rel.x < 1 - CLICK_ZONE:
                        #     self.board.edges[x, y].bottom = next_state(
                        #         self.board.edges[x, y].bottom
                        #     )

                    case _:
                        pass
            self.draw_board()

    def draw_board(self) -> None:
        pg.display.set_caption(f'zoom: {self.view.zoom_k}')
        if 1:
            self.screen.blit(pg.transform.box_blur(self.screen, 8), (0, 0))
            self.screen.blit(pg.transform.box_blur(self.screen, 4), (0, 0))
            bg = pg.Surface(self.screen.get_size())
            bg.fill(COLOR_BG)
            bg.set_alpha(1)
            self.screen.blit(bg, (0, 0))
        else:
            self.screen.fill(COLOR_BG)

        self.virtual_canvas.fill((0, 0, 0, 0))
        self.draw_nums()
        self.draw_edges()
        self.draw_vertices()

        # scaled = pg.transform.smoothscale_by(
        scaled = pg.transform.scale_by(
            self.virtual_canvas,
            self.view.zoom_k / self.virtual_view.zoom_k,
        )
        self.screen.blit(scaled, self.view.map(Point(-1, -1)).to_tuple())

        pg.display.update()

    def draw_nums(self) -> None:
        for y in range(self.board.y):
            for x in range(self.board.x):
                # self.virtual_canvas.blit(
                #     self.click_map, self.virtual_view.map(Point(x, y)).to_tuple()
                # )
                num = self.board.cells[x, y].value
                if num == game.NUM_UNK:
                    continue
                edges = self.board.edges[x, y]
                total = edges.edges.count(game.EDGE_1)
                draw_surface_centered(
                    self.virtual_canvas,
                    get_font(NUM_SIZE).render(
                        str(num),
                        True,
                        COLOR_NUM_BAD if num != total else COLOR_NUM_GOOD,
                    ),
                    self.virtual_view.map(Point(x, y)),
                    self.virtual_view.map(Point(x + 1, y + 1)),
                )

    def draw_vertices(self) -> None:
        # r = round(self.view.zoom_k * VERTEX_SIZE / 2) * 2 + 2
        for y in range(self.board.y + 1):
            for x in range(self.board.x + 1):
                total = self.board.vertices[x, y].edges.count(game.EDGE_1)
                pg.draw.circle(
                    self.virtual_canvas,
                    COLOR_VTX_GOOD if total <= 2 else COLOR_VTX_BAD,
                    self.virtual_view.map(Point(x, y)).round(),
                    VERTEX_SIZE,
                )

    def draw_edges(self) -> None:
        b = self.board

        xmin, ymin = self.view.unmap(Point.p00).trunc()
        xmin = max(0, xmin)
        ymin = max(0, ymin)

        xmax, ymax = self.view.unmap(Point.from_tuple(self.screen.get_size())).trunc()
        xmax = min(b.x + 1, xmax + 1)
        ymax = min(b.y + 1, ymax + 1)

        for y in range(ymin, ymax):
            for x in range(xmin, xmax):
                state = self.board.edges[x, y].left
                color = state2color[state]
                if state == game.EDGE_0:
                    continue
                if state == game.EDGE_UNK:
                    draw_dashed_line(
                        self.virtual_canvas,
                        color,
                        self.virtual_view.map(Point(x, y)) - Point.p11,
                        self.virtual_view.map(Point(x, y + 1)) - Point.p11,
                        dash_count=DASHES_CNT,
                        width=LINE_THICKNESS,
                    )
                else:
                    draw_line(
                        self.virtual_canvas,
                        color,
                        self.virtual_view.map(Point(x, y)) - Point.p11,
                        self.virtual_view.map(Point(x, y + 1)) - Point.p11,
                        width=LINE_THICKNESS,
                    )

        for y in range(ymin, ymax):
            for x in range(xmin, xmax):
                state = self.board.edges[x, y].top
                color = state2color[state]
                if state == game.EDGE_0:
                    continue
                if state == game.EDGE_UNK:
                    draw_dashed_line(
                        self.virtual_canvas,
                        color,
                        self.virtual_view.map(Point(x, y)) - Point.p11,
                        self.virtual_view.map(Point(x + 1, y)) - Point.p11,
                        dash_count=DASHES_CNT,
                        width=LINE_THICKNESS,
                    )
                else:
                    draw_line(
                        self.virtual_canvas,
                        color,
                        self.virtual_view.map(Point(x, y)) - Point.p11,
                        self.virtual_view.map(Point(x + 1, y)) - Point.p11,
                        width=LINE_THICKNESS,
                    )


if __name__ == '__main__':
    b = game.make_random_board(15)
    print(b)
    App(b).main_loop()
