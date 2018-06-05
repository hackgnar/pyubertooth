# PyUbertooth
* Python libraries for Ubertooth

## Project Description:
* The goal of PyUbertooth is to provide libraries and tools to interact with an ubertooth device in python.
* All modules and libraries provided by PyUbertooth provide pure python implementations.
* Cpython implementations will be provided in the future, but will always have pure python alternatives.

## Core PyUbertooth Libraries:
* pyubertooth/ubertooth.py: Provides direct access to an ubertooth device.
* pyubertooth/bluetooth_packet.py: Provides methods and data structures for converting ubertooth data into bluetooth baseband data.

## Core PyUbertooth Tools:
* pyubertooth_rx: This file provides some CLI functionality to control the ubertooth.
* ubertooth_dump: A simple script to dump data from an ubertooth device to a file.  This dump data is compatible with the ubertooth C libraries and tools (i.e. used with the -i flag with the ubertooth-rx tool).

## Upcoming Milestones:
* Finish up porting over all USB get/set/mode command functions (WIP)
* The library is still lacking verbose doc strings.  These will be added soon and all of my shitty useless comments will get cleaned up
* Rewrite my pure python libbtbb lib (WIP)
* Create Ctypes libbtbb bindings (WIP)
* Rewrite my ubertooth scapy rx layer
* Create an ubertooth scapy tx layer

-------------------------------

# Core CLI Script: pyubertooth_rx
* A pure python interface to an ubertooth device.
* TODO: Switch to \*args, \*\*kwargs for my argparse methods
* TODO: Many of the simple ubertooth usb contols will be added soon (such as led control, etc)
* TODO: Full python library documentation.

### Sample command line usage:
##### For usage help:
    pyubertooth_rx --help

##### To log ubertooth data to a file (usable with ubertooth-rx -i filename):
    pyubertooth_rx --outfile=dump_filename.dump

##### To log ubertooth data directly to a file from bluetooth channel 60:
    pyubertooth_rx --outfile=dump_filename.dump --channel 60

##### To log 30 seconds worth of ubertooth data directly to a file :
    pyubertooth_rx --outfile=dump_filename.dump -t 30

##### To log 300 ubertooth usb data packets directly to a file :
    pyubertooth_rx --outfile=dump_filename.dump -n 300

##### To read raw ubertooth usb data from a dump file to std out:
    pyubertooth_rx --infile=dump_filename.dump

##### To display bluetooth packet information from a dump file (LAP, UAP, channel, etc):
    pyubertooth_rx --infile=dump_filename.dump --btbb

##### To display bluetooth packet information from a live stream (LAP, UAP, channel, etc):
    pyubertooth_rx --btbb

### Sample python library usage:
##### To open a connection to an ubertooth device:
    from pyubertooth.ubertooth import Ubertooth
    ut = Ubertooth()

##### To access 5 data blocks from an ubertooth device as a python iterator:
    from pyubertooth.ubertooth import Ubertooth
    ut = Ubertooth()
    for data in ut.rx_stream(count=5):
        print data
    ut.close()

##### To access data blocks from an ubertooth device as a python iterator for 30 seconds:
    from pyubertooth.ubertooth import Ubertooth
    ut = Ubertooth()
    for data in ut.rx_stream(secs=30):
        print data
    ut.close()

##### To access data from an ubertooth device until ctrl-C is pressed:
    from pyubertooth.ubertooth import Ubertooth
    ut = Ubertooth()
    try:
        for data in ut.rx_stream():
            print data
    except KeyboardInterrupt:
        pass
    ut.close()

##### An example of directly streaming ubertooth data to a file for 60 seconds:
    from pyubertooth.ubertooth import Ubertooth
    ut = Ubertooth()
    f = open("dump_filename.dump", 'wb')
    for data in ut.rx_stream(secs=60):
        f.write(data)
    f.close()
    ut.close()

##### Changing the channel on an ubertooth device:
    from pyubertooth.ubertooth import Ubertooth 
    ut = Ubertooth()
    ut.set_channel(66)

--------------------------

# Core Library: pylibbtbb/bluetooth_packet.py
* This is a pure python implementation of bluetooth_packet from libbtbb.  It serves as library for python applications.  It is currently in its early stages and based off of the c library libbtbb and some of my ugly POC code 
* LAP & channel detection is working (still needs some cleanup).
* UAP and packet type detection still needs ported from my alpha POC code.
* TODO: utilized the pure python module BitVector.
* TODO: be as cool as the C libbtbb

### Sample python library usage:
##### To display bluetooth packet data for an ubertooth device stream:    
    from pyubertooth.ubertooth import Ubertooth() 
    from pyubertooth.bluetooth_packet import BtbbPacket
    ut = Ubertooth()
    for data in ut.rx_stream():
        print BtbbPacket(data=data)
    ut.close()

----------------------------

# Core Tools: tools/ubertooth_dump.py
* A simple stand alown pure python script to dump data from an ubertooth into a file.  The dump format is compatible with the ubertooth-rx tool.  This allows for data to be collected in python and parsed with the core ubertooth libraries.

## To dump data from an ubertooth to a file:
    python ubertooth_dump.py dump_filename.dump
