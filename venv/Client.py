#---------------------------------------------------------------------------#
# import the various server implementations
#---------------------------------------------------------------------------#
import pymodbus
from pymodbus.client.sync import ModbusTcpClient

#---------------------------------------------------------------------------#
# configure the client logging
#---------------------------------------------------------------------------#
import logging

from pymodbus.server.sync import ModbusTcpServer

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = ModbusTcpClient("127.0.0.1")
client.connect()
client.write_coil(1, True)
result = server.read_coils(1,1)
print(result.bits[0])
client.close()