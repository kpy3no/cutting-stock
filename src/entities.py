import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def distance(self):
        math.sqrt((self.point1.x - self.point2.x)**2 + (self.point1.y - self.point2.y)**2)


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