#!/usr/bin/python

################################################################
# JetScanner - Command-line utility to scan pages from an HP
# JetDirect device without using the web interface. Currently
# it only supports HP JetDirect 175x (J6035B). Others not tested
# Copyright (C) 2011 Dante Lanznaster, www.yournearestbar.com
################################################################

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>

import urllib, urllib2, sys, argparse, time
from pyPdf import PdfFileWriter, PdfFileReader

def reporthook(a,b,c):
    print "% 3.1f%% of %d bytes\r" % (min(100, float(a * b) / c * 100), c),
    sys.stdout.flush()

def extension(i):
    if args.fmt == 1:
       return 'tif'
    elif args.fmt == 2:
       return 'jpg'
    else:
       return 'pdf'

arguments = argparse.ArgumentParser(prog='jetscanner', description='Scans a page from a JetDirect device')
arguments.add_argument('--dev', '-d', help='HP JetDirect device, either IP address or hostname', required=True)
arguments.add_argument('--type', '-t', help='Image type, 4=Color Picture 3=Color Drawing 2=B/W Picture 1=Text', required=True, type=int, choices=[4, 3, 2, 1])
arguments.add_argument('--size', '-s', help='Document size, 1=Letter, 4=Executive, 5=4x6in 6=5x7in 7=3x5in 8=3x3in', required=True, type=int, choices=[1, 4, 5, 6, 7, 8])
arguments.add_argument('--fmt', '-f', help='File format, 1=TIFF 2=JPEG 3=PDF', required=True, type=int, choices=[1, 2, 3])
args = arguments.parse_args()

posttime = int(time.time() * 1000) # the POST string requires a 13 char epoch time string
filetime = time.strftime('%Y%m%d%H%M')

dev = args.dev
id = 10
type = args.type
size = args.size
fmt = args.fmt

if args.fmt == 2:
   if args.type == 2 or args.type == 1:
      print 'JPEG scanning is not supported with B/W or Text types'
      quit()

url = 'http://' + dev + '/scan/image1.' + extension(args.fmt)
parameters = {'id' : id, 'type' : type, 'size' : size, 'fmt' : fmt, 'time' : posttime}
pass_values = urllib.urlencode(parameters)
sendreq = url + '?' + pass_values
localfile = 'scanned' + filetime + '.' + extension(args.fmt)
print sendreq, '>>>', localfile
urllib.urlretrieve(sendreq, localfile, reporthook)


#formats not supported: JPEG/BW, JPEG/TEXT, 
