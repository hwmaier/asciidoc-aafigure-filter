#! /usr/bin/env python
"""AsciiDoc filter script which runs the aafigure program to
convert ASCII line drawings into either a SVG or PNG image file.

Requires the aafigure Python package and Python Imaging Library (PIL) packages
to be installed.

Copyright (C) 2011 Henrik Maier. Free use of this software is
granted under the terms of the GNU General Public License (GPL).
"""

usage = "%prog [options] inputfile"
__version__ = '1.2'

# Suppress warning: "the md5 module is deprecated; use hashlib instead"
import warnings
warnings.simplefilter('ignore',DeprecationWarning)

import os, sys, md5
from optparse import *

# Import aafigure which must be installed as Python package.
# Tested with aafigure 0.5
import aafigure, aafigure.svg, aafigure.pil


#
# Global data
#
verbose = False

#
# Helper functions and classes
#
class AppError(Exception):
    """Application specific exception."""
    pass


def print_verbose(line):
    if verbose:
        sys.stderr.write(line + os.linesep)


#
# Customised aafigure classes
#
class WidthHeightSVGOutputVisitor(aafigure.svg.SVGOutputVisitor):
    '''Modfied version of SVG output visitor class which inserts width/height'''
    def visit_image(self, aa_image):
        return aafigure.svg.SVGOutputVisitor.visit_image(self, aa_image, xml_header=False)


#
# Application init and logic
#
class Application():
    """Application class"""

    def __init__(self):
        """Process commandline arguments"""
        global verbose
        parser = OptionParser(usage, version="%%prog %s" % __version__)
        parser.add_option("-v", "--verbose", action="store_true",
                          help="verbose output to stderr")
        parser.add_option("-o", "--outfile", help="file name of the output file")
        parser.add_option("-m", "--modified", action="store_true",
                          help="skip image creation if input has not changed"
                          " (Detected by time stamp or MD5 checksum (stdin))")
        parser.add_option("-F", "--format", default="png", choices=['svg','png',],
                          help="format type, FORMAT=<png|svg>")
        parser.add_option("-s", "--scale", type=float, default=1.0,
                          help="image scaling")
        parser.add_option("-a", "--aspect", type=float, default=1.0,
                          help="set aspect ratio")
        parser.add_option("-l", "--linewidth", type=float, default=1.0,
                          help="set linewidth (svg only)")
        parser.add_option("-c", "--foreground", default="#000000",
                          help="foreground color")
        parser.add_option("-b", "--background", default="#ffffff",
                          help="background color")
        parser.add_option("-f", "--fill", default="#000000", help="fill color")
        parser.add_option("-t", "--textual", action="store_true",
                          help="disable horizontal fill detection")
        parser.add_option("-p", "--proportional", action="store_true", default=True,
                          help="use proportional font")
        parser.add_option("-x", "--fixed", action="store_false", dest="proportional",
                          help="use fixed font")
        self.options, args = parser.parse_args()
        verbose = self.options.verbose
        print_verbose("Runing filter script %s" % os.path.realpath(sys.argv[0]))
        if len(args) != 1:
            parser.error("Invalid number of arguments")
        self.infile = args[0]
        if self.options.outfile is None:
            if self.infile == '-':
                parser.error("OUTFILE option must be specified")
            self.options.outfile = "%s.%s" % (os.path.splitext(self.infile)[0], self.options.format)
            print_verbose("Output file is %s" % self.options.outfile)
        print_verbose("Output format is %s" % str.upper(self.options.format))


    def run(self):
        """Core logic of the application"""
        outfile = os.path.abspath(self.options.outfile)
        outdir = os.path.dirname(outfile)
        if not os.path.isdir(outdir):
            raise AppError, 'directory does not exist: %s' % outdir
        skip = False
        if self.infile == '-':
            source = sys.stdin.read()
            checksum = md5.new(source).digest()
            f = os.path.splitext(outfile)[0] + '.md5'
            if self.options.modified:
                if os.path.isfile(f) and os.path.isfile(outfile) and \
                        checksum == open(f, 'rb').read():
                    skip = True
                open(f, 'wb').write(checksum)
        else:
            if not os.path.isfile(self.infile):
                raise AppError, 'input file does not exist: %s' % self.infile
            if self.options.modified and os.path.isfile(outfile) and \
                    os.path.getmtime(self.infile) <= os.path.getmtime(outfile):
                skip = True
            source = open(self.infile).read()
        if skip:
            print_verbose('Skipped: no change: %s' % outfile)
            return
        if self.options.format == 'svg':
            font = None # Embed no font info for SVGs, SVGs use font-family attribute
            visitor = WidthHeightSVGOutputVisitor
        else:
            # Be specific about fonts with PNGs as font files are otherwise platform specific
            if self.options.proportional:
                font = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),
                                    "LiberationSans-Regular.ttf")
            else:
                font = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),
                                    "LiberationMono-Regular.ttf")
            visitor = aafigure.pil.PILOutputVisitor
        aafigure.process(unicode(source, 'utf-8'), visitor,
                         options={'file_like': open(outfile, "wb"),
                                  'proportional': self.options.proportional,
                                  'textual': self.options.textual,
                                  'line_width': self.options.linewidth,
                                  'scale': self.options.scale,
                                  'aspect': self.options.aspect,
                                  'fill': self.options.fill,
                                  'foreground': self.options.foreground,
                                  'background': self.options.background,
                                  'format':self.options.format,
                                  'font': font
                                  })
        # To suppress asciidoc 'no output from filter' warnings.
        if self.infile == '-':
            sys.stdout.write(' ')


#
# Main program
#
if __name__ == "__main__":
    """Main program, called when run as a script."""
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        sys.exit("Ouch!")
    except Exception, e:
        sys.exit("%s: %s\n" % (os.path.basename(sys.argv[0]), e))

