from pymodbus.client.sync import ModbusTcpClient as ModbusClient

"""clientsystem = ModbusClient(100, "153.109.14.169", 502)
clientveBus = ModbusClient(242, "153.109.14.169", 502)
clientbattery = ModbusClient(225, "153.109.14.169", 502)"""

UNIT = [46,
247,
245,
243,
242,
100,
1,
2,
3,
4,
5,
6,
7,
8,
9,
10,
11,
12,
20,
21,
22,
23,
24,
25,
26,
27,
28,
29,
30,
31,
32,
33,
34,
40,
41,
42,
43,
44,
45,
46,
239,
238,
237,
236,
235,
233,
225
]


unit = 100

client = ModbusClient("153.109.14.172", port=502)
client.connect()

batt_soc = client.read_holding_registers(address=843, count=1, unit=100)
if batt_soc.isError() != 0:    # test that we are not an error
    print("Bat_soc: ", batt_soc)
else:
    for y in range(0, len(batt_soc.registers)): # print the value
        print("Bat_soc: ", batt_soc.registers[y])
client.close()
