#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2005 J�rg Lehmann <joergl@users.sourceforge.net>
# Copyright (C) 2005 Andr� Wobst <wobsta@users.sourceforge.net>
#
# This file is part of PyX (http://pyx.sourceforge.net/).
#
# PyX is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyX; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import time
import resource, style, version
import pykpathsea, t1strip

#
# Abstract base class
#

class PSprologitem:

    """Part of the PostScript prolog"""

    def __init__(self, id):
        # every PSprologitem has to have a unique id
        self.id = id

    def outputPS(self, file):
        """ write self in file """
        pass

#
# Different variants of prolog items
#

class PSdefinition(PSprologitem):

    """ PostScript function definition included in the prolog """

    def __init__(self, id, body):
        self.id = id
        self.body = body

    def __str__(self):
        return "PSdefinition(%s)" %  self.id

    def outputPS(self, file):
        file.write("%%%%BeginRessource: %s\n" % self.id)
        file.write("%(body)s /%(id)s exch def\n" % self.__dict__)
        file.write("%%EndRessource\n")


class PSfontfile(PSprologitem):

    """ PostScript font definition included in the prolog """

    def __init__(self, font, fontname, filename, encfilename, usedchars):
        """ include type 1 font defined by the following parameters

        - fontname:    PostScript FontName of font
        - filename:    name (without path) of file containing the font definition
        - encfilename: name (without path) of file containing used encoding of font
                       or None (if no encoding file used)
        - usechars:    list with 256 elements containing used charcodes of font

        """

        # Note that here we only need the encoding for selecting the used glyphs!

        # XXX rewrite

        self.font = font
        self.id = self.fontname = fontname
        self.filename = filename
        self.encfilename = encfilename
        self.usedchars = usedchars

    def __str__(self):
        return "PSfont(%s)" %  self.fontname

    def outputPS(self, file):
        if self.filename:
            file.write("%%%%BeginFont: %s\n" % self.fontname)
            file.write("%Included char codes:")
            for i in range(len(self.usedchars)):
                if self.usedchars[i]:
                    file.write(" %d" % i)
            file.write("\n")
            pfbpath = pykpathsea.find_file(self.filename, pykpathsea.kpse_type1_format)
            if not pfbpath:
                raise RuntimeError("cannot find type 1 font %s" % self.filename)
            if self.encfilename is not None:
                encpath = pykpathsea.find_file(self.encfilename, pykpathsea.kpse_tex_ps_header_format)
                if not encpath:
                    raise RuntimeError("cannot find font encoding file %s" % self.encfilename)
                t1strip.t1strip(file, pfbpath, self.usedchars, encpath)
            else:
                t1strip.t1strip(file, pfbpath, self.usedchars)
            file.write("%%EndFont\n")


class PSfontencoding(PSprologitem):

    """ PostScript font encoding vector included in the prolog """

    def __init__(self, name, filename):
        """ include font encoding vector specified by

        - name:        name of the encoding
        - filename:    name (without path) of file containing the font encoding

        """

        self.id = self.name = name
        self.filename = filename

    def __str__(self):
        return "PSfontencoding(%s)" %  self.name

    def outputPS(self, file):
        file.write("%%%%BeginProcSet: %s\n" % self.name)
        path = pykpathsea.find_file(self.filename, pykpathsea.kpse_tex_ps_header_format)
        encfile = open(path, "r")
        file.write(encfile.read())
        encfile.close()
        file.write("%%EndProcSet\n")


class PSfontreencoding(PSprologitem):

    """ PostScript font re-encoding directive included in the prolog """

    def __init__(self, fontname, basefontname, encname):
        """ include font re-encoding directive specified by

        - fontname:     PostScript FontName of the new reencoded font
        - basefontname: PostScript FontName of the original font
        - encname:      name of the encoding
        - font:         a reference to the font instance (temporarily added for pdf support)

        Before being able to reencode a font, you have to include the
        encoding via a fontencoding prolog item with name=encname

        """

        self.id = self.fontname = fontname
        self.basefontname = basefontname
        self.encname = encname

    def __str__(self):
        return "PSfontreencoding(%s, %s, %s)" % (self.fontname, self.basefontname, self.encname)

    def outputPS(self, file):
        file.write("%%%%BeginProcSet: %s\n" % self.fontname)
        file.write("/%s /%s %s ReEncodeFont\n" % (self.basefontname, self.fontname, self.encname))
        file.write("%%EndProcSet\n")


_ReEncodeFont = PSdefinition("ReEncodeFont", """{
  5 dict
  begin
    /newencoding exch def
    /newfontname exch def
    /basefontname exch def
    /basefontdict basefontname findfont def
    /newfontdict basefontdict maxlength dict def
    basefontdict {
      exch dup dup /FID ne exch /Encoding ne and
      { exch newfontdict 3 1 roll put }
      { pop pop }
      ifelse
    } forall
    newfontdict /FontName newfontname put
    newfontdict /Encoding newencoding put
    newfontname newfontdict definefont pop
  end
}""")


