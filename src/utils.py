import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import numpy as np
from matplotlib.patches import Rectangle as MatRectangle
import matplotlib.patches as mpatches
import csv
from src.entities import Rectangle, Point, Result


# Rectangles to matplotlib.patches.Rectangle
def rectangles_to_math_rectangle(rectangles):
    return list(map(convert_rectangle, rectangles))


def convert_rectangle(rectangle):
    return MatRectangle(xy=(rectangle.leftPoint.x, rectangle.leftPoint.y), width=rectangle.width, height=rectangle.height)


def routes_to_points(routes):
    return list(map(lambda point: point.x, routes)), list(map(lambda point: point.y, routes))


def draw_figures(rectangles, points, lim_point=100, result=None):
    # lim_point = max(max(r.rightPoint.x for r in rectangles), max(r.rightPoint.y for r in rectangles))
    draw_plot(rectangles_to_math_rectangle(rectangles), lim_point, routes_to_points(points), result)


def draw_plot(figures, lim_point=100, points=None, result=None):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Major ticks every 20, minor ticks every 5
    major_ticks = np.arange(0, lim_point, lim_point/4)
    minor_ticks = np.arange(0, lim_point, lim_point/20)

    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
    # And a corresponding grid
    ax.grid(which='both')
    ax.set_xlim(0, lim_point)
    ax.set_ylim(0, lim_point)
    # plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    plt.title('Фигуры раскроя')

    pc = PatchCollection(figures, facecolor='r', alpha=0.5,
                         edgecolor='Black')
    pc.set_array(100*np.random.random(100))
    ax.add_collection(pc)

    lbl_str = 'Описание'
    lbl_str += '\n' + 'кол-во фигур={0}'.format(len(figures))

    if result is not None:
        lbl_str += '\n' + 'алгоритм={0}'.format(result.method)
        lbl_str += '\n' + 'требуемое время={:2.3f}'.format(result.time)
        lbl_str += '\n' + 'общая стоимость={:2.3f}'.format(result.overall_sum)
        lbl_str += '\n' + 'стоимость фигур={:2.3f}'.format(result.figures_sum)
        lbl_str += '\n' + 'стоимость маршрута={:2.3f}'.format(result.routes_sum)

    if points is not None:
        plt.plot(points[0], points[1], '-p', color='gray',
                 markersize=5, linewidth=1,
                 markerfacecolor='white',
                 markeredgecolor='gray',
                 markeredgewidth=1)
        lbl_str += '\n' + 'начальная точка={0},{1}'.format(points[0][0], points[1][0])

    red_patch = mpatches.Patch(color='red', label=lbl_str)
    plt.legend(handles=[red_patch], loc='center left', bbox_to_anchor=(1, 0.5))

    plt.show()

    return ax, fig


def write_rectangles(rectangles, path='rectangles_file.csv'):
    with open(path, mode='w') as rectangles_file:
        fieldnames = ['left_bottom_x', 'left_bottom_y', 'width', 'height']
        writer = csv.DictWriter(rectangles_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

        writer.writeheader()
        for rectangle in rectangles:
            writer.writerow({'left_bottom_x': rectangle.leftPoint.x,
                             'left_bottom_y': rectangle.leftPoint.y,
                             'width': rectangle.width,
                             'height': rectangle.height})


def read_rectangles(path='rectangles_file.csv'):
    rectangles = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                rectangles.append(Rectangle(Point(int(row[0]), int(row[1])), int(row[2]), int(row[3])))
                line_count += 1
        print(f'Processed {line_count} lines.')
    return rectangles


def closest_border_rectangle_point(point, rectangle):
    x_points = range(rectangle.leftPoint.x, rectangle.rightPoint.x + 1, 1)
    y_points = range(rectangle.leftPoint.y, rectangle.rightPoint.y + 1, 1)
    closest_x = min(x_points, key=lambda x:abs(x-point.x))
    closest_y = min(y_points, key=lambda y:abs(y-point.y))

    if rectangle.is_inside(point):
        A = Point(rectangle.leftPoint.x, closest_y)
        B = Point(closest_x, rectangle.rightPoint.y)
        C = Point(rectangle.rightPoint.x, closest_y)
        D = Point(closest_x, rectangle.leftPoint.y)
        return find_nearest_point([A, B, C, D], target_point=point)
    else:
        return Point(closest_x, closest_y)


def find_nearest_point(points, target_point):
    nearest_point = points[0]
    nearest_distance = nearest_point.distance_to(target_point)

    for border_point in points[1:]:
        current_border_distance = border_point.distance_to(target_point)
        if current_border_distance < nearest_distance:
            nearest_distance = current_border_distance
            nearest_point = border_point
    return nearest_point
