from clientModBus import ClientModBus
from uploadDrive import UploadDrive

# --------------------------------------------------------------------------- #
# the controller
# --------------------------------------------------------------------------- #


class Controller:
    """ Implementation of a client

    :param client: The clientModbus to connect to

    """

    def __init__(self, client):
        """ Initialize
        """
        self.name = 0
        self.data = 0
        self.client = client

    def startTransmittToCloud(self):
        """
        start the transmission from the battery to the cloud
        :return:
        """
        self.getModbusValues()
        self.processingValues()
        self.transmittValue()

    def startTransmittToBattery(self):
            """
            start the transmission from the battery to the cloud
            :return:
            """

    def getModbusValues(self):
        """
        get value from the modbus
        :return:
        """
        self.client.connect()
        self.data = self.client.get_registers()
        self.client.disconnect()

    def setModbusValue(self):
        """
        set value to the modbus
        :return:
        """

        self.client.connect()
        self.set_register("""value""")
        self.disconnect()

    def setModbusValues(self):
        """
        set values to the modbus
        :return:
        """

        self.client.connect()
        self.client.set_registers("""value""")
        self.client.disconnect()

    def WriteCloud(self):
        """
        transmitt registers and names to the cloud
        :return:
        """
        i = 0
        while i <= len(self.data):
            """uploddrive(data[i],data[i+1].registers)"""   # data[i] = name // data[i+1].registers = list
            i = i+2


