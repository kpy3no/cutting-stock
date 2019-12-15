#!/usr/bin/python
# encoding=utf8


import matplotlib.pyplot as plt
import matplotlib._pylab_helpers
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle as MatRectangle
from random import random
from src.entities import Point, Rectangle, Line



# Каретка
class Carriage:
    def __init__(self, start_point, algorithm):
        self.currentPoint = start_point
        self.algorithm = algorithm
        self.passedRoute = {}

    # def go_to(self, point):
#         нари


class Audit:
    def __init__(self, method):
        self.overallTime = 0
        self.decisions = {}
        self.method = method
        self.figures = {'rectangle'}


class CuttingStock:
    def __init__(self, rectangles, lines=None):
        if lines is None:
            lines = []
        self.rectangles = rectangles
        self.lines = lines

    def add_line(self, point1, point2):
        self.lines.append(Line(point1, point2))

    def remove_line(self, point1, point2):
        self.lines.append(Line(point1, point2))


def goal_function(rectangles, lines):
    sum_distance = 0

    for rectangle in rectangles:
        sum_distance += rectangle.perimeter()
    for line in lines:
        sum_distance += line.distance()
    return sum_distance


def draw(rectangles, lines):
    figures = []
    figures += list(map(convert_rectangle, rectangles))
    figures += list(map(convert_line, lines))
    draw_plot(figures)


def convert_rectangle(rectangle):
    return MatRectangle(xy=(rectangle.leftPoint.x, rectangle.leftPoint.y), width=rectangle.width, height=rectangle.height)


def convert_line(line):
    return Line2D(xdata=[line.point1.x, line.point2.x], ydata=[line.point1.y, line.point2.y])

# def convert_rectangles(rectangles):


def random_init_pro(count, a_width, a_height, dispersion):
    assert count > 1 and a_width > 1 and a_height > 1 and dispersion > 0

    figures = []

    figures.append(MatRectangle((0, 1), 5, 5))
    figures.append(MatRectangle((5, 5), 5, 5))

    # figures.append(Line2D([0, 5], [0, 5]))

    draw_plot(figures)


def random_init():
    figures = []

    figures.append(MatRectangle((0, 1), 5, 5))
    figures.append(MatRectangle((5, 5), 5, 5))

    figures.append(Line2D([0, 5], [0, 5]))

    draw_plot(figures)

def draw_plot(figures):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Major ticks every 20, minor ticks every 5
    major_ticks = np.arange(0, 101, 20)
    minor_ticks = np.arange(0, 101, 5)

    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
    # And a corresponding grid
    ax.grid(which='both')
    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    # plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    plt.title('Фигуры раскроя')

    pc = PatchCollection(figures, facecolor='r', alpha=0.5,
                         edgecolor='Black')
    ax.add_collection(pc)
    plt.show()

    return ax, fig


def analyze():
    figures=[manager.canvas.figure
             for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
    print(figures)


if __name__ == "__main__":
    random_init()
    analyze()