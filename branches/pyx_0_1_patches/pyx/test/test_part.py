#!/usr/bin/env python
import sys, unittest

sys.path.append("..")
from pyx import *
from pyx.graph import frac, tick, manualpart, linpart, logpart


def PartEqual(part1, part2):
     assert len(part1) == len(part2), "partitions have different length"
     for tick1, tick2 in zip(part1, part2):
         assert tick1 == tick2, "position is different"
         assert tick1.ticklevel == tick2.ticklevel, "ticklevel is different"
         assert tick1.labellevel == tick2.labellevel, "labellevel is different"
         assert tick1.text == tick2.text, "text is different"


class ManualPartTestCase(unittest.TestCase):

     def testFrac(self):
         PartEqual(manualpart(ticks=frac(1, 1), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None)])
         PartEqual(manualpart(ticks=frac(2, 2), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None)])
         PartEqual(manualpart(ticks="1", labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None)])
         PartEqual(manualpart(ticks="1/1", labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None)])
         PartEqual(manualpart(ticks="2/2", labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None)])
         PartEqual(manualpart(ticks="0.5/0.5", labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None)])

     def testTicks(self):
         PartEqual(manualpart(ticks="1", labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None)])
         PartEqual(manualpart(ticks=("1",), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None)])
         PartEqual(manualpart(ticks=("1", "2"), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 0, None)])
         PartEqual(manualpart(ticks=("2", "1"), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 0, None)])
         try:
             manualpart(ticks=("1", "1"), labels=()).defaultpart(0, 0, 1, 1)
             raise Exception("exception for duplicate entry expected")
         except ValueError, msg:
             assert msg != "duplicate entry found"
         try:
             manualpart(ticks=("1", "2", "1"), labels=()).defaultpart(0, 0, 1, 1)
             raise Exception("exception for duplicate entry expected")
         except ValueError, msg:
             assert msg != "duplicate entry found"

     def testLabels(self):
         PartEqual(manualpart(labels="1", ticks=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 0)])
         PartEqual(manualpart(labels=("1",), ticks=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 0)])
         PartEqual(manualpart(labels=("1", "2"), ticks=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 0), tick(2, 1, None, 0)])
         PartEqual(manualpart(labels=("2", "1"), ticks=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 0), tick(2, 1, None, 0)])
         try:
             manualpart(labels=("1", "1"), ticks=()).defaultpart(0, 0, 1, 1)
             raise Exception("exception for duplicate entry expected")
         except ValueError, msg:
             assert msg != "duplicate entry found"
         try:
             manualpart(labels=("1", "2", "1"), ticks=()).defaultpart(0, 0, 1, 1)
             raise Exception("exception for duplicate entry expected")
         except ValueError, msg:
             assert msg != "duplicate entry found"

     def testSubTicks(self):
         PartEqual(manualpart(ticks=((), "1"), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 1, None)])
         PartEqual(manualpart(ticks=((), ("1",)), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 1, None)])
         PartEqual(manualpart(ticks=((), ("1", "2")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 1, None), tick(2, 1, 1, None)])
         PartEqual(manualpart(ticks=((), ("2", "1")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 1, None), tick(2, 1, 1, None)])
         try:
             manualpart(ticks=((), ("1", "1")), labels=()).defaultpart(0, 0, 1, 1)
             raise Exception("exception for duplicate entry expected")
         except ValueError, msg:
             assert msg != "duplicate entry found"
         try:
             manualpart(ticks=((), ("1", "2", "1")), labels=()).defaultpart(0, 0, 1, 1)
             raise Exception("exception for duplicate entry expected")
         except ValueError, msg:
             assert msg != "duplicate entry found"

     def testSubLabels(self):
         PartEqual(manualpart(labels=((), "1"), ticks=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 1)])
         PartEqual(manualpart(labels=((), ("1",)), ticks=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 1)])
         PartEqual(manualpart(labels=((), ("1", "2")), ticks=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 1), tick(2, 1, None, 1)])
         PartEqual(manualpart(labels=((), ("2", "1")), ticks=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 1), tick(2, 1, None, 1)])
         try:
             manualpart(labels=((), ("1", "1")), ticks=()).defaultpart(0, 0, 1, 1)
             raise Exception("exception for duplicate entry expected")
         except ValueError, msg:
             assert msg != "duplicate entry found"
         try:
             manualpart(labels=((), ("1", "2", "1")), ticks=()).defaultpart(0, 0, 1, 1)
             raise Exception("exception for duplicate entry expected")
         except ValueError, msg:
             assert msg != "duplicate entry found"

     def testTicksSubticks(self):
         PartEqual(manualpart(ticks=(("1", "2"), ("1", "2")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 0, None)])
         PartEqual(manualpart(ticks=(("1", "2"), ("3", "4")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 0, None), tick(3, 1, 1, None), tick(4, 1, 1, None)])
         PartEqual(manualpart(ticks=(("1", "2"), ("3", "2")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 0, None), tick(3, 1, 1, None)])
         PartEqual(manualpart(ticks=(("1", "3"), ("2", "4")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 1, None), tick(3, 1, 0, None), tick(4, 1, 1, None)])
         PartEqual(manualpart(ticks=(("1", "3"), ("2", "4", "1", "3")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 1, None), tick(3, 1, 0, None), tick(4, 1, 1, None)])

     def testTicksSubsubticks(self):
         PartEqual(manualpart(ticks=(("1", "2"), (), ("1", "2")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 0, None)])
         PartEqual(manualpart(ticks=(("1", "2"), (), ("3", "4")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 0, None), tick(3, 1, 2, None), tick(4, 1, 2, None)])
         PartEqual(manualpart(ticks=(("1", "2"), (), ("3", "2")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 0, None), tick(3, 1, 2, None)])
         PartEqual(manualpart(ticks=(("1", "3"), (), ("2", "4")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 2, None), tick(3, 1, 0, None), tick(4, 1, 2, None)])
         PartEqual(manualpart(ticks=(("1", "3"), (), ("2", "4", "1", "3")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 2, None), tick(3, 1, 0, None), tick(4, 1, 2, None)])
         PartEqual(manualpart(ticks=(("1", "3"), "2", ("2", "4", "1", "3")), labels=()).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, None), tick(2, 1, 1, None), tick(3, 1, 0, None), tick(4, 1, 2, None)])

     def testTickLabels(self):
         PartEqual(manualpart(ticks="1").defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, 0)])
         PartEqual(manualpart(ticks=("1",)).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, 0)])
         PartEqual(manualpart(ticks=("1", "2")).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, 0), tick(2, 1, 0, 0)])
         PartEqual(manualpart(ticks=("2", "1")).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, 0), tick(2, 1, 0, 0)])


     def testText(self):
         PartEqual(manualpart(labels="1", ticks=(), texts="a").defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 0, "a")])
         PartEqual(manualpart(labels="1", ticks=(), texts=("a",)).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 0, "a")])
         PartEqual(manualpart(labels=("1", "2"), ticks=(), texts=("a", "b")).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 0, "a"), tick(2, 1, None, 0, "b")])
         PartEqual(manualpart(labels=("2", "1"), ticks=(), texts=("a", "b")).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, None, 0, "a"), tick(2, 1, None, 0, "b")])
         try:
             manualpart(labels=("1"), ticks=(), texts=("a", "b")).defaultpart(0, 0, 1, 1)
             raise Exception("exception for wrong sequence length of texts expected")
         except IndexError, msg:
             assert msg != "wrong sequence length of texts"

     def testSubtextsAndSubLabelTicks(self):
         PartEqual(manualpart(labels=(("1", "2"), ("1", "2")), texts=("a", "b")).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, 0, "a"), tick(2, 1, 0, 0, "b")])
         PartEqual(manualpart(labels=(("1", "2"), ("3", "4")), texts=("a", "b")).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, 0, "a"), tick(2, 1, 0, 0, "b"), tick(3, 1, None, 1), tick(4, 1, None, 1)])
         PartEqual(manualpart(labels=(("1",), ("2", "3")), texts=(("a",), ("b", "c"))).defaultpart(0, 0, 1, 1),
                   [tick(1, 1, 0, 0, "a"), tick(2, 1, None, 1, "b"), tick(3, 1, None, 1, "c")])


