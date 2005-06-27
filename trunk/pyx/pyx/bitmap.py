#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2004 Andr� Wobst <wobsta@users.sourceforge.net>
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


import cStringIO, struct, warnings
try:
    import zlib
    haszlib = 1
except:
    haszlib = 0

import bbox, canvas, pswriter, trafo, unit

def ascii85lines(datalen):
    if datalen < 4:
        return 1
    return (datalen + 56)/60

def ascii85stream(file, data):
    """Encodes the string data in ASCII85 and writes it to
    the stream file. The number of lines written to the stream
    is known just from the length of the data by means of the
    ascii85lines function. Note that the tailing newline character
    of the last line is not added by this function, but it is taken
    into account in the ascii85lines function."""
    i = 3 # go on smoothly in case of data length equals zero
    l = 0
    l = [None, None, None, None]
    for i in range(len(data)):
        c = data[i]
        l[i%4] = ord(c)
        if i%4 == 3:
            if i%60 == 3 and i != 3:
                file.write("\n")
            if l:
                # instead of
                # l[3], c5 = divmod(256*256*256*l[0]+256*256*l[1]+256*l[2]+l[3], 85)
                # l[2], c4 = divmod(l[3], 85)
                # we have to avoid number > 2**31 by
                l[3], c5 = divmod(256*256*l[0]+256*256*l[1]+256*l[2]+l[3], 85)
                l[2], c4 = divmod(256*256*3*l[0]+l[3], 85)
                l[1], c3 = divmod(l[2], 85)
                c1  , c2 = divmod(l[1], 85)
                file.write(struct.pack('BBBBB', c1+33, c2+33, c3+33, c4+33, c5+33))
            else:
                file.write("z")
    if i%4 != 3:
        for j in range((i%4) + 1, 4):
            l[j] = 0
        l[3], c5 = divmod(256*256*l[0]+256*256*l[1]+256*l[2]+l[3], 85)
        l[2], c4 = divmod(256*256*3*l[0]+l[3], 85)
        l[1], c3 = divmod(l[2], 85)
        c1  , c2 = divmod(l[1], 85)
        file.write(struct.pack('BBBB', c1+33, c2+33, c3+33, c4+33)[:(i%4)+2])


class image:

    def __init__(self, width, height, mode, data, compressed=None):
        if width <= 0 or height <= 0:
            raise ValueError("valid image size")
        if mode not in ["L", "RGB", "CMYK"]:
            raise ValueError("invalid mode")
        if compressed is None and len(mode)*width*height != len(data):
            raise ValueError("wrong size of uncompressed data")
        self.size = width, height
        self.mode = mode
        self.data = data
        self.compressed = compressed

    def tostring(self, *args):
        if len(args):
            raise RuntimeError("encoding not supported in this implementation")
        return self.data

    def convert(self, model):
        raise RuntimeError("color model conversion not supported in this implementation")


class jpegimage(image):

   def __init__(self, file):
       try:
           data = file.read()
       except:
           data = open(file, "rb").read()
       pos = 0
       nestinglevel = 0
       try:
           while 1:
               if data[pos] == "\377" and data[pos+1] not in ["\0", "\377"]:
                   # print "marker: 0x%02x \\%03o" % (ord(data[pos+1]), ord(data[pos+1]))
                   if data[pos+1] == "\330":
                       if not nestinglevel:
                           begin = pos
                       nestinglevel += 1
                   elif not nestinglevel:
                       raise ValueError("begin marker expected")
                   elif data[pos+1] == "\331":
                       nestinglevel -= 1
                       if not nestinglevel:
                           end = pos + 2
                           break
                   elif data[pos+1] in ["\300", "\301"]:
                       l, bits, height, width, components = struct.unpack(">HBHHB", data[pos+2:pos+10])
                       if bits != 8:
                           raise ValueError("implementation limited to 8 bit per component only")
                       try:
                           mode = {1: "L", 3: "RGB", 4: "CMYK"}[components]
                       except KeyError:
                           raise ValueError("invalid number of components")
                       pos += l+1
                   elif data[pos+1] == "\340":
                       l, id, major, minor, dpikind, xdpi, ydpi = struct.unpack(">H5sBBBHH", data[pos+2:pos+16])
                       if dpikind == 1:
                           self.info = {"dpi": (xdpi, ydpi)}
                       elif dpikind == 2:
                           self.info = {"dpi": (xdpi*2.54, ydpi*2.45)}
                       # else do not provide dpi information
                       pos += l+1
               pos += 1
       except IndexError:
           raise ValueError("end marker expected")
       image.__init__(self, width, height, mode, data[begin:end], compressed="DCT")


