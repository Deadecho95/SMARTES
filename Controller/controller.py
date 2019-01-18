# --------------------------------------------------------------------------- #
# the controller
# --------------------------------------------------------------------------- #
from IO.INOUT import InOut
import Interface.Interface2 as face


class Controller:
    """ the controller manage the connection between
    the venus the raspberry and the cloud
    """
    AO_PIN = ['a', 'b']  # Channel of 4-20mA output
    RELAY_PINS = [37,38,40]  # pin of each relay
    DI_PIN = [1, 2, 3, 4]  # Channel of digital input
    NBR_RELAY = len(RELAY_PINS)  # nbr of relay

    def __init__(self, client_modbus, client_cloud, database):
        """

        :param client_modbus is the client for the modbus
        :param client_cloud is the client for the cloud
        :param database is the local database
        """
        
        self.run = 0
        self.command = []  # array from commands
        self.data = []  # all data from modbus
        self.client_modbus = client_modbus
        self.client_cloud = client_cloud
        self.database = database

        InOut.init()  # init IO
        for y in range(0, self.NBR_RELAY):
            InOut.set_relay(self.RELAY_PINS[y])  # set all relays

    def start_cycle(self):
        """
        start the cycle of the program
        :return:
        """

        self.read_modbus_values()
        self.connect_cloud()
        self.write_cloud()
        self.read_cloud()
        self.create_plot()
        self.check_output()
        self.write_modbus_values()

    def check_consumption(self):
        """
        check te consumption for the IO
        :return: state of battery and grid
        """
        batt_state = 0
        grid_l1 = 0
        grid_l2 = 0
        grid_l3 = 0
        pv_l1 = 0
        pv_l2 = 0
        pv_l3 = 0

        for y in range(0, len(self.data), 3):
            if self.data[y] == "Percent_Soc_Battery":   # check for battery %
                batt_state = self.data[y + 2]*self.data[y + 1]
            if self.data[y] == "Power_Grid_L1":   # check for load power l1
                grid_l1 = self.data[y + 2]*self.data[y + 1]
            if self.data[y] == "Power_Grid_L2":   # check for load power l2
                grid_l2 = self.data[y + 2]*self.data[y + 1]
            if self.data[y] == "Power_Grid_L3":   # check for load power l3
                grid_l3 = self.data[y + 2]*self.data[y + 1]
            if self.data[y] == "Power_PvOnGrid_L1":  # Check for pc power L1
                pv_l1 = self.data[y + 2]
            if self.data[y] == "Power_PvOnGrid_L2":  # Check for pc power L1
                pv_l2 = self.data[y + 2]*self.data[y + 1]
            if self.data[y] == "Power_PvOnGrid_L3":  # Check for pc power L1
                pv_l3 = self.data[y + 2]*self.data[y + 1]

        return [batt_state, grid_l1, grid_l2, grid_l3, pv_l1, pv_l2, pv_l3]

    def check_output(self):
        """
        Set all output
        :return:
        """
        data = self.check_consumption()
        power_pv = (data[4] + data[5] + data[6])  # Power on PV
        power_grid = (data[1] + data[2] + data[3])  # Power load
        soc_batt = data[0]  # percent charge battery

        power_nom_relay1 = 0
        power_nom_relay2 = 0
        power_nom_relay3 = 0
        power_nom_ao = 0

        for y in range(1, len(self.command)):
            if self.command[y][0] == "PowerNomRelay1":
                power_nom_relay1 = int(self.command[y][2])
            if self.command[y][0] == "PowerNomRelay2":
                power_nom_relay2 = int(self.command[y][2])
            if self.command[y][0] == "PowerNomRelay3":
                power_nom_relay3 = int(self.command[y][2])
            if self.command[y][0] == "PowerNomAO":
                power_nom_ao = int(self.command[y][2])

        analog_out_permit = InOut.read_digital_input(self.DI_PIN[0])
        relay1_permit = InOut.read_digital_input(self.DI_PIN[1])
        relay2_permit = InOut.read_digital_input(self.DI_PIN[2])
        relay3_permit = InOut.read_digital_input(self.DI_PIN[3])
        power_supply = 0

        #TEST
        ############
        soc_batt = 100
        #############

        # SET ANALOG OUTPUT (4-20mA)
        if (power_pv-power_grid >= 1) and (soc_batt >= 99) and analog_out_permit == 1 and power_nom_ao > 0:
            InOut.set_analog_output(self.AO_PIN[0], (power_pv-power_grid)/power_nom_ao*100)
            power_supply = power_nom_ao
        else:
            InOut.set_analog_output(self.AO_PIN[0], 0)

        # SET RELAY 1
        if (power_pv-power_grid >= power_nom_relay1 + power_supply) and (soc_batt >= 99) and relay1_permit == 1\
                and power_nom_relay1 > 0:  # if power extra >= pNom and soc >=99
            InOut.set_relay_value(self.RELAY_PINS[0], 1)
            power_supply = power_supply + power_nom_relay1
        else:
            InOut.set_relay_value(self.RELAY_PINS[0], 0)

        # SET RELAY 2
        if (power_pv-power_grid >= power_nom_relay2 + power_supply) and (soc_batt >= 99) and relay2_permit == 1 \
                and power_nom_relay2 > 0:
            InOut.set_relay_value(self.RELAY_PINS[1], 1)
            power_supply = power_supply + power_nom_relay2
        else:
            InOut.set_relay_value(self.RELAY_PINS[1], 0)

        # SET RELAY 3
        if (power_pv-power_grid >= power_nom_relay3 + power_supply) and (soc_batt >= 99) and relay3_permit == 1\
                and power_nom_relay3 > 0:
            InOut.set_relay_value(self.RELAY_PINS[2], 1)
            power_supply = power_supply + power_nom_relay3
        else:
            InOut.set_relay_value(self.RELAY_PINS[2], 0)

    def connect_cloud(self):
        """

        :return:
        """
        self.client_cloud.connect()

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
        # self.client_cloud.write_file_on_cloud(path="Files/Plot.html",title="Plot.html")

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
            if ok == 0:
                print("Error when read file commands.csv from cloud")
            else:
                print("file commands.csv read from cloud")
            if ok == 0:
                print("Error when read file commands.csv from cloud")
            else:
                print("file commands.csv read from cloud")
                file = open("Files/commands.csv", "r")

                lines = list(file)
                self.command.clear()
                for line in lines:
                    self.command.append(line.split(';'))
                file.close

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
        """
        write modbus registers from the command file
        :return:
        """
        for y in range(1, len(self.command)):
            if int(self.command[y][1]) != -1:
                value = int(self.command[y][2])
                register = int(self.command[y][1])
                self.client_modbus.connect()
                self.client_modbus.set_register(register, value)
                self.client_modbus.disconnect()
