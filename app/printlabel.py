### Import Python Modules
"""
Print label file that handles Brother QL-720NW interaction.
"""

# -*- coding: utf-8 -*-
import datetime
import socket
import sys
import re

### Printer Configuration
printer_ip = '10.93.0.33'
printer_port = 9100


def sendPrintData(item):
    """Sends print data to Brother QL-720NW."""

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (printer_ip, printer_port)
    sock.connect(server_address)
    labeldata = createESCpLabel(item)
    sock.sendall(labeldata)

    sock.close()
    
# Creates Label
def createESCpLabel(item):
    """Creates hex string for Brother QL-720NW that is converted into a
    label.
    
    Args:
        item (str): Item label requested for print.

    Returns:
        string: Encoded string that is readable by Brother QL-720NW printer.
    """

    # The following codes are compatible with a Brother QL-720NW

    NUL                  = chr(0x00)
    EOT                  = chr(0x04)
    HT                   = chr(0x09) # horizontal tab
    LF                   = chr(0x0a)
    FF                   = chr(0x0c) # Form feed (Print)
    DLE                  = chr(0x10)
    ESC                  = chr(0x1b) # Escape
    FS                   = chr(0x1c)
    GS                   = chr(0x1d)
    CRLF                 = chr(0x0d) + chr(0x0a) # Carriage return / Line feed
    BOLDON               = chr(0x1b) + chr(0x45) # Bold On
    BOLDOFF              = chr(0x1b) + chr(0x46) # Bold Off
    FONT_BROUGHAM        = chr(0x1b) + chr(0x6b) + chr(0x00) # Set font to Brougham (Bitmap fixed)
    FONT_LETTERGOTHIC    = chr(0x1b) + chr(0x6b) + chr(0x01) # Set font to Letter Gothic (Bitmap fixed)
    FONT_BRUSSELS        = chr(0x1b) + chr(0x6b) + chr(0x02) # Set font to Brussels (Bitmap Proportional)
    FONT_HELSINKI        = chr(0x1b) + chr(0x6b) + chr(0x03) # Set font to Helsinki (Bitmap Proportional)
    FONT_SANDIEGO        = chr(0x1b) + chr(0x6b) + chr(0x04) # Set font to San Diego (Bitmap Proportional)
    FONT_LETTERGOTHIC_OL = chr(0x1b) + chr(0x6b) + chr(0x09) # Set font to Letter Gothic (Outline fixed)
    FONT_BRUSSELS_OL     = chr(0x1b) + chr(0x6b) + chr(0x0a) # Set font to Brussels (Outline Proportional)
    FONT_HELSINKI_OL     = chr(0x1b) + chr(0x6b) + chr(0x0b) # Set font to Helsinki (Outline Proportional)
    LANDSCAPE            = chr(0x1b) + chr(0x69) + chr(0x4c) + chr(0x01) # Set to Landscape
    ESPCMODE             = chr(0x1b) + chr(0x61) + chr(0x69) + chr(0x00) # Select ESC/P mode
    INIT                 = chr(0x1b) + chr(0x40) # Initalize
    FONTSIZE             = chr(0x1b) + chr(0x58) + chr(0x00) # Set font size  nL nH
    MINLF                = chr(0x1b) + chr(0x33) # Specify minimum line feed n (0-255)
    BACKSLASH            = chr(0x5c)

    # Builds Barcode
    BARCODE = ESC + chr(0x69) + chr(0x74) + chr(0x30) + chr(0x72) + chr(0x30) + chr(0x68) + chr(0x68) + chr(0x00) + chr(0x77) + chr(0x31) + chr(0x7A) + chr(0x32) + chr(0x42)
	
    code = str(item.ItemCode)
    string = ESPCMODE + INIT + LANDSCAPE + FONT_HELSINKI_OL
    string += FONTSIZE + chr(58) + NUL
    string += item.ProductLine + " " + BOLDON + item.ItemCode + BOLDOFF + " "
    string += ESC + chr(0x24) + chr(0x20) + chr(0x03) + item.SalesUnitOfMeasure + CRLF
    string += BARCODE + code + BACKSLASH + CRLF
    string += item.ItemCodeDesc + CRLF
    #string += cleanString(item.ItemCodeDesc) + CRLF
    #string += item.ItemCodeDesc.encode('utf-8', errors='replace') + CRLF
    #string += unicode(item.ItemCodeDesc, errors='replace') + CRLF
    string += item.PrimaryVendorNo + CRLF
    string += FF
    encoded_str = string.encode('utf-8', errors='replace')
    #decoded_str = string.decode('windows-1252')
    #encoded_str = decoded_str.encode("utf8")
    print(encoded_str)
    print(':'.join(x.encode('hex') for x in encoded_str))
    return encoded_str

