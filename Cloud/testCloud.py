from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Cloud.uploadDrive import UploadDrive

client= UploadDrive()
fileID=client.find_file_on_cloud("ttt.txt")
client.delete_file_on_cloud(fileID)
