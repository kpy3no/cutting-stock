import sys

import src.initializer as utils
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
        self.initializer = FigureInitializer()

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

    def test_intersection(self):
        source = range(0, 5, 1)
        same = range(0, 5, 1)
        border_intersect = range(5, 10, 1)
        no_intersect = range(6, 10, 1)
        full_intersect = range(0, 5, 1)
        intersect = range(2, 3, 1)

        self.assertEqual(len(same), len(utils.intersection(same, source)))
        self.assertFalse(0, len(utils.intersection(border_intersect, source)))
        self.assertFalse(0, len(utils.intersection(no_intersect, source)))
        self.assertEqual(len(full_intersect), len(utils.intersection(full_intersect, source)))
        self.assertTrue(0 < len(utils.intersection(intersect, source)))

    def test_can_insert(self):
        source = range(0, 5, 1), range(0, 5, 1)
        same = range(0, 5, 1), range(0, 5, 1)
        border_intersect = range(0, 5, 1), range(5, 10, 1)
        no_intersect = range(6, 10, 1), range(6, 10, 1)
        full_intersect = range(2, 4, 1), range(2, 4, 1)
        intersect = range(4, 7, 1), range(4, 7, 1)

        self.assertFalse(utils.can_insert(source, same))
        self.assertTrue(utils.can_insert(source, border_intersect))
        self.assertTrue(utils.can_insert(source, no_intersect))
        self.assertTrue(utils.can_insert(source, full_intersect))
        self.assertFalse(utils.can_insert(source, intersect))

    def test_doOverlap(self):
        source = Point(0, 0), Point(5, 5)
        same = Point(0, 0), Point(5, 5)
        border_intersect = Point(0, 5), Point(1, 6)
        no_intersect = Point(6, 6), Point(10, 10)
        full_intersect = Point(0, 0), Point(3, 3)
        intersect = Point(4, 4), Point(6, 6)

        self.assertTrue(utils.doOverlap(source[0], source[1], intersect[0], intersect[1]))
        self.assertFalse(utils.doOverlap(source[0], source[1], no_intersect[0], no_intersect[1]))

        self.assertTrue(utils.doOverlap(source[0], source[1], same[0], same[1]))
        self.assertFalse(utils.doOverlap(source[0], source[1], border_intersect[0], border_intersect[1]))
        self.assertFalse(utils.doOverlap(source[0], source[1], full_intersect[0], full_intersect[1]))


if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)
