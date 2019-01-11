# ---------------------------------------------------------------------------#
# import the various server implementations
# ---------------------------------------------------------------------------#

from IO.chip.mcp4922 import MCP4922
from IO.chip.mcp23s08 import MCP23S08
import RPi.GPIO as GPIO
class InOut:


    @staticmethod
    def init():
        """ Initialize
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

    @staticmethod
    def close():
        """

        :return:
        """
        GPIO.cleanup()
    @staticmethod
    def set_analog_output(chan,value):
        """
        Set analog output 4-20mA
        (4mA at 745 D/A  -  20mA at 3723 D/A)

        :param pin: number of pin
        :param value: value of output in %
        """
        chip = MCP4922()

        # Set gain
        chip.set_gain(2)

        # Output analog voltage to channel B
        chip.output_percent(channel=chan,percent=value)

    @staticmethod
    def read_digital_input(pin):
        """
        Read digital input on external card

        :param pin: number of pin
        :return: value on the pin
        """
        chip = MCP23S08()
        chip.set_direction()

        return chip.get_values()

    @staticmethod
    def set_relay(pin):
        """
        Set relay in output

        :param pin: the pin
        """
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.OUT)

    @staticmethod
    def set_relay_value(pin, value):
        """
        Set value of relay

        :param pin: number of pin
        :param value: value 0 for hight and 1 for hight
        """

        if value == 1:
            GPIO.output(pin, GPIO.LOW)
        else:
            GPIO.output(pin, GPIO.HIGH)
