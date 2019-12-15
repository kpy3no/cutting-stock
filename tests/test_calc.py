import sys

from src.cutting import *
import src.cutting

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


class CalculatorTest(unittest.TestCase):
    def setUp(self):
        self.rectangles = [Rectangle(Point(0, 1), 5, 5), Rectangle(Point(5, 5), 5, 5)]
        self.lines = [Line(Point(5, 5), Point(10, 10))]

    def test_draw(self):
        draw(self.rectangles, self.lines)



if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)
