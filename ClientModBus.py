from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# --------------------------------------------------------------------------- #
# Client to connect to Venus
# --------------------------------------------------------------------------- #


class ClientModBus:
    """ Implementation of a client modbus
    """

    def __init__(self, UNIT=0x1, address ='localhost', port=502):
        """ Initialize a client instance

    :param UNIT: The host to connect to (default 0x1)
    :param address: The tcp address to connect to (default localhost)
    :param port: The modbus port to connect to (default 502)
    """
        self.UNIT = UNIT
        self.address = address
        self.port = port
        self.clientVenus = ModbusClient(self.address, port=self.port)
        self.veBus

    def connect(self):
        """ connect to ServerModBus
        """

        self.clientVenus.connect()

    def disconnect(self):
        """ Disconnect from the ServerModBus
        """
        self.clientVenus.close()

    def get_registers(self):
        """ read registers

    :return allRegisters: the list of all registers
        """

        veBus = self.clientVenus.read_holding_registers(3, 58, unit=self.UNIT)
        solarCharger = self.clientVenus.read_holding_registers(771,20, unit=self.UNIT)
        spvInverter = self.clientVenus.read_holding_registers(1026,14, unit=self.UNIT)
        battery = self.clientVenus.read_holding_registers(259,61, unit=self.UNIT)
        batteryExtraParam = self.clientVenus.read_holding_registers(1282,20, unit=self.UNIT)
        charger = self.clientVenus.read_holding_registers(2307,16, unit=self.UNIT)
        inverter = self.clientVenus.read_holding_registers(3100,29, unit=self.UNIT)
        tank = self.clientVenus.read_holding_registers(3000,6, unit=self.UNIT)
        grid = self.clientVenus.read_holding_registers(2600,10, unit=self.UNIT)
        gps = self.clientVenus.read_holding_registers(2800,8, unit=self.UNIT)
        generators = self.clientVenus.read_holding_registers(3200,24, unit=self.UNIT)
        temperature = self.clientVenus.read_holding_registers(3200,6, unit=self.UNIT)
        print("complete")

        allRegisters = [veBus, solarCharger, spvInverter, battery, batteryExtraParam, charger, inverter, tank,
                        grid, gps, generators, temperature]
        return allRegisters

    def _set_registers(self, register, value):
        """ write registers


        :param register: a list of all registers to set
        :param value: a list of all value of the registers to set
        """
        # self.writeRegister = self.clientVenus.write_register(register,value)

    def _set_register(self,register,value):
        """ write registers


        :param register: a register to set
        :param value: a value of the registers to set
        """
        self.writeRegister = self.clientVenus.write_register(register,value)

