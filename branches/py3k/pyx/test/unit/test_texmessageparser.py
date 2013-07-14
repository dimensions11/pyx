import sys
if sys.path[0] != "../..":
    sys.path.insert(0, "../..")

import unittest, warnings, os

from pyx import text, unit

# text.set(texdebug="bla.tex", usefiles=["bla.log"])

class MessageParserTestCase(unittest.TestCase):

    def failUnlessRaisesUserWarning(self, texexpression, warningmessage, textattrs=[], texmessages=[]):
        try:
            warnings.resetwarnings()
            warnings.filterwarnings(action="error")
            text.text(0, 0, texexpression, textattrs=textattrs, texmessages=texmessages)
        except UserWarning as w:
            if str(w) != warningmessage:
                if 0: # turn on for debugging differences
                    print(len(str(w)), len(warningmessage))
                    for i, (c1, c2) in enumerate(list(zip(str(w), warningmessage))):
                        print(c1, end=' ')
                        if c1 != c2:
                            print("difference at position %d" % i)
                            print(ord(c1), ord(c2))
                            break
                raise

    def testWarnings(self):
        self.failUnlessRaisesUserWarning(r"\some \badly \broken \TeX", r"""ignoring all warnings:
*
*! Undefined control sequence.
<argument> \some 
                 \badly \broken \TeX 
<*> }{1}
        %
! Undefined control sequence.
<argument> \some \badly 
                        \broken \TeX 
<*> }{1}
        %
! Undefined control sequence.
<argument> \some \badly \broken 
                                \TeX 
<*> }{1}
        %


*

""", texmessages=[text.texmessage.allwarning])
        self.failUnlessRaisesUserWarning(r"\fontseries{invalid}\selectfont{}hello, world", r"""ignoring font warning:
LaTeX Font Warning: Font shape `OT1/cmr/invalid/n' undefined
(Font)              using `OT1/cmr/m/n' instead on input line 0.""", texmessages=[text.texmessage.fontwarning])
        self.failUnlessRaisesUserWarning(r"hello, world", r"""ignoring overfull/underfull box warning:
Overfull \hbox (8.22089pt too wide) detected at line 0
[]\OT1/cmr/m/n/10 hello,""", textattrs=[text.parbox(30*unit.u_pt)])
        self.failUnlessRaisesUserWarning(r"\hbadness=0hello, world, hello", r"""ignoring overfull/underfull box warning:
Underfull \hbox (badness 171) detected at line 0
[]\OT1/cmr/m/n/10 hello, world,""", textattrs=[text.parbox(2.5)])
        self.failUnlessRaisesUserWarning(r"\parindent=0pt\vbox to 1cm {hello, world, hello, world, hello, world}", r"""ignoring overfull/underfull box warning:
Overfull \vbox (2.4917pt too high) detected at line 0""", textattrs=[text.parbox(1.9)])
        self.failUnlessRaisesUserWarning(r"\parindent=0pt\vbox to 1cm {hello, world, hello, world}", r"""ignoring overfull/underfull box warning:
Underfull \vbox (badness 10000) detected at line 0""", textattrs=[text.parbox(1.9)])

    def testLoadLongFileNames(self):
        testfilename = "x"*100
        f = open(testfilename + ".tex", "w")
        f.write("\message{ignore this}")
        f.close()
        text.text(0, 0, "\\input %s\n" % testfilename, texmessages=[text.texmessage.load])
        os.remove(testfilename + ".tex")
        f = open(testfilename + ".eps", "w")
        f.write("%%BoundingBox: 0 0 10 10")
        f.close()
        text.text(0, 0, r"\includegraphics{%s}" % testfilename)
        os.remove(testfilename + ".eps")

    def setUp(self):
        text.set(mode="latex")
        text.reset()
        text.preamble(r"\usepackage{graphicx}")

    def tearDown(self):
        try:
            warnings.resetwarnings()
            warnings.filterwarnings(action="error")
            text.defaulttexrunner.finishdvi()
        except UserWarning as w:
            if str(w) != """ignoring font warning:
LaTeX Font Warning: Some font shapes were not available, defaults substituted.""":
                raise


if __name__ == "__main__":
    unittest.main()