# Copyright (c) 2008, 2009, 2010, 2010, WuBook Srl 
#  http://en.wubook.net/ and http://wubook.net/
# Author: Federico Tomassini (aka yellow - yellow at wubook . net)
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of California, Berkeley nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS

__version__ = '0.2' # increase this when making a new stable release

import math
import Image
import ImageDraw

pi_4= math.pi/4
pi2= math.pi * 2

def miller_map(lat, long):
  y= long/180.0
  rlat= math.radians(lat)
  tang= math.tan( pi_4 + (0.8 * (rlat/2)))
  x= 1.25 * math.log(tang)
  x/= 2.3034125433763912
  return (y, x)

def _ellipse(idraw, x, y, nlen, col= 'red', bcol= 'black'):

  x= round(x)
  y= round(y)
  idraw.ellipse( (x-nlen-1, y - nlen-1, x + nlen+1, y + nlen+1), fill= bcol)
  idraw.ellipse( (x-nlen, y - nlen, x + nlen, y + nlen), fill= col)

def _range(n, f= 1, base= 10, steps= 5, minpoint= 2):

  inc= math.log(n, base)
  inc= min(inc, steps)

  nlen= int(minpoint + inc)

  nlen= int(nlen/f)
  return nlen

def geo_marker(coords, sfile, dfile, factor= 1, col= 'red', bcol= 'black', base= 10, steps= 5, minpoint= 2):
  """ geo_marker(coords, sfile, dfile [,factor= 1, col= 'red', bcol= 'black', base= 10, steps= 5]) -> None 

  `coords` is a list of tuples:

     [(lat, long, count, <`col`, `bcol`>),... ]

  where `lat` is latitude, `long` is longitude and `count` is
  the number of visitors coming from this location.
  `col` and `bcol` are optional tuple items (so elements of `coords` list
  can be tuples of different sizes); their meaning is similar to `col` and
  `bcol` function arguments (see below). If these items are missing from the
  tuple, the 'global' `col` and `bcol` values (the ones from the function
  arguments) will be used

  `sfile` is the geographic source map file.
  `dfile` is the destination file.

  `factor` is a scaling parameter. Tune with it your points dimensions.

  You can set your favorite colors with `col` and `bcol`.
  `col` is the color of the actual point.
  `bcol` is the border color of the actual point.
  The default combination col='red', bcol= 'black' draws red circles surrounded
  by black circumferences.
  
  `base` and `steps` control the points growing. For example, if base is 10
  and steps is 5, point changes their dimensions when `count` becomes 
  1,10,100,1000,10000.
  
  `minpoint` is the dimension of one point when count is less then `base`^2 - 1"""

  img= Image.open(sfile)

  xoff= img.size[0]/2
  yoff= img.size[1]/2

  idraw= ImageDraw.Draw(img)
  scoords= []

  for coord in coords:
      x = coord[0]
      y = coord[1]
      n = coord[2]
      try:
          ccol = coord[3]
      except IndexError:
          ccol = col
      try:
          cbcol = coord[4]
      except IndexError:
          cbcol = bcol
      sx, sy = miller_map(x, y)
      sx = xoff * (sx + 1)
      sy = yoff * (1 - sy)

      rng= _range(n, factor, base, steps, minpoint)
      _ellipse(idraw, sx, sy, rng, ccol, cbcol)

  img.save(dfile)
  del img
  del idraw
