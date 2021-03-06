"""
*** Python Driver class for Microchip's MCP4922 DA Converter ***

Copyright 2016

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS
"""

import os
import sys
from IO.pispi import PiSPI

# Add parent directory to path for `pispi.py`.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
__version__ = 0.1


class MCP4922(PiSPI):

    gain = 1
    v_ref = 3.3

    def __init__(self, cs_pin=15, gain=1, v_ref=3.3):               # AO module uses GPIO4 for SPI_CS
        # Though MCP4922 has maximum clock of 20MHz, I set it as 61KHz
        # See below for more details.
        # https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md
        # PiSPI.__init__(self, cs_pin=cs_pin, speed=61000, bus=bus, device=device)

        PiSPI.__init__(self, cs_pin=cs_pin, speed=61000)
        self.v_ref = v_ref
        if gain not in [1, 2]:
            raise ValueError('Error, Gain must be 1 or 2')
        self.gain = gain

    def set_gain(self, gain):
        if gain not in [1, 2]:
            raise ValueError('Error, Gain must be 1 or 2')
        self.gain = gain

    def output(self, prefix, val):
        """
        DA output to channel A
        :param prefix:      Command prefix, 0x3000 or 0xb000 for channel A & B
        :param val:
        :return:
        """
        if not (0 <= val <= 4096):
            raise ValueError('Input value must be range of 0~4095.')

        cmd = prefix | int(val) #convert float in int
        buf1 = (cmd >> 8) & 0xff
        buf2 = cmd & 0xff
        self.send_cmd([buf1, buf2])

    def output_percent(self, channel='a', percent=0.0):
        """
        Analog output
        :param channel: Channel label, `A` or `B`
        :param percent:
        :return:
        """
        val = percent*29.78+745

        if val < 743 or percent > 3725:
            raise ValueError('Invalid percent')

        if channel.lower() not in ['a', 'b']:
            raise ValueError('Invalid channel label, must be `a` or `b`')


       # print 'Analog output, channel: {}, voltage: {}V'.format(channel, volt)
        if channel.lower() == 'a':
            if self.gain == 1:
                self.output(0x3000, val)
            else:
                self.output(0x1000, val)
        else:   # channel b
            if self.gain == 1:
                self.output(0xb000, val)
            else:
                self.output(0x9000, val)

