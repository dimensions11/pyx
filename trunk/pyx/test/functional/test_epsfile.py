#!/usr/bin/env python
import sys; sys.path[:0] = ["../.."]

from pyx import *

c = canvas.canvas()

c.stroke(path.line("10 pt", "10 pt", "40 pt", "40 pt")+
         path.line("10 pt", "40 pt", "40 pt", "10 pt"))
#         path.rect("10 pt", "10 pt", "30 pt", "30 pt"))

c.writetofile("cross", bboxenlarge=0)

c = canvas.canvas()

c.stroke(path.line(0,4,6,4), style.linestyle.dashed)
c.insert(epsfile.epsfile(0, 4, "cross.eps", align="bl", showbbox=1))
c.insert(epsfile.epsfile(2, 4, "cross.eps", align="cl", showbbox=1))
c.insert(epsfile.epsfile(4, 4, "cross.eps", align="tl", showbbox=1))

c.stroke(path.line(3,6,3,10), style.linestyle.dashed)
c.insert(epsfile.epsfile(3, 6, "cross.eps", align="bl", showbbox=1))
c.insert(epsfile.epsfile(3, 8, "cross.eps", align="bc", showbbox=1))
c.insert(epsfile.epsfile(3, 10, "cross.eps", align="br", showbbox=1))

c.insert(epsfile.epsfile(1, -1, "cross.eps", scale=1, showbbox=1))
c.insert(epsfile.epsfile(1, -1, "cross.eps", scale=2, showbbox=1))

c.insert(epsfile.epsfile(5, -1, "cross.eps", scale=1, align="cc", showbbox=1))
c.insert(epsfile.epsfile(5, -1, "cross.eps", scale=2, align="cc", showbbox=1))

c.insert(epsfile.epsfile(9, -1, "cross.eps", scale=1, align="tr", showbbox=1))
c.insert(epsfile.epsfile(9, -1, "cross.eps", scale=2, align="tr", showbbox=1))

c.insert(epsfile.epsfile(1, -5, "cross.eps", showbbox=1))
c.insert(epsfile.epsfile(1, -5, "cross.eps", width=2, showbbox=1))

c.insert(epsfile.epsfile(5, -5, "cross.eps", scale=1, align="cc", showbbox=1))
c.insert(epsfile.epsfile(5, -5, "cross.eps", width=2, align="cc", showbbox=1))

c.insert(epsfile.epsfile(9, -5, "cross.eps", scale=1, align="tr", showbbox=1))
c.insert(epsfile.epsfile(9, -5, "cross.eps", width=2, align="tr", showbbox=1))

c.insert(epsfile.epsfile(1, -9, "cross.eps", showbbox=1))
c.insert(epsfile.epsfile(1, -9, "cross.eps", height=1.5, showbbox=1))

c.insert(epsfile.epsfile(5, -9, "cross.eps", scale=1, align="cc", showbbox=1))
c.insert(epsfile.epsfile(5, -9, "cross.eps", height=1.5, align="cc", showbbox=1))

c.insert(epsfile.epsfile(9, -9, "cross.eps", scale=1, align="tr", showbbox=1))
c.insert(epsfile.epsfile(9, -9, "cross.eps", height=1.5, align="tr", showbbox=1))

c.insert(epsfile.epsfile(1, -13, "cross.eps", showbbox=1))
c.insert(epsfile.epsfile(1, -13, "cross.eps", width=2, height=1.5, showbbox=1))

c.insert(epsfile.epsfile(5, -13, "cross.eps", scale=1, align="cc", showbbox=1))
c.insert(epsfile.epsfile(5, -13, "cross.eps", width=2,height=1.5, align="cc", showbbox=1))

c.insert(epsfile.epsfile(9, -13, "cross.eps", scale=1, align="tr", showbbox=1))
c.insert(epsfile.epsfile(9, -13, "cross.eps", width=2, height=1.5, align="tr", showbbox=1))

c.writetofile("test_epsfile")
