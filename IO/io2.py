import pispi.py
from ai.mcp3208 import MCP3208
from ao.mcp4922 import MCP4922

import time

a = MCP3208()

# The resistor value of AI board is 150ohm.
while True:
    for i in range(8):
        volt = a.read_channel(i)

    time.sleep(1)

AO - MCP4922


a = MCP4922()

# Set gain
a.set_gain(2)

# Output analog voltage to channel A
a.output_voltage(channel='a', volt=2.5)

# Output analog voltage to channel B
a.output_voltage(channel='b', volt=1.5)
