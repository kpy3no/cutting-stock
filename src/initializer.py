import numpy as np
from src.entities import Point, Rectangle, Line


class FigureInitializer:
    def __init__(self, count=100, a_width=6, a_height=5, varians=2, space_max_x=1000, space_max_y=1000, max_iterations=1000000):
        assert count > 1 and a_width > 1 and a_height > 1 and varians > 0
        self.count = count
        self.a_width = a_width
        self.a_height = a_height
        self.varians = varians
        self.figures = []
        self.space_max_x = space_max_x
        self.space_max_y = space_max_y
        self.max_iterations = max_iterations

    def generate_rectangles(self):
        widths, heights = self.random_size()
        for width, height in zip(widths, heights):
            if width < 1:
                width = 1
            if height < 1:
                height = 1
            self.insert_figure_random(int(width), int(height))

    def random_size(self):
        random_width = np.round(np.random.normal(loc=self.a_width, scale=self.varians, size=self.count))
        random_height = np.round(np.random.normal(loc=self.a_height, scale=self.varians, size=self.count))
        return random_width, random_height

    def insert_figure_random(self, width, height):
        for x in range(self.max_iterations):
            start_point = Point(np.random.randint(0, self.space_max_x - (self.a_width + self.varians + 1)),
                           np.random.randint(0, self.space_max_y - (self.a_height + self.varians + 1)))
            target_rectangle = Rectangle(start_point, width, height)
            # target_points = get_points(target_rectangle)

            can = True

            for rectangle in self.figures:
                # source_points = get_points(rectangle)
                if doOverlap(rectangle.leftPoint, rectangle.rightPoint, target_rectangle.leftPoint, target_rectangle.rightPoint):
                    can = False
                    break
            if can:
                self.figures.append(target_rectangle)
                return


def get_points(rectangle):
    source_points_x = range(rectangle[0][0], rectangle[0][0] + rectangle[1], 1)
    source_points_y = range(rectangle[0][1], rectangle[0][1] + rectangle[2], 1)
    return source_points_x, source_points_y


def can_insert(source_points, target_points):
    intersect_x = intersection(target_points[0], source_points[0])
    intersect_y = intersection(target_points[1], source_points[1])

    len_intersect_x = len(intersect_x)
    len_intersect_y = len(intersect_y)

    len_target_x = len(target_points[0])
    len_target_y = len(target_points[1])

    len_source_x = len(source_points[0])
    len_source_y = len(source_points[1])

    same = len_source_x == len_target_x and len_source_y == len_target_y and len_intersect_x == len_target_x and len_intersect_y == len_target_y
    full = len_target_x == len_intersect_x and len_target_y == len_intersect_y
    border = (len_intersect_x == len_target_x and len_target_y == 1) or (len_intersect_y == len_target_y and len_target_y == 1)
    not_intersect = 1 >= len_intersect_x or 1 >= len_intersect_y

    if not same and (full or border or not_intersect):
        can = True
    else:
        can = False

    return can


def doOverlap(l1, r1, l2, r2):
    # If one rectangle is on left side of other
    if(l1.x >= r2.x or l2.x >= r1.x):
        return False

    # If one rectangle is above other
    if(r1.y <= l2.y or r2.y <= l1.y):
        return False

    # If the same
    if l1.x == l2.x and r1.y == r2.y:
        return True
# and l2.y  and r2.y <= r1.y
#     and r2.x <= r1.x
    # If one rectangle inside other
    if(l2.x >= l1.x and r2.y <= r1.y) or (l1.x >= l2.x and r1.y <= r2.y):
        return False

    return True


# пересечение множеств без пограничных значений в 2 списке
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3