#!/usr/bin/env python
"""
A simple stand alown pure python script to dump data from an ubertooth into a 
file.  The dump format is compatible with the ubertooth-rx tool.  This allows 
for data to be collected in python and parsed with the core ubertooth libraries.

To dump data from an ubertooth to a file:
python ubertooth_dump.py dump_filename.dump
"""

import sys
import array
import usb.core

try:
    fw = open(sys.argv[1], 'wb')
except:
    print "[!] ERROR: please specify a file to write to"
    raise

try:
    device = usb.core.find(idVendor=0x1D50, idProduct=0x6002)
    device.default_timeout=3000
    device.set_configuration()
    device.ctrl_transfer(0x40, 12, 2402+37, 0)
    device.ctrl_transfer(0x40, 1, 0, 0)
except:
    print "[!] ERROR: no ubertooth detected"
    raise

try:
    print "[*] Writing data to %s" % (sys.argv[1])
    print "[*] Press ctrl+c to stop"
    while True:
        buffer = device.read(0x82, 64)
        buffer = array.array('B', [0,0,0,0]) + buffer
        fw.write(buffer)
except KeyboardInterrupt:
    pass

fw.close()

print "\n[*] Shutting down ubertooth device"
device.ctrl_transfer(0x40, 21)
device.ctrl_transfer(0x40, 13)
