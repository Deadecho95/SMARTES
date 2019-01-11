"""
*** Python Driver class for Microchip's MCP23S08 IO Expander ***

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

# Add parent directory to path for `pispi.py`.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from IO.pispi import PiSPI

__version__ = 0.1


class MCP23S08(PiSPI):
    """
        SDIN: | 0 | 1 | 0 | 0 | 0 | A1 | A0 | R/W | A7 | A6 | A5 | A4 | A3 | A2 | A1 | A0 |
    """
    address = 0

    def __init__(self, address=0, cs_pin=17):                        # AI module uses GPIO7 for SPI_CS
        # Though MCP23S08 has maximum clock of 10MHz, I set it as 61KHz
        # See below for more details.
        # https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md
        # PiSPI.__init__(self, cs_pin=cs_pin, speed=61000, bus=bus, device=device)
        PiSPI.__init__(self, cs_pin=cs_pin, speed=61000)
        if address not in [0, 1, 2, 3]:
            raise ValueError("Address error, it must be 0, 1, 2, or 3")
        self.address = address

    def set_direction(self, channel, direction):
        """
        Set direction of given channel
        :param channel:
        :param direction:
        :return:
        """
        if direction in [0, 'in', 'IN', 'input', 'INPUT']:
            d = '1'
        elif direction in [1, 'out', 'OUT', 'output', 'OUTPUT']:
            d = '0'
        else:
            raise ValueError("Invalid direction value")

        # Get current GPIO directions from IODIR(0x00) Register
        old_val = '{0:8b}'.format(self.read_register(0x00))

        old_val[7-channel] = d

        # Write to IODIR(0x00) Register
        self.write_register(0x00, int(old_val, 2))

    def read_register(self, address):
        """
        Read Register value
        :param address:
        :return:
        """
        cmd = (8 << 3) | (self.address << 1) | 1
        resp = self.send_cmd([cmd, address, 0, 0])
        # print 'Response: ', ' '.join(['{0:08b}'.format(r) for r in resp])
        return resp[2]

    def write_register(self, address, value):
        """
        Write new register value
        :param address:
        :param value:
        :return:
        """
        cmd = (8 << 3) | (self.address << 1)
        self.send_cmd([cmd, address, value])

    def get_values(self):
        """
        Read all GPIO values.
        Supposed that all channels are configured as INPUT
        :return:
        """
        # Get current GPIO status from GPIO(0x09) Register
        val = self.read_register(0x09)
        return '{0:08b}'.format(val)


