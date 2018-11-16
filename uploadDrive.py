from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime


# --------------------------------------------------------------------------- #
# Client to connect to Google Drive
# --------------------------------------------------------------------------- #


class UploadDrive:

    def __init__(self):
        """ Initialize a client instance

    :param drive: The Drive connected
    """

        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
        self.drive = GoogleDrive(gauth)

    def send(self, text='hello', title='a'):
        """ connect to ServerModBus
        """
        datetime.datetime.now().now.strftime("%Y-%m-%d %H:%M")
        file1 = self.drive.CreateFile({'title': title+'.txt'})

# Create GoogleDriveFile instance with title 'Hello.txt'.

        file1.SetContentString(text) # Set content of the file from given string.
        file1.Upload()


# Auto-iterate through all files that matches this query
    def read(self, title='a'):
        b = 0

        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:

            print('title: %s, id: %s' % (file1['title'], file1['id']))
            if file1['title'] == title:
                print('found')
                b += 1
        if b == 0:
            print('file not found')
    def addtotext(self,nametable,value=[]):
        length=value.length()
        #value.