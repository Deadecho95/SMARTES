# --------------------------------------------------------------------------- #
# the controller
# --------------------------------------------------------------------------- #
from Cloud.uploadDrive import UploadDrive as lient_modbus
from Controller.localDataBase import LocalDataBase as database
from Modbus.clientModBus import ClientModBus as client_cloud
import time


class Controller:
    """ Implementation of a client

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
            time.sleep(5)  # wait for secs
            self.read_modbus_values()
            self.write_cloud()
            self.read_cloud()
            self.check_consumption()

            self.write_modbus_values()

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
        file1 = self.client_cloud.find_file_title_on_cloud("values.csv")
        if file1 != 404:  # check if error
            self.client_cloud.delete_file_on_cloud(file1)    # delete old file
       # self.client_cloud.write_file_on_cloud("C:/users/chena/OneDrive/Documents/GitHub/SMARTES/Cloud/values.csv")   # write on cloud
        self.client_cloud.write_file_on_cloud("Files/values.csv")   # write on cloud
        print("file wrote")

    def read_cloud(self):
        """
        start the transmission to the battery
        :return:
        """
        file1 = self.client_cloud.find_file_id_on_cloud("commands.csv")  # find file on cloud
        if file1 == 404:
            print("error file not found")   # not found
        else:
            #ok = self.client_cloud.download_file_from_cloud(file1, "C:/users/chena/OneDrive/Documents/GitHub/SMARTES/Cloud")    # download command file
            ok = self.client_cloud.download_file_from_cloud(file1, "Files/")    # download command file

            if ok == 0:
                print("Error when read file from cloud")
            else:
                print("file read from cloud")

    def read_modbus_values(self):
        """
        get value from the modbus
        :return:
        """
        self.client_modbus.connect()
        self.data = self.client_modbus.get_registers()
        self.client_modbus.disconnect()

    def write_modbus_values(self):

        for y in range(0, ):
            database.

    def set_modbus_value(self):
        """
        set value to the modbus
        :return:
        """

        self.client_modbus.connect()
        self.set_register("""value""")
        self.disconnect()












