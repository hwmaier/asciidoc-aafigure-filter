aafigure filter for AsciiDoc
============================
Author: Henrik Maier

Version: 1.0


Introduction
------------

Aafigure (link:http://https://launchpad.net/aafigure[]) is an application for
ASCII line art to image conversion. Using the AsciiDoc aafigure filter, ASCII
line art can be embedded into AsciiDoc documents and processed into either PNG
bitmap or SVG vector graphics.


Usage
-----

- The aafigure filter is invoked by setting the listing block or
  paragraph style (the first positional block attribute) to '"aafigure"'.
- The second positional attribute (named 'target') is optional, it sets
  the name of the generated image file. If this is not supplied a
  file name is automatically generated.
- The default output format is SVG for DocBook and PNG for all other backends.
- Additional well known aafigure options can be specified as named attributes. Refer to table below.

.Supported aafigure options
[cols="20e,35m,10,35",options="header,unbreakable"]
|==============================================================================
| Option       | Example                        | Default | Function
| format       | ["aafigure",format="png"]      | `svg` for DocBook, otherwise `png` | Image file format
| scaling      | ["aafigure",scaling="0.5"]     | `1.0` | aafigure image scaling
    footnote:[`scaling` is different to the DocBook backend's image `scale` attribute!]
| aspect       | ["aafigure",aspect="0.7"]      | `1.0` | set aafigure aspect ratio
| linewidth    | ["aafigure",linewidth="4.0"]   | `2.0` | set linewidth (svg only)
| foreground   | ["aafigure",foreground="#ff1050"] | `#000000` | foreground color
| background   | ["aafigure",background="#eeeeee"] | `#ffffff` | background color
| fill         | ["aafigure",fill="#fff"]          | `#000000` | fill color (png only)
| textual      | ["aafigure",options="textual"]    |  | disable horizontal fill detection
| proportional | ["aafigure",options="proportional"] | `proportional` | use proportional font (default)
| fixed        | ["aafigure",options="fixed"]      |  | used fixed-width font
|==============================================================================


This AsciiDoc block:

[listing]
.....................................................................
["aafigure"]
-------------------------------------------------------------------------------
    +---------------+
    |A box with text|
    +---------------+
-------------------------------------------------------------------------------
.....................................................................

renders:

["aafigure"]
-------------------------------------------------------------------------------
    +---------------+
    |A box with text|
    +---------------+
-------------------------------------------------------------------------------


Installation
------------

In addition to AsciiDoc you will need to have installed:

- The aafigure Python package (https://launchpad.net/aafigure)
- The Python Imaging Library (PIL) package (http://www.pythonware.com/products/pil/)

The filter was developed and tested on Windows using aafigure 0.5, PIL 1.1.7
and AsciiDoc 8.6.3.


Known Issues
------------

The Python Imaging Library (PIL) does a very poor job determining the correct
font file on Windows platforms. It may generate warning and error messages as
shown below if the font file names do not exactly match:

---------------------
FT_Stream_Open: could not open `LiberationSans-Regular.ttf'
FT_Stream_Open: could not open `C:\WINDOWS\fonts\LiberationSans-Regular.ttf'
FT_Stream_Open: could not open `Arial.ttf'
---------------------

or

---------------------
FT_Stream_Open: could not open `LiberationMono-Regular.ttf'
FT_Stream_Open: could not open `C:\WINDOWS\fonts\LiberationMono-Regular.ttf'
FT_Stream_Open: could not open `Courier_New.ttf'
FT_Stream_Open: could not open `C:\WINDOWS\fonts\Courier_New.ttf'
WARNING: font not found, using PIL default font
---------------------

To avoid the warning and error messages make a local copy of the the font
files into same directory as the filter script and rename them accordingly.


Examples
--------

The following examples are taken from the aafigure documentation.

.Different arrow types
[aafigure]
-------------------------------------------------------------------------------
    <-->  >->   --> <--
    >--<  o-->  -->+<--
    o--o          o=>
-------------------------------------------------------------------------------


.Another example
[aafigure]
-------------------------------------------------------------------------------
        ---> | ^|   |   +++
        <--- | || --+-- +++
        <--> | |V   |   +++<-
     __             __    ^
    |  |__  +---+  |__|   |
            |box|   ..
            +---+  Xenophon
-------------------------------------------------------------------------------


.Flow chart
["aafigure",options="textual"]
-------------------------------------------------------------------------------
        /---------\
        |  Start  |
        \----+----/
             |
             V
        +----+----+
        |  Init   |
        +----+----+
             |
             +<-----------+
             |            |
             V            |
        +----+----+       |
        | Process |       |
        +----+----+       |
             |            |
             V            |
        +----+----+  yes  |
        |  more?  +-------+
        +----+----+
             | no
             V
        /----+----\
        |   End   |
        \---------/
-------------------------------------------------------------------------------


.Sequence diagram
["aafigure",scaling="0.8"]
-------------------------------------------------------------------------------
    +---------+  +---------+  +---------+
    |Object 1 |  |Object 2 |  |Object 3 |
    +----+----+  +----+----+  +----+----+
         |            |            |
         |            |            |
         X            |            |
         X----------->X            |
         X            X            |
         X<-----------X            |
         X            |            |
         X            |            |
         X------------------------>X
         |            |            X
         X----------->X            X---+
         X            X            X   |
         |            |            X<--+
         X<------------------------X
         X            |            |
         |            |            |
         |            |            |
-------------------------------------------------------------------------------


["aafigure",scaling="0.8"]
-------------------------------------------------------------------------------
    +---------+         +---------+     +---------+
    |  Shape  |         |  Line   |     |  Point  |
    +---------+         +---------+   2 +---------+
    | draw    +<--------+ start   +----O+ x       |
    | move    +<-+      | end     |     | y       |
    +---------+   \     +---------+     +---------+
                   \
                    \   +---------+
                     +--+ Circle  |
                        +---------+
                        | center  |
                        | radius  |
                        +---------+
-------------------------------------------------------------------------------


["aafigure",scaledwidth="100%"]
-------------------------------------------------------------------------------
                             /-----------\     yes /----------\
                          -->| then this |--->*--->| and this |
                      +  /   \-----------/    |no  \----------/
     /------------\   +--                     |
     | First this |-->+                       |
     \------------/   +--                     |
                      +  \   /---------\      V        /------\
                          -->| or that |----->*------->| Done |
                             \---------/               \------/
-------------------------------------------------------------------------------


.Electrical circuit
["aafigure",fill="#fff"]
-------------------------------------------------------------------------------
          Iin +-----+      Iout
        O->---+ R1  +---o-->-----O
       |      +-----+   |         |
    Vin|       100k   ----- C1    | Vout
       |              ----- 100n  |
       v                |         v
        O---------------o--------O
-------------------------------------------------------------------------------


.Schematic diagram
["aafigure",format="png",fill="#fff",scaling="0.8",options="textual",scaledwidth="100%"]
-------------------------------------------------------------------------------
                         Q1  _  8MHz
                           || ||
                      +----+| |+----+
                      |    ||_||    |
                      |             |
                +-----+-------------+-----+
                |    XIN           XOUT   |
                |                         |
                |                    P3.3 +--------------+
    SDA/I2C O---+ P2.0                    |              |
                |                         |             e|
                |        MSP430F123       |   +----+  b|/  V1
    SCL/I2C O---+ P2.1               P3.4 +---+ R1 +---+   PNP
                |                         |   +----+   |\
                |           IC1           |      1k     c|    +----+
                |                         |              o----+ R3 +---O TXD/RS232
                |    VCC             GND  |              |    +----+
                +-----+---------------+---+              |      1k
                      |               |                  |    +----+
                      |               |                  +----+ R2 +---O RXD/RS232
                      |               |                       +----+
                      |               |                         10k
    GND/I2C O---o-----+----o----------o-----------o--------------------O GND/RS232
                |     |    |   C1     |           |   C2
               =+=    |  ----- 1u     |         ----- 10u
                      |  ----- 5V +---+---+     ----- 16V
                      |    |      |  GND  |       |            D1|/|
                      +----o------+out  in+-------o----------o---+ +---O RTS/RS232
                                  |  3V   |                  |   |\|
                                  +-------+                  |
                                   IC2                       | D2|/|
                                                             +---+ +---O DTR/RS232
                                                                 |\|
-------------------------------------------------------------------------------


.Timing diagram
["aafigure",aspect="0.5"]
-------------------------------------------------------------------------------
      ^    ___     ___           ____
    A |___|   |___|   |_________|    |______
      |      ___        ___           __
    B |_____|   |______|   |________XX  XX__
      |
      +-------------------------------------> t
-------------------------------------------------------------------------------


.Timing diagram with descriptions
["aafigure",scaledwidth="100%"]
-------------------------------------------------------------------------------
                        SDA edge
         start                              stop
           |    |          |                 |
           v    v          v                 v
        ___      __________                   ___
    SDA    |    |          |                 |
           |____|          |_____..._________|
        ______      _____       _..._       _____
    SCL       |    |     |     |     |     |
              |____|     |_____|     |_____|

              ^    ^     ^     ^     ^     ^
              |    |     |     |     |     |
              | 'sh_in'  |  'sh_in'  |  'sh_in
           'sh_out'   'sh_out'    'sh_out'

                        SCL edge
-------------------------------------------------------------------------------


.Statistical diagrams
["aafigure",foreground="#ff1050",aspect="0.7",scaledwidth="100%"]
-------------------------------------------------------------------------------

      |
    1 +------------------------------------------------------------> 31.59%
    2 +-------------------------------> 16.80%
    3 +-----------------------> 12.40%
    4 +-----------------> 9.31%
    5 +--------------> 7.89%
    6 +-----------> 6.10%
    7 +---------> 5.20%
    8 +---------> 4.90%
    9 +--------> 4.53%
      |         +         |         +         |         +         |
      +---------+---------+---------+---------+---------+---------+--->
      |         +         |         +         |         +         |
      0         5        10        15        20        25        30

-------------------------------------------------------------------------------


.Just some bars
[aafigure]
-------------------------------------------------------------------------------
    ^     2
    |    EE
    | 1  EE       4
    |DD  EE   3  HH
    |DD  EE  GG  HH
    |DD  EE  GG  HH
    +------------------>
-------------------------------------------------------------------------------


.Schedules
["aafigure",scaledwidth="100%"]
-------------------------------------------------------------------------------
    "Week"      |  1    |  2    |  3    |  4    |  5    |
    ------------+----------------------------------------
    "Task 1"    |HHHH
    "Task 2"    |    EEEEEEEEEEEE
    "Task 3"    |                GGGGGGGGZZZZZZZZZZ
    "Task 4"    |DD      DD          DD          DD
-------------------------------------------------------------------------------

