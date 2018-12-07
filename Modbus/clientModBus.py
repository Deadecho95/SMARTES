from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# --------------------------------------------------------------------------- #
# Client to connect to Venus
# --------------------------------------------------------------------------- #


class ClientModBus:
    """ Implementation of a client modbus
    """

    def __init__(self, address ='localhost', port=502):
        """ Initialize a client instance

    :param UNIT: The host to connect to (default 0x1)
    :param address: The tcp address to connect to (default localhost)
    :param port: The modbus port to connect to (default 502)
    """
        self.UNIT = 0
        self.address = address
        self.port = port
        self.clientVenus = ModbusClient(self.address, port=self.port)



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

        self.UNIT = 100
        system = self.clientVenus.read_holding_registers(3, 58, unit=self.UNIT)
        if system.isError() != 0:    # test that we are not an error
            print("veBus:", system)

        self.UNIT = 242
        veBus = self.clientVenus.read_holding_registers(3, 58, unit=self.UNIT)
        if veBus.isError() != 0:    # test that we are not an error
            print("veBus:", veBus)

        solarCharger = self.clientVenus.read_holding_registers(771, 20, unit=self.UNIT)
        if solarCharger.isError() != 0:    # test that we are not an error
            print("solarCharger:", solarCharger)

        spvInverter = self.clientVenus.read_holding_registers(1026, 14, unit=self.UNIT)
        if spvInverter.isError() != 0:    # test that we are not an error
            print("spvInverter:", spvInverter)

        battery = self.clientVenus.read_holding_registers(259, 61, unit=self.UNIT)
        if battery.isError() != 0:    # test that we are not an error
            print("battery:", battery)

        batteryExtraParam = self.clientVenus.read_holding_registers(1282, 20, unit=self.UNIT)
        if batteryExtraParam.isError() != 0:    # test that we are not an error
            print("batteryExtraParam:", batteryExtraParam)

        charger = self.clientVenus.read_holding_registers(2307, 16, unit=self.UNIT)
        if charger.isError() != 0:    # test that we are not an error
            print("charger:", charger)

        inverter = self.clientVenus.read_holding_registers(3100, 29, unit=self.UNIT)
        if veBus.isError() != 0:    # test that we are not an error
            print("inverter:", inverter)

        tank = self.clientVenus.read_holding_registers(3000, 6, unit=self.UNIT)
        if tank.isError() != 0:    # test that we are not an error
            print("tank:", tank)

        grid = self.clientVenus.read_holding_registers(2600, 10, unit=self.UNIT)
        if grid.isError() != 0:    # test that we are not an error
            print("grid:", grid)

        gps = self.clientVenus.read_holding_registers(2800, 8, unit=self.UNIT)
        if gps.isError() != 0:    # test that we are not an error
            print("gps:", gps)

        generators = self.clientVenus.read_holding_registers(3200, 24, unit=self.UNIT)
        if generators.isError() != 0:    # test that we are not an error
            print("generators:", generators)

        temperature = self.clientVenus.read_holding_registers(3300, 6, unit=self.UNIT)
        if temperature.isError() != 0:    # test that we are not an error
            print("temperature:", temperature)

        print("complete")

        allRegisters = ["veBus", veBus, "solarCharger", solarCharger, "spvInverter", spvInverter, "battery", battery,
                        "batteryExtraParam", batteryExtraParam, "charger", charger, "inverter", inverter, "tank", tank,
                        "grid", grid, "gps", gps, "generators", generators, "temperature", temperature]

        return allRegisters

    def set_registers(self, register, value):
        """ write registers


        :param register: a list of all registers to set
        :param value: a list of all value of the registers to set
        """
        # self.writeRegister = self.clientVenus.write_register(register,value)

    def set_register(self,register,value):
        """ write registers


        :param register: a register to set
        :param value: a value of the registers to set
        """
        writeRegister = self.clientVenus.write_register(register,value)
        if writeRegister.isError() != 0:    # test that we are not an error
            print("writeRegister Error:", writeRegister)
