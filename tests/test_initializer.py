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


class InitializerTest(unittest.TestCase):
    def setUp(self):
        self.initializer = FigureInitializer(count=2000, space_max_x=500, space_max_y=500)

    def test_generate(self):
        self.initializer.generate_rectangles()

    def test_random_size(self):
        width, height = self.initializer.random_size()
        self.assertEqual(len(width), len(height))
        self.assertTrue(abs(self.initializer.a_width - np.mean(width)) < self.initializer.varians)
        count, bins, ignored = plt.hist(width, 30, density=True)
        plt.plot(bins, 1 / (self.initializer.varians * np.sqrt(2 * np.pi)) *
                 np.exp(- (bins - self.initializer.a_width)**2 / (2 * self.initializer.varians ** 2)), linewidth=2, color='r')

        self.assertTrue(abs(self.initializer.a_height - np.mean(height)) < self.initializer.varians)
        count, bins, ignored = plt.hist(height, 30, density=True)
        plt.plot(bins, 1 / (self.initializer.varians * np.sqrt(2 * np.pi)) *
                 np.exp(- (bins - self.initializer.a_height)**2 / (2 * self.initializer.varians ** 2)), linewidth=2, color='r')
        plt.show()

    def test_doOverlap(self):
        source = Point(0, 0), Point(5, 5)
        same = Point(0, 0), Point(5, 5)
        border_intersect = Point(0, 5), Point(1, 6)
        no_intersect = Point(6, 6), Point(10, 10)
        full_intersect = Point(0, 0), Point(3, 3)
        intersect = Point(4, 4), Point(6, 6)

        problem_source_point = Point(0, 2), Point(6, 8)
        problem_point = Point(0, 2), Point(7, 4)
        self.assertTrue(initializer.doOverlap(problem_source_point[0], problem_source_point[1], problem_point[0], problem_point[1]))

        self.assertTrue(initializer.doOverlap(source[0], source[1], intersect[0], intersect[1]))
        self.assertFalse(initializer.doOverlap(source[0], source[1], no_intersect[0], no_intersect[1]))

        self.assertTrue(initializer.doOverlap(source[0], source[1], same[0], same[1]))
        self.assertFalse(initializer.doOverlap(source[0], source[1], border_intersect[0], border_intersect[1]))
        self.assertFalse(initializer.doOverlap(source[0], source[1], full_intersect[0], full_intersect[1]))

    def test_generate_figures(self):
        rectangles = self.initializer.generate_rectangles()
        utils.draw_plot(utils.rectangles_to_math_rectangle(rectangles), self.initializer.space_max_x)
        print('count {0}'.format(self.initializer.count))
        utils.write_rectangles(rectangles)


if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)
