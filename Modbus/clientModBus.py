from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# --------------------------------------------------------------------------- #
# Client to connect to Venus
# --------------------------------------------------------------------------- #


class ClientModBus:
    """ Implementation of a client modbus
    """

    def __init__(self, address ='localhost', port=502):
        """ Initialize a modbus client instance
    :param address: The tcp address to connect to (default localhost)
    :param port: The modbus port to connect to (default 502)
    """
        self.UNIT = 0
        self.address = address
        self.port = port
        self.clientVenus = ModbusClient(self.address, port=self.port)
        self.registers = [["Power_PvOnGrid_L1", 811, 100, 1], ["Power_PvOnGrid_L2", 812, 100, 1],
                          ["Power_PvOnGrid_L3", 813, 100, 1], ["Power_Consumption_L1", 817, 100, 1],
                          ["Power_Consumption_L2", 818, 100, 1], ["Power_Consumption_L3", 819, 100, 1],
                          ["Power_Grid_L1", 820, 100, 1], ["Power_Grid_L2", 821, 100, 1],
                          ["Power_Grid_L3", 822, 100, 1], ["Power_Genset_L1", 824, 100, 1],
                          ["Power_Genset_L2", 824, 100, 1], ["Power_Genset_L3", 824, 100, 1],
                          ["Voltage_Battery", 840, 100, 0.1],
                          ["Current_Battery", 841, 100, 0.1], ["Power_Battery", 842, 100, 1],
                          ["Percent_Soc_Battery", 843, 100, 1], ["State_Battery", 844, 100, 1],
                          ["Amphours_Consumed_Battery", 845, 100, 0.1],
                          ["Sec_TimeToGo_Battery", 846, 100, 100], ["Alarms_High_Temperature", 34, 242, 1],
                          ["Alarms_LowBattery", 35, 242, 1], ["Alarms_Overload", 36, 242, 1],
                          ["State_Relay_0", 806, 100, 1], ["State_Relay_1", 807, 100, 1],
                          ["Power_AC_SetPoint", 2700, 100, 1], ["Percent_Max_Charge", 2701, 100, 1],
                          ["Percent_Max_Discharge", 2702, 100, 1]]  # Name, Register, unit ID, scale

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
        all_registers = []
        for y in range(0, len(self.registers)):
            self.UNIT = self.registers[y][2]    # unit id
            all_registers.append(self.registers[y][0])   # name
            all_registers.append(self.registers[y][3])  # scaling
            registers = self.clientVenus.read_holding_registers(self.registers[y][1], 1, unit=self.UNIT)   # value
            if registers.isError() != 0:    # test that we are not an error
                print(all_registers.index(len(all_registers)-1), registers)
            else:
                all_registers.append(registers.registers[0])

        return all_registers    # name;value

    def set_register(self, register, value):
        """ write registers


        :param register: a register to set
        :param value: a value of the registers to set
        """
        write_register = self.clientVenus.write_register(register, value)
        if write_register.isError() != 0:    # test that we are not an error
            print("write_register Error:", write_register)
