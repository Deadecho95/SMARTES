# --------------------------------------------------------------------------- #
# the controller
# --------------------------------------------------------------------------- #
from Cloud.uploadDrive import UploadDrive as lient_modbus
from Controller.localDataBase import LocalDataBase as database
from Modbus.clientModBus import ClientModBus as client_cloud
from IO.IO import InOut
import time
import keyboard  # Using module keyboard


class Controller:
    """ Implementation of a client

    """
    RELAY_PINS = [37,38,40]
    NBR_RELAY = len(RELAY_PINS)

    def __init__(self, client_modbus, client_cloud, database):
        """ Initialize
        """
        self.name = 0
        self.data = 0
        self.client_modbus = client_modbus
        self.client_cloud = client_cloud
        self.database = database

        InOut.init()
        for y in range(0, self.NBR_RELAY):
            InOut.set_relay(self.RELAY_PINS[y])
        InOut.set_relay_value(37, 1) #test -------------------------------

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
            self.set_relays()
            self.set_analog_output()
            InOut.set_relay_value(37,1)
            InOut.set_analog_output(1, 3723)



    def set_analog_output(self):
        """
        set analog output
        :return:
        """
        data = self.check_consumption()
        self.check_output_analog(1,data,100)

    def set_relays(self):
        """
        Write relay
        :return:
        """
        data = self.check_consumption()

        for y in range(0, self.NBR_RELAY):  #write n relays
            self.check_relay(self.RELAY_PINS[y],data, 100)

            self.write_modbus_values()
            try:  # used try so that if user pressed other than the given key error will not be shown
                if keyboard.is_pressed('q'):  # if key 'q' is pressed
                    print('You Pressed A Key!')
                    break  # finishing the loop
                else:
                    pass
            except:
                break  # if user pressed a key other than the given key the loop will break

    def check_consumption(self):
        """
        check te consumption for the IO
        :return:
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
        if (data[1] + data[2] + data[3]) <= pmin and InOut.read_digital_input(pin)<=0: # if power PV is higher than and DIN is not 1
            InOut.set_relay_value(pin,1)
        else:
            InOut.set_relay_value(pin,0)

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
        #self.client_cloud.write_file_on_cloud("C:/users/chena/OneDrive/Documents/GitHub/SMARTES/Files/values.csv")   # write on cloud
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
            "readdatabase"

    def set_modbus_value(self):
        """
        set value to the modbus
        :return:
        """

        self.client_modbus.connect()
        self.set_register("""value""")
        self.disconnect()













