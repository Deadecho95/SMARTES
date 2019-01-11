from Cloud.uploadDrive import UploadDrive
from Controller.controller import Controller
from Modbus.clientModBus import ClientModBus
from Controller.localDataBase import LocalDataBase


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

client_modbus = ClientModBus("153.109.14.172", 502)
client_cloud = 0
database = LocalDataBase()
controller = Controller(client_modbus, client_cloud, database)
controller.start_cycle()
