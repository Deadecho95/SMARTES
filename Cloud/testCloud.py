""""
import webbrowser


url = 'http://docs.python.org/'

chrome_path = '/usr/lib/firefox-esr %s'

webbrowser.get(chrome_path).open(url)
"""""
import Cloud.uploadDrive as drive
my_drive = drive.UploadDrive()
fileId = my_drive.find_file_id_on_cloud("values.csv")
#fileName = my_drive.find_file_title_on_cloud(fileId)
my_drive.download_file_from_cloud(fileId, "")
my_drive.write_file_on_cloud("../Files/values.csv")
