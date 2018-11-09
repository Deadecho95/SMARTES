from pymodbus.client.sync import ModbusTcpClient as ModbusClient



UNIT = 0x1

client = ModbusClient("localhost", port=5020)
client.connect()

result = client.read_holding_registers(3000, 6, unit=UNIT)


for i in range(0, 6):
    if result.isError() == 0:    # test that we are not an error
        print(result.registers[i])
    else:
        print(result);
        break
client.close()
