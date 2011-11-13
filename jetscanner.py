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

#import pdb

localfile = 'none'

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

def askyesno():
    ok = False
    while True:
          user_input = raw_input("\nAnother page? (y=yes*, n=no)?").strip().lower()
          if not user_input or user_input == 'y':
             ok = True
             return(True)             
          elif user_input == 'n':
               return(False)
          else:
               print "Please enter 'y' or 'n'"

def curfilename():
    filetime = time.strftime('%Y%m%d%H%M%S')
    global localfile
    localfile = 'scanned' + filetime + '.' + extension(args.fmt)
    return(localfile)

arguments = argparse.ArgumentParser(prog='jetscanner', description='Scans a page from a JetDirect device')
arguments.add_argument('--dev', '-d', help='HP JetDirect device, either IP address or hostname', required=True)
arguments.add_argument('--type', '-t', help='Image type, 4=Color Picture 3=Color Drawing 2=B/W Picture 1=Text', required=True, type=int, choices=[4, 3, 2, 1])
arguments.add_argument('--size', '-s', help='Document size, 1=Letter, 4=Executive, 5=4x6in 6=5x7in 7=3x5in 8=3x3in', required=True, type=int, choices=[1, 4, 5, 6, 7, 8])
arguments.add_argument('--fmt', '-f', help='File format, 1=TIFF 2=JPEG 3=PDF', required=True, type=int, choices=[1, 2, 3])
arguments.add_argument('--mp', '-m', help='Create a multi-page PDF file, only valid for PDF scanning', action='store_true')
args = arguments.parse_args()

posttime = int(time.time() * 1000) # the POST string requires a 13 char epoch time string

if args.fmt == 2:
   if args.type == 2 or args.type == 1:
      print 'JPEG scanning is not supported with B/W or Text types'
      quit()

def scanpage():
    url = 'http://' + args.dev + '/scan/image1.' + extension(args.fmt)
    parameters = {'id' : 10, 'type' : args.type, 'size' : args.size, 'fmt' : args.fmt, 'time' : posttime}
    pass_values = urllib.urlencode(parameters)
    sendreq = url + '?' + pass_values
    urllib.urlretrieve(sendreq, curfilename(), reporthook)
    #return ('scanned')

#pdb.set_trace()

print 'We are scanning the first page'
scanpage()

if args.fmt == 3 and args.mp == True:
   #onemore = ''
   out = PdfFileWriter()
   outstream = file('out.pdf', "wb")
   while askyesno() == True:
      print 'answered yes so we are scanning again'
      inp = PdfFileReader(file(localfile, "rb"))
      print 'read the file'
      out.addPage(inp.getPage(0))
      print 'at this point we added the first page to the output'
      scanpage()
   out.write(outstream)
   outstream.close()
   quit()


#   while onemore != False:
#         print 'we entered the while'
#         scanpage()
#         if askyesno() == True:
#            inp = PdfFileReader(file(localfile, "rb"))
#            print 'you said yes, sending the next scan command'
#            out.addPage(inp.getPage(0))
#            print 'added the previous file,' + localfile + ' to the out file'
#            #scanpage()
#            #onemore = True
#         else:
#              print 'answered no'
#              onemore == False
#              break
#         outStream = file("out.pdf", "wb")
#         out.write(outStream)
#         outStream.close()
#         quit()


