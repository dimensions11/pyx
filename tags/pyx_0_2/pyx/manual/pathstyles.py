#!/usr/bin/env python
import sys
sys.path.append("..")
from pyx import *

c = canvas.canvas()
t = tex.latex()
t.define(r"\renewcommand{\familydefault}{\ttdefault}")

# positioning is quite ugly ... but it works at the moment
x = 0
y = 0
dx = 6
dy = -0.65
length = 0.8

def drawstyle(name, showpath=0, default=0):
    global x,y
    p = path.path(path.moveto(x + 0.1, y+0.1 ),
                       path.rlineto(length/2.0, 0.3),
                       path.rlineto(length/2.0, -0.3))
    c.stroke(p, canvas.linewidth.THIck,  eval("canvas."+name))
    if showpath:
        c.stroke(p, canvas.linewidth.Thin, color.gray.white)
    if default:
        name = name + r"\rm\quad (default)"
    t.text(x + 1.5, y + 0.15, name, tex.fontsize.footnotesize)
    y += dy
    if y < -16:
        y = 0
        x += dx

drawstyle("linecap.butt", showpath=1, default=1)
drawstyle("linecap.round", showpath=1)
drawstyle("linecap.square", showpath=1)

y += dy

drawstyle("linejoin.miter", showpath=1, default=1)
drawstyle("linejoin.round", showpath=1)
drawstyle("linejoin.bevel", showpath=1)

y += dy

drawstyle("linestyle.solid", default=1)
drawstyle("linestyle.dashed")
drawstyle("linestyle.dotted")
drawstyle("linestyle.dashdotted")

y += dy

drawstyle("linewidth.THIN")
drawstyle("linewidth.THIn")
drawstyle("linewidth.THin")
drawstyle("linewidth.Thin")
drawstyle("linewidth.thin")
drawstyle("linewidth.normal", default=1)
drawstyle("linewidth.thick")
drawstyle("linewidth.Thick")
drawstyle("linewidth.THick")
drawstyle("linewidth.THIck")
drawstyle("linewidth.THICk")
drawstyle("linewidth.THICK")

drawstyle("miterlimit.lessthan180deg", showpath=1)
drawstyle("miterlimit.lessthan90deg", showpath=1)
drawstyle("miterlimit.lessthan60deg", showpath=1)
drawstyle("miterlimit.lessthan45deg", showpath=1)
drawstyle("miterlimit.lessthan11deg", showpath=1, default=1)

y += dy

drawstyle("dash((1, 1, 2, 2, 3, 3), 0)")
drawstyle("dash((1, 1, 2, 2, 3, 3), 1)")
drawstyle("dash((1, 2, 3), 2)")
drawstyle("dash((1, 2, 3), 3)")
drawstyle("dash((1, 2, 3), 4)")

y += dy

drawstyle("earrow.SMall")
drawstyle("earrow.Small")
drawstyle("earrow.small")
drawstyle("earrow.normal")
drawstyle("earrow.large")
drawstyle("earrow.Large")
drawstyle("earrow.LArge")

y += dy

drawstyle("barrow.normal")

c.insert(t)
c.writetofile("pathstyles")