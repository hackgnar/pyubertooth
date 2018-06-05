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

import array
import time
import struct

import usb.core


USB_ID_VENDOR = 0x1D50
USB_ID_PRODUCT = 0x6002


class Ubertooth(object):
    #TODO: add support for multiple ubertooth devices
    def __init__(self, device=True, infile=None):
        if device:
            self.device = self._init_device()
        else:
            self.device = None
        
        if infile:
            self.infile = open(infile, 'rb') 

    @staticmethod
    def _init_device():
        device = usb.core.find(idVendor=USB_ID_VENDOR,
                               idProduct=USB_ID_PRODUCT)
        device.default_timeout = 3000
        device.set_configuration()
        return device

    def set_channel(self, channel=37):
        self.device.ctrl_transfer(0x40, 12, 2402+channel, 0)
    
    def set_rx_mode(self):
        self.device.ctrl_transfer(0x40, 1, 0, 0)

    def rx_file_stream(self, count=None, secs=None):
        i = 0
        start = time.time()
        while True:
            buffer = array.array('B')
            try:
                buffer.fromfile(self.infile, 68)
            except:
                break
            if count != None: 
                if i >= count:
                    break
                i += 1
            if secs is not None:
                if time.time() >= start+secs:
                    break
            yield buffer

    def rx_stream(self, count=None, secs=None):
        self.set_rx_mode()
        i = 0
        start = time.time()
        while True:
            buf = self.device.read(0x82, 64)
            if count is not None:
                if i >= count:
                    print i
                    break
                i += 1
            if secs is not None:
                if time.time() >= start+secs:
                    break
            yield buf
    
    def close(self):
        self.device.ctrl_transfer(0x40, 21)
        self.device.ctrl_transfer(0x40, 13)

    ### Start new stuff 4/27/16
    def cmd_trim_clock(self):
        #trim clock
        #line 65 ubertooth_control.c
        #THIS IS AN UBERTOOTH ASYNC COMMAND
        pass

    def cmd_ping(self):
        # cmd ping 
        #line 75 ubertooth_control.c
        result = self.device.ctrl_transfer(0xc0,0,0, 0,0)
        return result

    def cmd_rx_syms(self):
        ### already implemented above
        #set rx mode
        #line 88 ubertooth_control.c
        self.device.ctrl_transfer(0x40,1,0,0)

    def cmd_specan(self, low_freq=2402, high_freq=2480):
        #specan where low_freq & high_freq is 2402-2480
        #line 101 ubertooth_control.c
        self.device.ctrl_transfer(0x40,27,low_freq,high_freq)

    def cmd_led_specan(self, rssi=225):
        # led specscan where rssi is 1-225
        #line 114 ubertooth_control.c
        self.device.ctrl_transfer(0x40,34,225, 0)

    def cmd_set_usrled(self, state=0):
        #set usrled where state is 0-1
        #line 127 ubertooth_control.c
        self.device.ctrl_transfer(0x40,4,state, 0)

    def cmd_get_usrled(self):
        #get usrled where state is 0-1
        #line 140 ubertooth_control.c
        state = self.device.ctrl_transfer(0xc0,3,0, 0,1)
        state = struct.unpack('b',state)[0]
        return state

    def cmd_set_rxled(self, state=0):
        #set rxled where state is 0-1
        #line 154 ubertooth_control.c
        self.device.ctrl_transfer(0x40,6,state, 0)

    def cmd_get_rxled(self):
        #get rxled where state is 0-1
        #line 167 ubertooth_control.c
        state = self.device.ctrl_transfer(0xc0,5,0, 0,1)
        state = struct.unpack('b',state)[0]
        return state

    def cmd_set_txled(self, state=0):
        #set txled where state is 0-1
        #line 181 ubertooth_control.c
        self.device.ctrl_transfer(0x40,8,state, 0)

    def cmd_get_txled(self):
        #get txled where state is 0-1
        #line 194 ubertooth_control.c
        state = self.device.ctrl_transfer(0xc0,7,0, 0,1)
        state = struct.unpack('b',state)[0]
        return state

    def cmd_get_modulation(self):
        #get modulation where modulation is 0-2 where 0=BTBR 1=BTLE 2=80211_FHSS
        #line 208 ubertooth_control.c
        modulation = self.device.ctrl_transfer(0xc0,22,0, 0,1)
        modulation = struct.unpack('b',modulation)[0]
        return modulation

    def cmd_get_channel(self):
        #get channel where channel is 0-78
        #line 223 ubertooth_control.c
        channel = self.device.ctrl_transfer(0xc0,11,0, 0,2)
        channel = struct.unpack('H',channel)[0]-2402
        return channel

    def cmd_set_channel(self, channel=39):
        ### already implemented
        #set channel where channel is 0-78
        #line 241 ubertooth_control.c
        self.device.ctrl_transfer(0x40,12,2402+channel, 0)

    def cmd_get_partnum(self):
        # get partnum where result=0 for success and part is in hex format
        #line 257 ubertooth_control.c
        part = self.device.ctrl_transfer(0xc0,15,0, 0,5)
        result = struct.unpack('B',part[0:1])[0]
        part = hex(struct.unpack('<I',part[1:])[0])
        return part

    def cmd_get_serial(self):
        #get serial where result=0 for success
        #line 287 ubertooth_control.c
        serial = self.device.ctrl_transfer(0xc0,14,0, 0,17)
        result = struct.unpack('B',serial[0:1])[0]
        serial = struct.unpack('>4i',serial[1:])
        serial = ''.join([format(i,'x') for i in serial])
        return serial
    
    def cmd_set_modulation(self, modulation=0):
        #set modulation 0-2 where 0=BTBR 1=BTLE 2=80211_FHSS
        #line 303 ubertooth_control.c
        self.device.ctrl_transfer(0x40,23,modulation, 0)


    def cmd_set_isp(self):
        #set isp mode (in system programing)
        #line 319 ubertooth_control.c
        self.device.ctrl_transfer(0x40,24,0, 0)

    def cmd_reset(self):
        #reset ubertooth 
        #line 334 ubertooth_control.c
        self.device.ctrl_transfer(0x40,13,0, 0)

    def cmd_stop(self):
        #stop ubertooth
        #line 349 ubertooth_control.c
        self.device.ctrl_transfer(0x40,21,0, 0)

    def cmd_set_paen(self, state=-1):
        #set paen where state ???
        #line 365 ubertooth_control.c
        self.device.ctrl_transfer(0x40,17,state, 0)

    def cmd_set_hgm(self, state=-1):
        #set hgm where state ???
        #line 381 ubertooth_control.c
        self.device.ctrl_transfer(0x40,19,state, 0)

    def cmd_tx_test(self):
        #tx test
        #line 397 ubertooth_control.c
        self.device.ctrl_transfer(0x40,20,0, 0)

    def cmd_flash(self):
        # flash mode
        #line 413 ubertooth_control.c
        self.device.ctrl_transfer(0x40,25,0, 0)

    def cmd_get_palevel(self):
        #get palevel (power amplifier level)
        #line 427 ubertooth_control.c
        level = self.device.ctrl_transfer(0xc0,28,0, 0,1)
        return struct.unpack('b',level)[0]

    def cmd_set_palevel(self, level=7):
        #set palevel (power amplifier level) where level 0-7
        #line 441 ubertooth_control.c
        self.device.ctrl_transfer(0x40,29,level, 0)

    def cmd_get_rangeresult(self):
        #get range test results
        #NOTE THIS FUNCTIONALITY IS BROKEN IN FIRMWARE ATM
        #line 458 ubertooth_control.c
        result = self.device.ctrl_transfer(0xc0,32,0, 0,20)
        return {"valid": result[0],
                "request_pa": result[1],
                "request_num": result[2],
                "reply_pa": result[3],
                "reply_num": result[4]}

    def cmd_range_test(self):
        #range test
        #line 484 ubertooth_control.c
        self.device.ctrl_transfer(0x40,31,0, 0)

    def cmd_repeater(self):
        #repeater mode
        #line 501 ubertooth_control.c
        self.device.ctrl_transfer(0x40,30,0, 0)

    def cmd_get_rev_num(self):
        # get revision number
        #line 518 ubertooth_control.c
        #result = device.ctrl_transfer(0xc0,33,0, 0,258)
        pass

    def cmd_get_compile_info(self):
        # get compile info
        #line 547 ubertooth_control.c
        #result = device.ctrl_transfer(0xc0,55,0, 0,256)
        pass

    def cmd_get_board_id(self):
        # get board id
        #line 570 ubertooth_control.c
        result = self.device.ctrl_transfer(0xc0,35,0, 0,1)
        result = struct.unpack('b',result)[0]
        return result

    def cmd_set_squelch(self, level=0):
        #set squelch where level is ???
        #line 587 ubertooth_control.c
        self.device.ctrl_transfer(0x40,36,level, 0)

    def cmd_get_squelch(self):
        #get squelch where level is default 136
        #line 587 ubertooth_control.c
        level = self.device.ctrl_transfer(0xc0,37,0, 0,1)
        level = struct.unpack('B',level)[0]
        return level

    def cmd_set_bdaddr(self, addr):
        #set bd addr
        #line 617 ubertooth_control.c
        pass

    def cmd_start_hopping(self):
        # start hopping
        #line 647 ubertooth_control.c
        #THIS IS AN UBERTOOTH ASYNC COMMAND
        pass

    def cmd_set_clock(self, clock=0):
        # set clock
        #line 669 ubertooth_control.c
        #clock = ???
        #some magic conversion
        #device.ctrl_transfer(0x40,40,clock... set args change...
        import array
        data = array.array("B", [0, 0, 0, 0, 0, 0])
        self.device.ctrl_transfer(0x40,40,0,0,data)
        pass

    def cmd_get_clock(self):
        # get clock
        #line 689 ubertooth_control.c
        clock = self.device.ctrl_transfer(0xc0,41,0, 0,4)
        clock = struct.unpack('<I',clock)[0]
        return clock

    def cmd_btle_sniffing(self, num=2):
        # btle sniffing mode where num=2... wtf is num always 2???
        #line 706 ubertooth_control.c
        self.device.ctrl_transfer(0x40,42,num, 0)

    def todo(self):
        #set afm map
        ##line 723 ubertooth_control.c
        #clear afm map
        ##line 736 ubertooth_control.c
        #get access address
        ##line 752 ubertooth_control.c
        # set access address
        ##line 768 ubertooth_control.c
        # do something
        ##line 788 ubertooth_control.c
        # do something reply
        ##line 803 ubertooth_control.c
        # get crc verify
        ##line 818 ubertooth_control.c
        # set crc verify
        ##line 832 ubertooth_control.c
        # poll mode
        ##line 845 ubertooth_control.c
        # btle promisc mode
        ##line 858 ubertooth_control.c
        pass

    def cmd_read_register(self, reg):
        value = self.device.ctrl_transfer(0xc0, 53, reg & 0xFF, 0, 2)
        value = struct.unpack('>H',value)
        return value

    def todo2(self):
        # read register
        ##line 875 ubertooth_control.c
        # btle slave mode
        ##line 894 ubertooth_control.c
        # btle set target
        ##line 912 ubertooth_control.c
        pass

    def cmd_set_jam_mode(self, mode=2):
        #set jam mode where mode is 0-2 where 0 is none 1 is once and 2 is continuous ???
        ##line 930 ubertooth_control.c
        self.device.ctrl_transfer(0x40,59,mode, 0)

    def todo3(self):
        # ego mode
        ##line 947 ubertooth_control.c
        # afh mode
        ##line 964 ubertooth_control.c
        # hop mode
        ##line 982 ubertooth_control.c
        # api version
        ##line 994 ubertooth_control.c
        pass

    def cmd_write_register(self, reg, value=0):
        self.device.ctrl_transfer(0x40, 58, reg & 0xFF, value)

    def cmd_write_registers(self, registers):
        """
        registers is a dictionary of register:value pairs
        """
        count = len(registers)
        data = array.array("B", [0]*count*3)
        for i, reg in enumerate(registers):
            data[i*3] = reg & 0xFF
            data[(i*3)+1] = (registers[reg]>>8) & 0xFF
            data[(i*3)+2] = registers[reg] & 0xFF
        print data
        self.device.ctrl_transfer(0x40, 65, count, 0, data)
