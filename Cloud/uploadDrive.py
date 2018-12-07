from urllib.error import URLError

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime
from urllib.request import urlopen
from apiclient import http
from apiclient import errors

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

    def write_file_on_cloud(self, text='hello', title='a'):
        """Create GoogleDriveFile instance with title 'Hello.txt'
        :param text: The text to be written
        :param title:The title of the text file
        """
        datetime.datetime.now().now.strftime("%Y-%m-%d %H:%M")
        file1 = self.drive.CreateFile({'title': title+'.txt'})
        file1.SetContentString(text)
        file1.Upload()
# Auto-iterate through all files that matches this query
    def find_file_on_cloud(self, title='a'):
        """Read GoogleDriveFile instance with title 'Hello.txt'
            :param title:The title of the text file
        """
        nb_files = 0
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
            if file1['title'] == title:
                print('found')
                nb_files += 1
        if nb_files == 0:
            print('file not found')

    def download_file_on_cloud(self, file_id, local_fd):
        """Download a Drive file's content to the local filesystem.

        Args:
          service: Drive API Service instance.
          file_id: ID of the Drive file that will downloaded.
          local_fd: io.Base or file object, the stream that the Drive file's
              contents will be written to.
        """
        request = self.drive.files().get_media(fileId=file_id)
        media_request = http.MediaIoBaseDownload(local_fd, request)
        while True:
            try:
                download_progress, done = media_request.next_chunk()
            except errors.HttpError as error:
                print
                'An error occurred: %s' % error
                return
            if download_progress:
                print
                'Download Progress: %d%%' % int(download_progress.progress() * 100)
            if done:
                print
                'Download Complete'
                return
    def addtotext(self,nametable,value=[]):
        length=value.length()
        #value.

    def writeFile(self,string,title):
        fichier = open(title,"w+")
        import os.path
        if os.path.exists(filepath):
            os.remove()

    def delete_file_on_cloud(self, file_id):
        # HTTP request DELETE
        # https: // www.googleapis.com / drive / v2 / files / fileId
        """Permanently delete a file, skipping the trash.

        Args:
          service: Drive API service instance.
          file_id: ID of the file to delete.
        """
        try:
            self.drive.files().delete(fileId=file_id).execute()
        except errors.HttpError as error:
            print
            'An error occurred: %s' % error

    @staticmethod
    def internet_on():
        try:
            urlopen('http://216.58.192.142', timeout=1)
            return True
        except URLError as err:
            return False

