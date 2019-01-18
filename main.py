from Cloud.driveManager import UploadDrive
from Controller.controller import Controller
from Modbus.clientModBus import ClientModBus
from Controller.localDataBase import LocalDataBase
import time

# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

client_modbus = ClientModBus("153.109.14.172", 502)  # the clientmodbus
client_cloud = UploadDrive()  # the client cloud
database = LocalDataBase()
controller = Controller(client_modbus, client_cloud, database)  # create new controller with clients to connect

while True:
    controller.start_cycle()  # start the program
    time.sleep(15)
