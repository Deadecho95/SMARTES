from Cloud.uploadDrive import UploadDrive
from Controller.controller import Controller
from Modbus.clientModBus import ClientModBus
from Controller.localDataBase import LocalDataBase


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

client_modbus = ClientModBus("153.109.14.168", 502)
client_cloud = UploadDrive()
client_cloud.delete_file_on_cloud("ttt")
