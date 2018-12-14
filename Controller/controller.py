# --------------------------------------------------------------------------- #
# the controller
# --------------------------------------------------------------------------- #
from Cloud.uploadDrive import UploadDrive
from Controller.localDataBase import LocalDataBase
from Modbus.clientModBus import ClientModBus
import time


class Controller:
    """ Implementation of a client

    :param client: The clientModbus to connect to

    """

    def __init__(self, client_modbus, client_cloud, database):
        """ Initialize
        """
        self.name = 0
        self.data = 0
        self.client_modbus = client_modbus
        self.client_cloud = client_cloud
        self.database = database

    def start_cycle(self):
        """
        start the cycle of the program
        :return:
        """
        while True:
            time.sleep(30)  # wait for secs
            self.read_modbus_values()
            self.start_transmit_to_cloud()
            self.check_consumption()
            self.start_transmit_to_battery()

    def check_consumption(self):
        """
        check te consumption for the IO
        :return:
        """
        for y in range(0, len(self.data)):
            if self.data[y] == "Percent_Soc_Battery":   # check for battery %
                batt_state = self.data[y + 1]
            if self.data[y] == "Power_Consumption_L3":   # check for consumption l1
                cons_l1 = self.data[y + 1]
            if self.data[y] == "Power_Consumption_L2":   # check for consumption l2
                cons_l2 = self.data[y + 1]
            if self.data[y] == "Power_Consumption_L2":   # check for consumption l3
                cons_l3 = self.data[y + 1]



    def write_cloud(self):
        """
        start the transmission to the cloud
        :return:
        """
        self.database.add_text(self.data)    # write data on local database
        file1 = self.client_cloud.find_file_on_cloud("values.csv")
        if file1 == 404:  # check if error
            print("error file not found")
        else:
            self.client_cloud.delete_file_on_cloud(file1)    # delete old file
            self.client_cloud.write_file_on_cloud("/home/pi/Desktop")   # write on cloud
            print("file wrote")

    def read_cloud(self):
        """
        start the transmission to the battery
        :return:
        """
        file1 = self.client_cloud.find_file_on_cloud("command.csv")  # find file on cloud
        if file1 == 404:
            print("error file not found")   # not found
        else:
            ok = self.client_cloud.download_file_from_cloud(file1, "/home/pi/Desktop")    # download command file
            if ok == 0:
                print("Error when read file from cloud")
            else:
                print("file read from cloud")

    def read_modbus_values(self):
        """
        get value from the modbus
        :return:
        """
        self.client.connect()
        self.data = self.client.get_registers()
        self.client.disconnect()

    def set_modbus_value(self):
        """
        set value to the modbus
        :return:
        """

        self.client.connect()
        self.set_register("""value""")
        self.disconnect()












