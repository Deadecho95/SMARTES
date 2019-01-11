# --------------------------------------------------------------------------- #
# the controller
# --------------------------------------------------------------------------- #
from Cloud.uploadDrive import UploadDrive
from Controller.localDataBase import LocalDataBase
from Modbus.clientModBus import ClientModBus
from IO.INOUT import InOut
import time
import keyboard  # Using module keyboard
import Interface.Interface2 as face


class Controller:
    """ the controller manage the connection between
    the venus the raspberry and the cloud
    """

    RELAY_PINS = [37,38,40] #pin of each relay
    NBR_RELAY = len(RELAY_PINS) #nbr of relay

    def __init__(self, client_modbus, client_cloud, database):
        """

        :param client_modbus is the client for the modbus
        :param client_cloud is the client for the cloud
        :param database is the local database
        """
        self.command = 0 #array from commands
        self.data = 0 #all data from modbus
        self.client_modbus = client_modbus
        self.client_cloud = client_cloud
        self.database = database

        InOut.init() #init IO
        for y in range(0, self.NBR_RELAY):
            InOut.set_relay(self.RELAY_PINS[y]) #set all relays


    def start_cycle(self):
        """
        start the cycle of the program
        :return:
        """
        while True:
            time.sleep(15)  # wait for secs
            self.read_modbus_values()
            self.write_cloud()
            self.read_cloud()
            self.create_plot()
            self.set_relays()
            self.set_analog_output()




    def set_analog_output(self):
        """
        set analog output
        :return:
        """
        data = self.check_consumption()
        self.check_output_analog('a',data,100)

    def set_relays(self):
        """
        set relays
        :return:
        """
        data = self.check_consumption()

        for y in range(0, self.NBR_RELAY):  #write n relays
            self.check_relay(self.RELAY_PINS[y],data, 100)


    def check_consumption(self):
        """
        check te consumption for the IO
        :return: state of battery and grid
        """
        batt_state = 0
        grid_l1 = 0
        grid_l2 = 0
        grid_l3 = 0

        for y in range(0, len(self.data), 2):
            if self.data[y] == "Percent_Soc_Battery":   # check for battery %
                batt_state = self.data[y + 1]
            if self.data[y] == "Power_Grid_L1":   # check for grid power l1
                grid_l1 = self.data[y + 1]
            if self.data[y] == "Power_Grid_L1":   # check for grid power l2
                grid_l2 = self.data[y + 1]
            if self.data[y] == "Power_Grid_L1":   # check for grid power l3
                grid_l3 = self.data[y + 1]

        return [batt_state, grid_l1, grid_l2, grid_l3]

    def check_relay(self, pin, data, pmin):
        """
        Set the relay
        :param pin: number pin
        :param data: data to compare
        :param pmin: order to compare
        """
        """if (data[1] + data[2] + data[3]) <= pmin and InOut.read_digital_input(pin)<=0: # if power PV is higher than and DIN is not 1
            InOut.set_relay_value(pin,1)
        else:
            InOut.set_relay_value(pin,0)
"""
    def check_output_analog(self, pin, data, pnom):
        """
        Set analog output
        :param pin: number of pin
        :param data: power to grid
        :param pnom : power nominal to set 100%
        """
        if (data[1] + data[2] + data[3]) <= 0:
            InOut.set_analog_output(pin, (data[1] + data[2] + data[3])/pnom*100)
        else:
            InOut.set_analog_output(pin, 0)

    def write_cloud(self):
        """
        start the transmission to the cloud
        :return:
        """
        self.database.add_text(self.data)    # write data on local database
        file1 = self.client_cloud.find_file_title_on_cloud("values.csv")
        if file1 != 404:  # check if error
            self.client_cloud.delete_file_on_cloud(file1)    # delete old file
        self.client_cloud.write_file_on_cloud("Files/values.csv")   # write on cloud
        print("file wrote")

    def read_cloud(self):
        """
        download command.csv file from cloud
        :return:
        """
        file1 = self.client_cloud.find_file_id_on_cloud("commands.csv")  # find file on cloud
        if file1 == 404:
            print("error file not found")   # not found
        else:
            ok = self.client_cloud.download_file_from_cloud(file1, "Files/")    # download command file
            file = open("commands.csv", "rw+")
            lines = list(file)
            self.command = lines.split(',')
            file.close
            if ok == 0:
                print("Error when read file commands.csv from cloud")
            else:
                print("file commands.csv read from cloud")

    def read_modbus_values(self):
        """
        get value from the modbus
        :return:
        """
        self.client_modbus.connect()
        self.data = self.client_modbus.get_registers()
        self.client_modbus.disconnect()

    def create_plot(self):
        face.Interface2.show_values()

    def write_modbus_values(self):

        for y in range(0, ):
            "readdatabase"

    def set_modbus_value(self):
        """
        set value to the modbus
        :return:
        """

        self.client_modbus.connect()
        self.set_register("""value""")
        self.disconnect()













