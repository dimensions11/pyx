import unittest

from pyx import *
from pyx.graph import tick, rationaltexter, decimaltexter, exponentialtexter, defaulttexter


class TexterTestCase(unittest.TestCase):
    # TODO: test all combinations (silly work)

    def testFrac(self):
        ticks = [graph.tick((1, 4), labellevel=0), graph.tick((2, 4), labellevel=0)]
        rationaltexter(enumsuffix=r"\pi").labels(ticks)
        assert [tick.label for tick in ticks] == [r"{{\pi}\over{4}}", r"{{\pi}\over{2}}"]
        ticks = [graph.tick((0, 3), labellevel=0), graph.tick((3, 3), labellevel=0), graph.tick((6, 3), labellevel=0)]
        rationaltexter(enumsuffix=r"\pi").labels(ticks)
        assert [tick.label for tick in ticks] == ["0", r"\pi", r"2\pi"]
        ticks = [graph.tick((2, 3), labellevel=0), graph.tick((4, 5), labellevel=0)]
        rationaltexter(enumsuffix=r"\pi", equaldenom=1).labels(ticks)
        assert [tick.label for tick in ticks] == [r"{{10\pi}\over{15}}", r"{{12\pi}\over{15}}"]

    def testDec(self):
        ticks = [graph.tick((1, 4), labellevel=0), graph.tick((2, 4), labellevel=0)]
        decimaltexter().labels(ticks)
        assert [tick.label for tick in ticks] == ["0.25", "0.5"]
        ticks = [graph.tick((1, 4), labellevel=0), graph.tick((2, 4), labellevel=0)]
        decimaltexter(equalprecision=1).labels(ticks)
        assert [tick.label for tick in ticks] == ["0.25", "0.50"]
        ticks = [graph.tick((1, 17), labellevel=0), graph.tick((17, 17), labellevel=0)]
        decimaltexter().labels(ticks)
        assert [tick.label for tick in ticks] == [r"0.\overline{0588235294117647}", "1"]
        ticks = [graph.tick((1, 10000000), labellevel=0), graph.tick((1, 100000000), labellevel=0), graph.tick((1, 1000000000), labellevel=0)]
        decimaltexter(thousandthpartsep=",").labels(ticks)
        assert [tick.label for tick in ticks] == ["0.000,000,1", "0.000,000,01", "0.000,000,001"]
        ticks = [graph.tick((1000000, 1), labellevel=0), graph.tick((10000000, 1), labellevel=0), graph.tick((100000000, 1), labellevel=0)]
        decimaltexter(thousandsep=",").labels(ticks)
        assert [tick.label for tick in ticks] == ["1,000,000", "10,000,000", "100,000,000"]

    def testExp(self):
        ticks = [graph.tick((-1, 10), labellevel=0), graph.tick((1, 1), labellevel=0), graph.tick((10, 1), labellevel=0)]
        exponentialtexter().labels(ticks)
        assert [tick.label for tick in ticks] == [r"{-10^{-1}}", r"{10^{0}}", r"{10^{1}}"]
        ticks = [graph.tick((0, 1), labellevel=0), graph.tick((1, -10), labellevel=0), graph.tick((15, 100), labellevel=0)]
        exponentialtexter(mantissatexter=decimaltexter(equalprecision=1)).labels(ticks)
        assert [tick.label for tick in ticks] == [r"{{0.0}\cdot10^{0}}", r"{{-1.0}\cdot10^{-1}}", r"{{1.5}\cdot10^{-1}}"]

    def testDefault(self):
        ticks = [graph.tick((0, 10), labellevel=0), graph.tick((1, 10), labellevel=0), graph.tick((1, 1), labellevel=0), graph.tick((10, 1), labellevel=0)]
        defaulttexter().labels(ticks)
        assert [tick.label for tick in ticks] == ["0", "0.1", "1", "10"]
        ticks = [graph.tick((0, 10), labellevel=0), graph.tick((1, 10), labellevel=0), graph.tick((1, 1), labellevel=0), graph.tick((10000, 1), labellevel=0)]
        defaulttexter().labels(ticks)
        assert [tick.label for tick in ticks] == [r"{{0}\cdot10^{0}}", r"{{1}\cdot10^{-1}}", r"{{1}\cdot10^{0}}", r"{{1}\cdot10^{4}}"]
        ticks = [graph.tick((0, 10), labellevel=0), graph.tick((1, 10), labellevel=0), graph.tick((1, 1), labellevel=0), graph.tick((10000, 1), labellevel=0)]
        defaulttexter(equaldecision=0).labels(ticks)
        assert [tick.label for tick in ticks] == ["0", "0.1", "1", r"{10^{4}}"]


suite = unittest.TestSuite((unittest.makeSuite(TexterTestCase, 'test'),))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)