class LinPartTestCase(unittest.TestCase):

     def testAll(self):
         PartEqual(linpart(ticks="1", labels=()).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0), tick(1, 1, 0)])
         PartEqual(linpart(ticks=("1", "0.5"), labels=()).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0), tick(1, 2, 1), tick(1, 1, 0)])
         PartEqual(linpart(ticks=("1", "0.5", "0.25"), labels=()).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0), tick(1, 4, 2), tick(1, 2, 1), tick(3, 4, 2), tick(1, 1, 0)])
         PartEqual(linpart(ticks=("1", "0.5"), labels=(), extendtick=None).defaultpart(0, 1.5, 1, 1),
                   [tick(0, 1, 0), tick(1, 2, 1), tick(1, 1, 0), tick(3, 2, 1)])
         PartEqual(linpart(ticks=("1", "0.5"), labels=(), extendtick=1).defaultpart(0, 1.2, 1, 1),
                   [tick(0, 1, 0), tick(1, 2, 1), tick(1, 1, 0), tick(3, 2, 1)])
         PartEqual(linpart(ticks=("1", "0.5"), labels=(), extendtick=0).defaultpart(0, 1.2, 1, 1),
                   [tick(0, 1, 0), tick(1, 2, 1), tick(1, 1, 0), tick(3, 2, 1), tick(2, 1, 0)])
         PartEqual(linpart(labels="1", ticks=()).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, None, 0), tick(1, 1, None, 0)])
         PartEqual(linpart(labels=("1", "0.5"), ticks=()).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, None, 0), tick(1, 2, None, 1), tick(1, 1, None, 0)])
         PartEqual(linpart(labels=("1", "0.5", "0.25"), ticks=()).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, None, 0), tick(1, 4, None, 2), tick(1, 2, None, 1), tick(3, 4, None, 2), tick(1, 1, None, 0)])
         PartEqual(linpart(labels=("1", "0.5"), ticks=(), extendlabel=None).defaultpart(0, 1.5, 1, 1),
                   [tick(0, 1, None, 0), tick(1, 2, None, 1), tick(1, 1, None, 0), tick(3, 2, None, 1)])
         PartEqual(linpart(labels=("1", "0.5"), ticks=(), extendlabel=1).defaultpart(0, 1.2, 1, 1),
                   [tick(0, 1, None, 0), tick(1, 2, None, 1), tick(1, 1, None, 0), tick(3, 2, None, 1)])
         PartEqual(linpart(labels=("1", "0.5"), ticks=(), extendlabel=0).defaultpart(0, 1.2, 1, 1),
                   [tick(0, 1, None, 0), tick(1, 2, None, 1), tick(1, 1, None, 0), tick(3, 2, None, 1), tick(2, 1, None, 0)])
         PartEqual(linpart(ticks="1").defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 1, 0, 0)])
         PartEqual(linpart(ticks=("1", "0.5")).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 2, 1), tick(1, 1, 0, 0)])
         PartEqual(linpart(ticks=("1", "0.5", "0.25")).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 4, 2), tick(1, 2, 1), tick(3, 4, 2), tick(1, 1, 0, 0)])
         PartEqual(linpart(ticks=("1", "0.5"), extendtick=None).defaultpart(0, 1.5, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 2, 1), tick(1, 1, 0, 0), tick(3, 2, 1)])
         PartEqual(linpart(ticks=("1", "0.5"), extendtick=1).defaultpart(0, 1.2, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 2, 1), tick(1, 1, 0, 0), tick(3, 2, 1)])
         PartEqual(linpart(ticks=("1", "0.5"), extendtick=0).defaultpart(0, 1.2, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 2, 1), tick(1, 1, 0, 0), tick(3, 2, 1), tick(2, 1, 0, 0)])
         PartEqual(linpart(labels="1").defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 1, 0, 0)])
         PartEqual(linpart(labels=("1", "0.5")).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 2, None, 1), tick(1, 1, 0, 0)])
         PartEqual(linpart(labels=("1", "0.5", "0.25")).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 4, None, 2), tick(1, 2, None, 1), tick(3, 4, None, 2), tick(1, 1, 0, 0)])
         PartEqual(linpart(labels=("1", "0.5"), extendtick=None).defaultpart(0, 1.5, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 2, None, 1), tick(1, 1, 0, 0), tick(3, 2, None, 1)])
         PartEqual(linpart(labels=("1", "0.5"), extendtick=None, extendlabel=1).defaultpart(0, 1.2, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 2, None, 1), tick(1, 1, 0, 0), tick(3, 2, None, 1)])
         PartEqual(linpart(labels=("1", "0.5"), extendtick=None, extendlabel=0).defaultpart(0, 1.2, 1, 1),
                   [tick(0, 1, 0, 0), tick(1, 2, None, 1), tick(1, 1, 0, 0), tick(3, 2, None, 1), tick(2, 1, 0, 0)])
         PartEqual(linpart(labels="1", texts=("a", "b")).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0, 0, "a"), tick(1, 1, 0, 0, "b")])
         PartEqual(linpart(labels=("1", "0.5"), texts=(("a", "c"), "b")).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0, 0, "a"), tick(1, 2, None, 1, "b"), tick(1, 1, 0, 0, "c")])
         PartEqual(linpart(labels=("1", "0.5", "0.25"), texts=(("a", "e"), "c", ("b", "d"))).defaultpart(0, 1, 1, 1),
                   [tick(0, 1, 0, 0, "a"), tick(1, 4, None, 2, "b"), tick(1, 2, None, 1, "c"), tick(3, 4, None, 2, "d"), tick(1, 1, 0, 0, "e")])

