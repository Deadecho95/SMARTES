from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# --------------------------------------------------------------------------- #
# Client to connect to Venus
# --------------------------------------------------------------------------- #
class ClientModBus:
    """ Implementation of a client
    """
    def __init__(self,UNIT=0x1,address ='localhost', port=502):
        """ Initialize a client instance

    :param UNIT: The host to connect to (default 0x1)
    :param address: The tcp address to connect to (default localhost)
    :param port: The modbus port to connect to (default 502)
    """
        self.UNIT = UNIT
        self.address = address
        self.port = port
        self.clientVenus = ModbusClient(self.address, port=self.port)
    def Connect(self,clientVenus):
        """ connect to ServerModBus


    :param UNIT: The host to connect to (default 0x1)
    :param address: The tcp address to connect to (default localhost)
    :param port: The modbus port to connect to (default 502)
    """
        self.clientVenus.connect()
    def Disconnect(self):
        """ Disconnect from the ServerModBus
        """
        self.clientVenus.close()

    def _get_registers(self):
        """ read registers
        """

        self.veBus = self.clientVenus.read_holding_registers(3, 58, unit=self.UNIT)
        self.solarCharger = self.clientVenus.read_holding_registers(771,20, unit=self.UNIT)
        self.pvInverter = self.clientVenus.read_holding_registers(1026,14, unit=self.UNIT)
        self.battery = self.clientVenus.read_holding_registers(259,61, unit=self.UNIT)
        self.batteryExtraParam = self.clientVenus.read_holding_registers(1282,20, unit=self.UNIT)
        self.charger = self.clientVenus.read_holding_registers(2307,16, unit=self.UNIT)
        self.inverter = self.clientVenus.read_holding_registers(3100,29, unit=self.UNIT)
        self.tank = self.clientVenus.read_holding_registers(3000,6, unit=self.UNIT)
        self.grid = self.clientVenus.read_holding_registers(2600,10, unit=self.UNIT)
        self.gps = self.clientVenus.read_holding_registers(2800,8, unit=self.UNIT)
        self.generators = self.clientVenus.read_holding_registers(3200,24, unit=self.UNIT)
        self.temperature = self.clientVenus.read_holding_registers(3200,6, unit=self.UNIT)
        print("complete")

    def _set_register(self,register,value):
        """ write registers
        """
        self.writeregister = self.clientVenus.write_register(register,value)

    def _set_registers(self,register,value):
        """ write registers
        """
        self.writeregister = self.clientVenus.write_register(register,value)

"""
client = ModbusClient('localhost', port=5020)
client.connect()


rr = client.read_holding_registers(1, 1, unit=UNIT)
result = client.read_holding_registers(3000, 6, unit=UNIT)
for i in range (0,6):
    print(result.registers[i])
#--------------------------------------#
"""