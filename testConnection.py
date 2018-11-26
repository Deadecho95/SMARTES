from pymodbus.client.sync import ModbusTcpClient as ModbusClient



UNIT = 0x1

client = ModbusClient("153.109.14.169", port=502)
client.connect()

temperature = client.read_holding_registers(0, 6, unit=UNIT)
if temperature.isError() != 0:    # test that we are not an error
    print("temperature:", temperature)
else:
    for y in range(0, len(temperature.registers)): # stock registers in the
        print(temperature.registers[y])
client.close()
