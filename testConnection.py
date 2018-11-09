from pymodbus.client.sync import ModbusTcpClient as ModbusClient

UNIT = 0x1

client = ModbusClient("153.109.7.29", port=502)
client.connect()

result = client.read_holding_registers(3000, 6, unit=UNIT)


for i in range(0, 6):
    print(result)

client.close()
