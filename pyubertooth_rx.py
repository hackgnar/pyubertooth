#!/usr/bin/env python
"""Copyright 2013 - 2013 Ryan Holeman

This file is part of Project pyubertooth.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; see the file COPYING.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street,
Boston, MA 02110-1301, USA."""

description = """
Description:
A pure python interface to an ubertooth device.  This module can 
be used as a stand alown script or as a python library to interact with an
ubertooth.

Sample usage:
For usage help:
python ubertooth.py --help

To log ubertooth data to a file (usable with ubertooth-rx -i filename):
python ubertooth.py --outfile=dump_filename.dump

To log ubertooth data directly to a file from bluetooth channel 60:
python ubertooth.py --outfile=dump_filename.dump --channel 60

To log 30 seconds worth of ubertooth data directly to a file :
python ubertooth.py --outfile=dump_filename.dump -t 30

To log 300 ubertooth usb data packets directly to a file :
python ubertooth.py --outfile=dump_filename.dump -n 300

To read raw ubertooth usb data from a dump file to std out:
python ubertooth.py --infile=dump_filename.dump
"""

import sys
import argparse
from pylibbtbb.bluetooth_packet import BtbbPacket
from pyubertooth.ubertooth import Ubertooth

def file_to_stdout(infile=None, count=None, secs=None, btbb=False):
    ut = Ubertooth(device=False, infile=infile)
    try:
        for i in ut.rx_file_stream(count=count, secs=secs):
            if btbb:
                pkt = BtbbPacket(data=i[4:])
                if pkt.LAP:
                    print pkt
            else:
                print i
    except KeyboardInterrupt:
        pass

def ubertooth_rx_to_file(outfile=None, channel=37, count=None, secs=None,
        btbb=False):
    ut = Ubertooth()
    ut.set_channel(channel)
    f = open(outfile,'wb')
    try:
        systime = array.array('B',[0,0,0,0])
        for i in ut.rx_stream(count=count, secs=secs):
            f.write(systime + i)
    except KeyboardInterrupt:
        pass
    f.close()
    ut.close()

def ubertooth_rx_to_stdout(channel=37, count=None, secs=None):
    ut = Ubertooth()
    ut.set_channel(channel)
    try:
        for data in ut.rx_stream(count=count, secs=secs):
            ut.set_channel(channel % 79)
            channel += 1
            pkt = BtbbPacket(data=data)
            if pkt.LAP:
                print pkt
    except KeyboardInterrupt:
        pass
    ut.close()

def CreateParser():
    parser = argparse.ArgumentParser(description=description,
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-n", type=int, default=None,
            help="how many usb packets to iterate before quiting")
    parser.add_argument("-t", type=int, default=None,
            help="how many seconds to read from usb device or file")
    parser.add_argument("--channel", type=int, default=37,
            help="What bluetooth channel to listen on (1-79)")
    parser.add_argument("--infile", type=str, default=None,
            help="read packets from an ubertooth dump file")
    parser.add_argument("--outfile", type=str, default="ubertooth-dump.dump",
            help="file to store ubertooth usb packets")
    parser.add_argument("--btbb", action='store_true', default=False,
            help = "parse ubertooth data with pylibbtbb")
    return parser.parse_args()

def main(infile=None, outfile=None, channel=37, count=None, secs=None, btbb=False):
    if infile:
        file_to_stdout(infile=infile, count=count, secs=secs, btbb=btbb)
    elif btbb:
       ubertooth_rx_to_stdout(channel=channel, count=count, secs=secs) 
    else:
        ubertooth_rx_to_file(outfile=outfile, channel=channel, count=count,
                secs=secs, btbb=btbb)

if __name__ == "__main__":
    args = CreateParser()
    main(infile=args.infile, outfile=args.outfile, channel=args.channel,
            count=args.n, secs=args.t, btbb=args.btbb)