# TODO Fix vulgar fraction handling.

# UTF-8 Compatible Print
def cleanString(s):
	
	return s

# UTF-8 Compatible Print, version 2
def cleanStringxx(s):
	fractions = {
	    0x2189: 0.0,  # ; ; 0 # No       VULGAR FRACTION ZERO THIRDS
	    0x2152: 0.1,  # ; ; 1/10 # No       VULGAR FRACTION ONE TENTH
	    0x2151: 0.11111111,  # ; ; 1/9 # No       VULGAR FRACTION ONE NINTH
	    0x215B: 0.125,  # ; ; 1/8 # No       VULGAR FRACTION ONE EIGHTH
	    0x2150: 0.14285714,  # ; ; 1/7 # No       VULGAR FRACTION ONE SEVENTH
	    0x2159: 0.16666667,  # ; ; 1/6 # No       VULGAR FRACTION ONE SIXTH
	    0x2155: 0.2,  # ; ; 1/5 # No       VULGAR FRACTION ONE FIFTH
	    0xBC  : 0.25,  # ; ; 1/4 # No       VULGAR FRACTION ONE QUARTER
	    0x00BC: 0.25,  # ; ; 1/4 # No       VULGAR FRACTION ONE QUARTER
	    0x2153: 0.33333333,  # ; ; 1/3 # No       VULGAR FRACTION ONE THIRD
	    0x215C: 0.375,  # ; ; 3/8 # No       VULGAR FRACTION THREE EIGHTHS
	    0x2156: 0.4,  # ; ; 2/5 # No       VULGAR FRACTION TWO FIFTHS
	    0xBD  : 0.5,  # ; ; 1/2 # No       VULGAR FRACTION ONE HALF
	    0x00BD: 0.5,  # ; ; 1/2 # No       VULGAR FRACTION ONE HALF
	    0x2157: 0.6,  # ; ; 3/5 # No       VULGAR FRACTION THREE FIFTHS
	    0x215D: 0.625,  # ; ; 5/8 # No       VULGAR FRACTION FIVE EIGHTHS
	    0x2154: 0.66666667,  # ; ; 2/3 # No       VULGAR FRACTION TWO THIRDS
	    0xBE  : 0.75,  # ; ; 3/4 # No       VULGAR FRACTION THREE QUARTERS
	    0x00BE: 0.75,  # ; ; 3/4 # No       VULGAR FRACTION THREE QUARTERS
	    0x2158: 0.8,  # ; ; 4/5 # No       VULGAR FRACTION FOUR FIFTHS
	    0x215A: 0.83333333,  # ; ; 5/6 # No       VULGAR FRACTION FIVE SIXTHS
	    0x215E: 0.875,  # ; ; 7/8 # No       VULGAR FRACTION SEVEN EIGHTHS
	}
	rx = r'(?u)([+-])?(\d*)(%s)' % '|'.join(map(unichr, fractions))
	pattern = re.compile(rx)
	result = pattern.sub(lambda x: fractions[x.group()], s)
	return result
