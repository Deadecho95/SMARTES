from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

# --------------------------------------------------------------------------- #
# Client to connect to Google Drive
# --------------------------------------------------------------------------- #


class UploadDrive:

    def __init__(self,drive):
        """ Initialize a client instance

    :param UNIT: The host to connect to (default 0x1)
    :param address: The tcp address to connect to (default localhost)
    :param port: The modbus port to connect to (default 502)
    """

        self.drive = GoogleDrive(gauth)

    def __send__(self,text='hello',titleText='a'):
        """ connect to ServerModBus
        """

        datetime.datetime.now().now.strftime("%Y-%m-%d %H:%M")

        file1 = self.drive.CreateFile({'title': titleText+'.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.

        file1.SetContentString(text) # Set content of the file from given string.
        file1.Upload()


# Auto-iterate through all files that matches this query
    def __read__(self,titleText='a'):
        b=0
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
            if file1['title']==titleText:
                print('found')
                b+=1
        if b==0:
            print('file not found')