class epswriter:

    def __init__(self, document, filename):
        if len(document.pages) != 1:
            raise ValueError("EPS file can be construced out of a single page document only")
        page = document.pages[0]
        canvas = page.canvas

        if filename[-4:] != ".eps":
            filename = filename + ".eps"
        try:
            file = open(filename, "w")
        except IOError:
            raise IOError("cannot open output file")

        bbox = canvas.bbox()
        bbox.enlarge(page.bboxenlarge)
        pagetrafo = page.pagetrafo(bbox)

        # if a page transformation is necessary, we have to adjust the bounding box
        # accordingly
        if pagetrafo is not None:
            bbox.transform(pagetrafo)

        file.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        bbox.outputPS(file)
        file.write("%%%%Creator: PyX %s\n" % version.version)
        file.write("%%%%Title: %s\n" % filename)
        file.write("%%%%CreationDate: %s\n" %
                   time.asctime(time.localtime(time.time())))
        file.write("%%EndComments\n")

        file.write("%%BeginProlog\n")
        registry = resource.resourceregistry()
        canvas.registerresources(registry)
        writtenPSprologitemids = []
        for aresource in registry.resources.values():
            for PSprologitem in aresource.PSprolog():
                if PSprologitem.id not in writtenPSprologitemids:
                    PSprologitem.outputPS(file)
                    writtenPSprologitemids.append(PSprologitem.id)
        file.write("%%EndProlog\n")

        # apply a possible page transformation
        if pagetrafo is not None:
            pagetrafo.outputPS(file)

        style.linewidth.normal.outputPS(file)

        # here comes the canvas content
        canvas.outputPS(file)

        file.write("showpage\n")
        file.write("%%Trailer\n")
        file.write("%%EOF\n")


class pswriter:
    pass

#     def outputPS(self, file):
#         file.write("%%%%PageMedia: %s\n" % self.paperformat)
#         file.write("%%%%PageOrientation: %s\n" % (self.rotated and "Landscape" or "Portrait"))
#         # file.write("%%%%PageBoundingBox: %d %d %d %d\n" % (math.floor(pbbox.llx_pt), math.floor(pbbox.lly_pt),
#         #                                                    math.ceil(pbbox.urx_pt), math.ceil(pbbox.ury_pt)))
# 
#         # page setup section
#         file.write("%%BeginPageSetup\n")
#         file.write("/pgsave save def\n")
#         # for scaling, we need the real bounding box of the page contents
#         pbbox = canvas.bbox(self)
#         pbbox.enlarge(self.bboxenlarge)
#         ptrafo = calctrafo(pbbox, self.paperformat, self.margin, self.rotated, self.fittosize)
#         if ptrafo:
#             ptrafo.outputPS(file)
#         file.write("%f setlinewidth\n" % unit.topt(style.linewidth.normal))
#         file.write("%%EndPageSetup\n")
# 
#         # here comes the actual content
#         canvas.outputPS(self, file)
#         file.write("pgsave restore\n")
#         file.write("showpage\n")
#         # file.write("%%PageTrailer\n")


#     def writePSfile(self, filename):
#         """write pages to PS file """
# 
#         if filename[-3:]!=".ps":
#             filename = filename + ".ps"
# 
#         try:
#             file = open(filename, "w")
#         except IOError:
#             raise IOError("cannot open output file")
# 
#         docbbox = None
#         for apage in self.pages:
#             pbbox = apage.bbox()
#             if docbbox is None:
#                 docbbox = pbbox
#             else:
#                 docbbox += pbbox
# 
#         # document header
#         file.write("%!PS-Adobe-3.0\n")
#         docbbox.outputPS(file)
#         file.write("%%%%Creator: PyX %s\n" % version.version)
#         file.write("%%%%Title: %s\n" % filename)
#         file.write("%%%%CreationDate: %s\n" %
#                    time.asctime(time.localtime(time.time())))
#         # required paper formats
#         paperformats = {}
#         for apage in self.pages:
#             if isinstance(apage, page):
#                 paperformats[apage.paperformat] = _paperformats[apage.paperformat]
#         first = 1
#         for paperformat, size in paperformats.items():
#             if first:
#                 file.write("%%DocumentMedia: ")
#                 first = 0
#             else:
#                 file.write("%%+ ")
#             file.write("%s %d %d 75 white ()\n" % (paperformat, unit.topt(size[0]), unit.topt(size[1])))
# 
#         file.write("%%%%Pages: %d\n" % len(self.pages))
#         file.write("%%PageOrder: Ascend\n")
#         file.write("%%EndComments\n")
# 
#         # document default section
#         #file.write("%%BeginDefaults\n")
#         #if paperformat:
#         #    file.write("%%%%PageMedia: %s\n" % paperformat)
#         #file.write("%%%%PageOrientation: %s\n" % (rotated and "Landscape" or "Portrait"))
#         #file.write("%%EndDefaults\n")
# 
#         # document prolog section
#         file.write("%%BeginProlog\n")
#         mergedprolog = []
#         for apage in self.pages:
#             for pritem in apage.prolog():
#                 for mpritem in mergedprolog:
#                     if mpritem.merge(pritem) is None: break
#                 else:
#                     mergedprolog.append(pritem)
#         for pritem in mergedprolog:
#             pritem.outputPS(file)
#         file.write("%%EndProlog\n")
# 
#         # document setup section
#         #file.write("%%BeginSetup\n")
#         #file.write("%%EndSetup\n")
# 
#         # pages section
#         for nr, apage in enumerate(self.pages):
#             file.write("%%%%Page: %s %d\n" % (apage.pagename is None and str(nr) or apage.pagename , nr+1))
#             apage.outputPS(file)
# 
#         file.write("%%Trailer\n")
#         file.write("%%EOF\n")
