# ---------------------------------------------------------------------------#
# import the various server implementations
# ---------------------------------------------------------------------------#
from widgetlords.pi_spi import *
import RPi.GPIO as GPIO


class InOut:

    @staticmethod
    def init():
        """ Initialize
        """
        init()
        GPIO.setmode(GPIO.BCM)

    @staticmethod
    def set_analog_output(pin,value):
        """
        Set analog output 4-20mA
        (4mA at 745 D/A  -  20mA at 3723 D/A)

        :param pin: number of pin
        :param value: value of output in %
        """
        outputs = Mod2AO()
        outputs.write_single(pin, (value*29.78+745))

    @staticmethod
    def read_digital_input(pin):
        """
        Read digital input on external card

        :param pin: number of pin
        :return: value on the pin
        """
        inputs = Mod8DI()
        return inputs.read_single(pin)

    @staticmethod
    def set_relay(pin):
        """
        Set relay in output

        :param pin: the pin
        """
        GPIO.output(pin, GPIO.OUT)

    @staticmethod
    def set_relay_value(pin, value):
        """
        Set value of relay

        :param pin: number of pin
        :param value: value 0 for hight and 1 for hight
        """

        if value == 0:
            GPIO.output(pin, GPIO.LOW)
        else:
            GPIO.output(pin, GPIO.HIGH)
