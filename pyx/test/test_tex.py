#!/usr/bin/env python 
import sys
sys.path.append("..")
from pyx import *

c=canvas.canvas()
t=c.insert(tex.tex())

t.text(0, 0, "Hello, world!")
print "width of 'Hello, world!': ", t.textwd("Hello, world!")
print "height of 'Hello, world!': ", t.textht("Hello, world!")
print "depth of 'Hello, world!': ", t.textdp("Hello, world!")

c.writetofile("test_tex")

c=canvas.canvas()
t=c.insert(tex.latex())
c.draw(path.rect(0, 0, 22, 1))
t.text(0, 0, r"""\linewidth22cm\begin{itemize}
\item This is an example. This is an example. This is an example.
      This is an example. This is an example. This is an example.
      This is an example. This is an example. This is an example.
      This is an example. This is an example. This is an example.
\item This is an example. This is an example. This is an example.
      This is an example. This is an example. This is an example.
      This is an example. This is an example. This is an example.
      This is an example. This is an example. This is an example.
\end{itemize}""", tex.vbox(22))
c.writetofile("test_tex2")
