from ClientModBus import ClientModBus
from ClientModBus import ClientModBus
from threading import Timer

# --------------------------------------------------------------------------- #
# the controller
# --------------------------------------------------------------------------- #


class Controller:
    """ Implementation of a client
    """
    def __init__(self):
        """ Initialize
        """


    def transmittValue(self):
        """
        transmitt the values
        :return:
        """

    def getsModbusValues(self):
        """
        get value from th modbus
        :return:
        """
        client1 = ClientModBus(0x1,"153.109.7.29")
        client1.connect()
        self.data = client1.get_registers()
        client1.disconnect()

    def processingValues(self):
        """
        traitement of the vlues for the cloud
        :return:
        """
        for i in range(0, self.data.lenght()):
            for y in range(0, self.data[i].lenght()):
                value = self.data[i].re