class bitmap(canvas.canvasitem):

    def __init__(self, xpos, ypos, image,
                       width=None, height=None, ratio=None,
                       storedata=0, maxstrlen=4093,
                       compressmode="Flate",
                       flatecompresslevel=6,
                       dctquality=75, dctoptimize=0, dctprogression=0):
        self.xpos = xpos
        self.ypos = ypos
        self.imagewidth, self.imageheight = image.size
        self.storedata = storedata
        self.maxstrlen = maxstrlen
        self.imagedataid = "imagedata%d" % id(self)
        self._PSresources = []

        if width is not None or height is not None:
            self.width = width
            self.height = height
            if self.width is None:
                if ratio is None:
                    self.width = self.height * self.imagewidth / float(self.imageheight)
                else:
                    self.width = ratio * self.height
            elif self.height is None:
                if ratio is None:
                    self.height = self.width * self.imageheight / float(self.imagewidth)
                else:
                    self.height = (1.0/ratio) * self.width
            elif ratio is not None:
                raise ValueError("can't specify a ratio when setting width and height")
        else:
            if ratio is not None:
                raise ValueError("must specify width or height to set a ratio")
            widthdpi, heightdpi = image.info["dpi"] # XXX fails when no dpi information available
            self.width = unit.inch(self.imagewidth / float(widthdpi))
            self.height = unit.inch(self.imageheight / float(heightdpi))

        self.xpos_pt = unit.topt(self.xpos)
        self.ypos_pt = unit.topt(self.ypos)
        self.width_pt = unit.topt(self.width)
        self.height_pt = unit.topt(self.height)

        # create decode and colorspace
        self.palettedata = None
        if image.mode == "P":
            palettemode, self.palettedata = image.palette.getdata()
            self.decode = "[0 255]"
            # palettedata and closing ']' is inserted in outputPS
            if palettemode == "L":
                self.colorspace = "[ /Indexed /DeviceGray %i" % (len(self.palettedata)/1-1)
            elif palettemode == "RGB":
                self.colorspace = "[ /Indexed /DeviceRGB %i" % (len(self.palettedata)/3-1)
            elif palettemode == "CMYK":
                self.colorspace = "[ /Indexed /DeviceCMYK %i" % (len(self.palettedata)/4-1)
            else:
                image = image.convert("RGB")
                self.decode = "[0 1 0 1 0 1]"
                self.colorspace = "/DeviceRGB"
                self.palettedata = None
                warnings.warn("image with unknown palette mode converted to rgb image")
        elif len(image.mode) == 1:
            if image.mode != "L":
                image = image.convert("L")
                warnings.warn("specific single channel image mode not natively supported, converted to regular grayscale")
            self.decode = "[0 1]"
            self.colorspace = "/DeviceGray"
        elif image.mode == "CMYK":
            self.decode = "[0 1 0 1 0 1 0 1]"
            self.colorspace = "/DeviceCMYK"
        else:
            if image.mode != "RGB":
                image = image.convert("RGB")
                warnings.warn("image with unknown mode converted to rgb")
            self.decode = "[0 1 0 1 0 1]"
            self.colorspace = "/DeviceRGB"

        # create imagematrix
        self.imagematrix = str(trafo.mirror(0)
                               .translated_pt(-self.xpos_pt, self.ypos_pt+self.height_pt)
                               .scaled_pt(self.imagewidth/self.width_pt, self.imageheight/self.height_pt))

        # savely check whether imagedata is compressed or not
        try:
            imagecompressed = image.compressed
        except:
            imagecompressed = None
        if compressmode != None and imagecompressed != None:
            raise ValueError("compression of a compressed image not supported")
        if not haszlib and compressmode == "Flate":
            warnings.warn("zlib module not available, disable compression")
            compressmode = None

        # create data
        if compressmode == "Flate":
            self.data = zlib.compress(image.tostring(), flatecompresslevel)
        elif compressmode == "DCT":
            self.data = image.tostring("jpeg", image.mode,
                                       dctquality, dctoptimize, dctprogression)
        else:
            self.data = image.tostring()
        self.singlestring = self.storedata and len(self.data) < self.maxstrlen

        # create datasource
        if self.storedata:
            if self.singlestring:
                self.datasource = "/%s load" % self.imagedataid
            else:
                self.datasource = "/imagedataaccess load" # some printers do not allow for inline code here
                self._PSresources.append(pswriter.PSdefinition("imagedataaccess",
                                                               "{ /imagedataindex load " # get list index
                                                               "dup 1 add /imagedataindex exch store " # store increased index
                                                               "/imagedataid load exch get }")) # select string from array
        else:
            self.datasource = "currentfile /ASCII85Decode filter"
        if compressmode == "Flate" or imagecompressed == "Flate":
            self.datasource += " /FlateDecode filter"
        elif compressmode == "DCT" or imagecompressed == "DCT":
            self.datasource += " /DCTDecode filter"
        else:
            if compressmode != None:
                raise ValueError("invalid compressmode '%s'" % compressmode)
            if imagecompressed != None:
                raise ValueError("invalid compressed image '%s'" % imagecompressed)

        # cache resources
        if self.storedata:
            # TODO resource data could be written directly on the output stream
            #      after proper code reorganization
            buffer = cStringIO.StringIO()
            if self.singlestring:
                buffer.write("%%%%BeginData: %i ASCII Lines\n"
                             "<~" % ascii85lines(len(self.data)))
                ascii85stream(buffer, self.data)
                buffer.write("~>\n%%EndData\n")
            else:
                datalen = len(self.data)
                tailpos = datalen - datalen % self.maxstrlen
                buffer.write("%%%%BeginData: %i ASCII Lines\n" %
                             ((tailpos/self.maxstrlen) * ascii85lines(self.maxstrlen) + ascii85lines(datalen-tailpos)))
                buffer.write("[ ")
                for i in xrange(0, tailpos, self.maxstrlen):
                    buffer.write("<~")
                    ascii85stream(buffer, self.data[i: i+self.maxstrlen])
                    buffer.write("~>\n")
                if datalen != tailpos:
                    buffer.write("<~")
                    ascii85stream(buffer, self.data[tailpos:])
                    buffer.write("~>")
                buffer.write("]\n%%EndData\n")
            self._PSresources.append(pswriter.PSdefinition(self.imagedataid, buffer.getvalue()))

    def bbox(self):
        return bbox.bbox_pt(self.xpos_pt, self.ypos_pt,
                            self.xpos_pt+self.width_pt, self.ypos_pt+self.height_pt)

    def registerPS(self, registry):
        for PSresource in self._PSresources:
            registry.add(PSresource)

    def outputPS(self, file):
        file.write("gsave\n"
                   "%s" % self.colorspace)
        if self.palettedata is not None:
            # insert palette data
            file.write("<~")
            ascii85stream(file, self.palettedata)
            file.write("~> ]")
        file.write(" setcolorspace\n")

        if self.storedata and not self.singlestring:
            file.write("/imagedataindex 0 store\n" # not use the stack since interpreters differ in their stack usage
                       "/imagedataid %s store\n" % self.imagedataid)

        file.write("<<\n"
                   "/ImageType 1\n"
                   "/Width %i\n" # imagewidth
                   "/Height %i\n" # imageheight
                   "/BitsPerComponent 8\n"
                   "/ImageMatrix %s\n" # imagematrix
                   "/Decode %s\n" # decode
                   "/DataSource %s\n" # datasource
                   ">>\n" % (self.imagewidth, self.imageheight,
                             self.imagematrix, self.decode, self.datasource))
        if self.storedata:
            file.write("image\n")
        else:
            # the datasource is currentstream (plus some filters)
            file.write("%%%%BeginData: %i ASCII Lines\n"
                       "image\n" % (ascii85lines(len(self.data)) + 1))
            ascii85stream(file, self.data)
            file.write("~>\n%%EndData\n")

        file.write("grestore\n")