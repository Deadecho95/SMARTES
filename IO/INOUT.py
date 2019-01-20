# ---------------------------------------------------------------------------#
# import the various server implementations
# ---------------------------------------------------------------------------#

from IO.chip.mcp4922 import MCP4922
from IO.chip.mcp23s08 import MCP23S08
import RPi.GPIO as GPIO


class InOut:
    """
    manage the IO
    """

    @staticmethod
    def init():
        """ Initialize the IP
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        chip = MCP4922()
        chip.output_percent(channel='a', percent=0)
        chip.output_percent(channel='b', percent=0)

    @staticmethod
    def set_analog_output(chan, value):
        """
        Set analog output 4-20mA
        (4mA at 745 D/A  -  20mA at 3723 D/A)

        :param chan: number of pin
        :param value: value of output in %
        """
        chip = MCP4922()

        # Set gain
        chip.set_gain(1)

        # Output analog voltage to channel B

        if value >= 100:
            value = 100
            chip.output_percent(channel=chan, percent=value)

        elif value <= 0:
            value = 0
            chip.output_percent(channel=chan, percent=value)

        else:
            chip.output_percent(channel=chan, percent=value)

    @staticmethod
    def read_digital_input(pin):
        """
        Read digital input on external card

        :param pin: number of pin
        :return: value on the pin
        """
        chip = MCP23S08()
        chip.set_direction()

        str_result = chip.get_values()

        return int(str_result[len(str_result)-pin])

    @staticmethod
    def set_relay(pin):
        """
        Set relay in output

        :param pin: the pin
        """
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)  # inverted the relay is low in this state

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
