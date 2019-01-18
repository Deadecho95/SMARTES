
from IO.chip.mcp4922 import MCP4922
import time

while True:

    time.sleep(1)

    a = MCP4922()

    # Set gain
    a.set_gain(1)

    # Output analog voltage to channel A
    a.output_percent(channel='b', percent=3)

    a.output_percent(channel='a', percent=3)
