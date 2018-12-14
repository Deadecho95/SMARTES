#---------------------------------------------------------------------------#
# import the various server implementations
# ---------------------------------------------------------------------------#
from widgetlords.pi_spi import *
import RPi.GPIO as GPIO

class In_out:

    def __init__(self, ):
        """ Initialize
        """
        init()
        self.outputs = Mod2AO()
        self.inputs = Mod8DI()

        GPIO.setmode(GPIO.BCM)

        self.set_relay(37)
        self.set_relay(38)
        self.set_relay(40)



    def set_analog_output(self, pin,value):
        """
        Set analog output 4-20mA
        (4mA at 745 D/A  -  20mA at 3723 D/A)

        :param pin: number of pin
        :param value: value of output in %
        """

        self.outputs.write_single(pin, (value*29.78+745))


    def read_digital_input(self, pin):
        """
        Read digital input on external card

        :param pin: number of pin
        :return: value on the pin
        """
        return self.inputs.read_single(pin)


    def set_relay(self, pin):
        """
        Set relay in output

        :param pin: the pin
        """
        GPIO.output(pin, GPIO.OUT)


    def set_relay_value(self, pin, value):
        """
        Set value of relay

        :param pin: number of pin
        :param value: value 0 for hight and 1 for hight
        """

        if value == 0:
            GPIO.output(pin, GPIO.LOW)
        else:
            GPIO.output(pin, GPIO.HIGH)


