from Cloud.uploadDrive import UploadDrive
from Controller.controller import Controller
from Modbus.clientModBus import ClientModBus
from Controller.localDataBase import LocalDataBase


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

client_modbus = ClientModBus("153.109.14.169", 502)
client_cloud = UploadDrive()
dataBase = LocalDataBase()
controller = Controller(client_modbus, client_cloud, dataBase)






