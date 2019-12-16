import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, obj):
        return isinstance(obj, Point) and obj.x == self.x and obj.y == self.y

    def __sub__(self, p):
        """Point(x1-x2, y1-y2)"""
        return Point(self.x - p.x, self.y - p.y)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance_to(self, p):
        """Calculate the distance between two points."""
        return (self - p).length()

    def as_tuple(self):
        """(x, y)"""
        return self.x, self.y

    def clone(self):
        """Return a full copy of this point."""
        return Point(self.x, self.y)

    def integerize(self):
        """Convert co-ordinate values to integers."""
        self.x = int(self.x)
        self.y = int(self.y)

    def floatize(self):
        """Convert co-ordinate values to floats."""
        self.x = float(self.x)
        self.y = float(self.y)

    def move_to(self, x, y):
        """Reset x & y coordinates."""
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def distance(self):
        math.sqrt((self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2)


class Rectangle:
    def __init__(self, left_point, width, height):
        # left-bottom point
        self.leftPoint = left_point
        self.width = width
        self.height = height
        # right-top point
        self.rightPoint = Point(left_point.x + width, left_point.y + height)

    def perimeter(self):
        return (self.width + self.height) * 2

    def is_inside(self, point):
        return self.leftPoint.x < point.x < self.rightPoint.x \
               and self.leftPoint.y < point.y < self.rightPoint.y

    def is_belongs(self, point):
        return self.leftPoint.x <= point.x <= self.rightPoint.x \
               and self.leftPoint.y <= point.y <= self.rightPoint.y


class Result:
    def __init__(self, method, figures, routes, point_routes, overall_value, figures_value, routes_value, time=None, operations=None):
        self.method = method
        self.figures = figures
        self.routes = routes
        self.point_routes = point_routes
        self.overall_sum = overall_value
        self.figures_sum = figures_value
        self.routes_sum = routes_value
        self.time = time
        self.operations = operations

    def __str__(self):
        return 'method={0}; count of the figures={1}; chosen routes count{2}; chosen points in routes{3}; overall_value={4}; figure_value={5}; routes_value={6}; time={7}'\
            .format(self.method, len(self.figures), len(self.routes), '', self.overall_sum, self.figures_sum, self.routes_sum, self.time)
