"""
*** Python Basic class for Widgetlords Electronics' SPI devices ***

NOTE: All SPI devices from Widgetlord Electronics uses auxiliary CS pin.

Copyright 2016

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS

"""

#try:
import spidev
import RPi.GPIO as GPIO
#except ImportError:
    # print 'Failed to import SPI library, please install it now'


class PiSPI:
    """
    This class provides basic feature of SPI protocol.
    """
    spi = spidev.SpiDev()
    cs_pin = 22
    b_opened = False
    mode = 0
    speed = 100000

    def __init__(self, cs_pin=22, mode=0, speed=100000):
        """
        :param cs_pin:  Auxiliary SPI_CS pin number
        :param mode:    SPI mode
        :param speed:   SPI clock
        """
        # self.bus = bus
        # self.device = device
        self.cs_pin = cs_pin
        self.initialize_gpio()
        self.mode = mode
        self.speed = speed

    def open(self):
        """
        Open SPI bus and initialize.
        :return:
        """
        # self.spi.open(self.bus, self.device)
        self.spi.open(0, 0)
        self.spi.mode = self.mode
        self.spi.lsbfirst = False
        self.spi.max_speed_hz = self.speed
        self.b_opened = True

    def initialize_gpio(self):
        """
        Initialize GPIO of RPi
        :return:
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.output(self.cs_pin, True)
        return True

    def close(self):
        """
        Close SPI connection
        :return:
        """
        self.b_opened = False
        self.spi.close()

    def send_cmd(self, cmd):
        """
        Send SPI cmd and return response
        :param cmd: Must be a list
        :return:
        """
        if type(cmd) != list:
            raise ValueError("Error: Command must be in format of list")

        self.open()
        GPIO.output(self.cs_pin, False)
        resp = self.spi.xfer(cmd)
        GPIO.output(self.cs_pin, True)
        self.close()
        return resp