class LogPartTestCase(unittest.TestCase):

     def testAll(self):
         PartEqual(logpart(ticks=logpart.shiftfracs1, labels=()).defaultpart(1, 10, 1, 1),
                   [tick(1, 1, 0), tick(10, 1, 0)])
         PartEqual(logpart(ticks=logpart.shiftfracs1, labels=()).defaultpart(1, 100, 1, 1),
                   [tick(1, 1, 0), tick(10, 1, 0), tick(100, 1, 0)])
         PartEqual(logpart(ticks=logpart.shift2fracs1, labels=()).defaultpart(1, 100, 1, 1),
                   [tick(1, 1, 0), tick(100, 1, 0)])
         PartEqual(logpart(ticks=logpart.shiftfracs1to9, labels=()).defaultpart(1, 10, 1, 1),
                   [tick(1, 1, 0), tick(2, 1, 0), tick(3, 1, 0), tick(4, 1, 0), tick(5, 1, 0), tick(6, 1, 0), tick(7, 1, 0), tick(8, 1, 0), tick(9, 1, 0), tick(10, 1, 0)])
         PartEqual(logpart(ticks=(logpart.shiftfracs1, logpart.shiftfracs1to9), labels=()).defaultpart(1, 10, 1, 1),
                   [tick(1, 1, 0), tick(2, 1, 1), tick(3, 1, 1), tick(4, 1, 1), tick(5, 1, 1), tick(6, 1, 1), tick(7, 1, 1), tick(8, 1, 1), tick(9, 1, 1), tick(10, 1, 0)])
         PartEqual(logpart(ticks=(logpart.shiftfracs1, logpart.shiftfracs1to9)).defaultpart(1, 10, 1, 1),
                   [tick(1, 1, 0, 0), tick(2, 1, 1), tick(3, 1, 1), tick(4, 1, 1), tick(5, 1, 1), tick(6, 1, 1), tick(7, 1, 1), tick(8, 1, 1), tick(9, 1, 1), tick(10, 1, 0, 0)])


suite = unittest.TestSuite((unittest.makeSuite(ManualPartTestCase, 'test'),
                            unittest.makeSuite(LinPartTestCase, 'test'),
                            unittest.makeSuite(LogPartTestCase, 'test')))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
