#!/usr/bin/env python
import sys, imp, re
sys.path.append("..")
import pyx
from pyx import *

c = canvas.canvas()
t = tex.latex()
t.define(r"\renewcommand{\familydefault}{\ttdefault}")

# data to be plotted
pf = graph.paramfunction("k", 0, 1, "color, xmin, xmax, ymin, ymax= k, k, 1, 0, 1")

# positioning is quite ugly ... but it works at the moment
y = 0
dy = -0.65

# we could use gradient.__dict__ to get the instances, but we
# would loose the ordering ... instead we just parse the file:
p = re.compile("(?P<id>gradient\\.(?P<name>[a-z]+)) += gradient\\(.*\\)\n", re.IGNORECASE)
lines = imp.find_module("color", pyx.__path__)[0].readlines()
skiplevel = None
for line in lines: # we yet don't use a file iterator
    m = p.match(line)
    if m:
        xaxis = graph.linaxis(datavmin=0, datavmax=1, part=graph.linpart(ticks=("0.5","0.1"), labels="1"),
                              painter=graph.axispainter(innerticklengths=None, labelattrs=None))
        g = c.insert(graph.graphxy(t, ypos=y, width=10, height=0.5, x=xaxis,
                                   x2=graph.linkaxis(xaxis,
                                                     skipticklevel=skiplevel,
                                                     skiplabellevel=skiplevel,
                                                     painter=graph.axispainter(innerticklengths=None,
                                                                               outerticklengths=graph.axispainter.defaultticklengths)),
                                   y=graph.linaxis(datavmin=0, datavmax=1, part=graph.manualpart(ticks=None))))
        g.plot(pf, graph.rect(pyx.color.gradient.__dict__[m.group("name")]))
        g.dodata()
        g.finish()
        t.text(10.2, y + 0.15, m.group("id"), tex.fontsize.footnotesize)
        y += dy
        skiplevel = 0


c.insert(t)
c.writetofile("gradientname", paperformat="a4")