import pygame as pg

from point import Point


class View:
    '''
    maps coordinates between logic points and image points
    '''

    # logic coordinate of (0,0) image point
    pos: Point
    # image size relative to logic size
    zoom_k: float

    def __init__(
        self,
        zoom: float,
        pos: Point,
    ) -> None:
        self.zoom_k = zoom
        self.pos = pos

    def map(self, pos: Point, /) -> Point:
        '''logic -> image'''
        return (pos - self.pos) * self.zoom_k

    def unmap(self, pos: Point, /) -> Point:
        '''image -> logic'''
        return pos / self.zoom_k + self.pos

    def zoom(
        self,
        pos: Point,
        scale: float, # >1 to zoom into image, 0<x<1 to zoom out of image
        /,
    ) -> None:
        p = self.unmap(pos)
        self.pos, self.zoom_k = p - (p - self.pos) / scale, self.zoom_k * scale
