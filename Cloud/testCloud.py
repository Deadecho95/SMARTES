from Cloud.uploadDrive import UploadDrive
from pydrive.files import GoogleDriveFile
client = UploadDrive()
client.write_file_on_cloud("ggdd", "tttffff")

fileId = client.find_file_on_cloud("ttt.txt")
gdf =GoogleDriveFile(fileId)
#client.delete_file_on_cloud(fileId)