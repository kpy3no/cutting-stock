import sys

import src.initializer as initializer
import src.utils as utils
from src.initializer import FigureInitializer
from src.entities import Point, Rectangle
import numpy as np
import src.cutting
import matplotlib.pyplot as plt

# Attempt to use back-ported unittest2 for Python 2.6 and earlier
# However, it is strongly recommended to use Python 2.7 or 3.<latest>
try:
    if sys.version_info < (2, 7):
        import unittest2
    else:
        raise ImportError()
except ImportError:
    import unittest

NUMBER_1 = 3.0
NUMBER_2 = 2.0
FAILURE = 'incorrect value'


class UtilsTest(unittest.TestCase):
    def test_write_read_rectangles(self):
        rectangles = [Rectangle(Point(0, 0), 10, 10), Rectangle(Point(2, 2), 20, 20)]
        utils.write_rectangles(rectangles)

        csv_rectangles = utils.read_rectangles()
        self.assertEqual(len(rectangles), len(csv_rectangles))

    def test_closest_border_rectangle_point(self):
        rectangle = Rectangle(Point(0, 0), 10, 10)
        point_in = Point(1, 1)
        point_out = Point(20, 20)
        point_in_border = Point(10, 10)

        self.assertEqual(Point(10, 10), utils.closest_border_rectangle_point(point_out, rectangle))
        self.assertEqual(Point(10, 10), utils.closest_border_rectangle_point(point_in_border, rectangle))
        self.assertEqual(Point(0, 1), utils.closest_border_rectangle_point(point_in, rectangle))

    def test_is_inside(self):
        rectangle = Rectangle(Point(0, 0), 10, 10)
        point_in = Point(1, 1)
        point_out = Point(20, 20)
        point_in_border = Point(10, 10)

        self.assertTrue(rectangle.is_inside(point_in))
        self.assertFalse(rectangle.is_inside(point_out))
        self.assertFalse(rectangle.is_inside(point_in_border))

    def test_equal(self):
        self.assertEqual(Point(10, 10), Point(10, 10))
        self.assertNotEqual(Point(10, 10), Point(5, 10))


if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)
