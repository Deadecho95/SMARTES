from Controller.controller import Controller
from Modbus.clientModBus import ClientModBus

# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

client = ClientModBus("153.109.14.169", 502)
controller = Controller(client)
controller.getModbusValues()
"""t = Timer(5, controller.getModbusValues(), None)
t.start()"""
client.clientVenus.connect()
print(client.clientVenus.read_input_registers(5,1).registers[0])





