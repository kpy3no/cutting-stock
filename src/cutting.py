#!/usr/bin/python
# encoding=utf8

import time
import numpy as np
import src.utils as utils
import matplotlib.pyplot as plt
import matplotlib._pylab_helpers

from matplotlib.collections import PatchCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle as MatRectangle
from src.entities import Point, Rectangle, Line, Result


class RandomAlgorithm:

    def __init__(self, start_point, figures):
        self.start_point = start_point
        self.currentPoint = start_point
        self.figures = figures
        self.left_figures = figures.copy()
        self.point_routes = [start_point]
        self.routes = []

    def generate_routes(self):
        start_time = time.time()
        np.random.shuffle(self.left_figures)
        for figure in self.left_figures:
            self.currentPoint = utils.closest_border_rectangle_point(self.currentPoint, figure)
            self.point_routes.append(self.currentPoint)
            self.routes.append(figure)
        return Result('random',
                      self.figures,
                      self.routes,
                      self.point_routes,
                      value_function(self.figures, self.point_routes),
                      sum_rectangles(self.figures),
                      sum_routes(self.point_routes),
                      time.time() - start_time)


class GreedyAlgorithm:

    def __init__(self, start_point, figures):
        self.start_point = start_point
        self.currentPoint = start_point
        self.figures = figures
        self.left_figures = figures.copy()
        self.point_routes = [start_point]
        self.routes = []

    def generate_routes(self):
        start_time = time.time()
        left_figures = self.left_figures
        while len(left_figures) > 1:
            closest_point = utils.closest_border_rectangle_point(self.currentPoint, left_figures[0])
            closest_distance = self.currentPoint.distance_to(closest_point)
            closest_figure = left_figures[0]
            for figure in left_figures:
                point_to_figure = utils.closest_border_rectangle_point(self.currentPoint, figure)
                distance = self.currentPoint.distance_to(point_to_figure)

                if distance < closest_distance:
                    closest_distance = distance
                    closest_figure = figure
                    closest_point = point_to_figure

            self.point_routes.append(closest_point)
            self.routes.append(closest_figure)
            left_figures.remove(closest_figure)

        return Result('Жадный',
                      self.figures,
                      self.routes,
                      self.point_routes,
                      value_function(self.figures, self.point_routes),
                      sum_rectangles(self.figures),
                      sum_routes(self.point_routes),
                      time.time() - start_time)
# class Audit:
#     def __init__(self, method):
#         self.overallTime = 0
#         self.decisions = {}
#         self.method = method
#         self.figures = {'rectangle'}
#
#
# class CuttingStock:
#     def __init__(self, rectangles, lines=None):
#         if lines is None:
#             lines = []
#         self.rectangles = rectangles
#         self.lines = lines
#
#     def add_line(self, point1, point2):
#         self.lines.append(Line(point1, point2))
#
#     def remove_line(self, point1, point2):
#         self.lines.append(Line(point1, point2))


def sum_rectangles(figures):
    sum_distance = 0

    for rectangle in figures:
        sum_distance += rectangle.perimeter()

    return sum_distance


def sum_routes(routes):
    sum_distance = 0

    for i in range(len(routes) - 1):
        sum_distance += routes[i].distance_to(routes[i+1])
    return sum_distance


def value_function(figures, routes):
    return sum_rectangles(figures) + sum_routes(routes)


def analyze(in_result):
    print(in_result)
    utils.draw_figures(in_result.figures, in_result.point_routes, 100, in_result)


if __name__ == "__main__":
    rectangles = utils.read_rectangles('../data/rectangles_file.csv')
    startPoint = Point(0, 0)

    # random_algorithm = RandomAlgorithm(startPoint, rectangles)
    # result = random_algorithm.generate_routes()
    # analyze(result)

    greedy_algorithm = GreedyAlgorithm(startPoint, rectangles)
    result = greedy_algorithm.generate_routes()
    analyze(result)
