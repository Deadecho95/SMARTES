from urllib.error import URLError

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from urllib.request import urlopen
from apiclient import http
from apiclient import errors
from pydrive.files import GoogleDriveFile


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

    def write_file_on_cloud(self, path):
        """Create GoogleDriveFile instance with title 'Hello.txt'
        :param path: path of the file
        """
        file1 = self.drive.CreateFile()
        file1.SetContentFile(path)
        file1['title'] = "values.csv"
        file1.Upload()

    # Auto-iterate through all files that matches this query
    def find_file_title_on_cloud(self, title=''):
        """Read GoogleDriveFile instance with title 'Hello.txt'
        :param title:The title of the text file
        :return file_id
        """
        # results=service.files().list().execute()
        # file_list=results.get('items',[])
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))
            if file['title'] == title:
                print('found : ' + title)
                return file['title']
        print('file not found : ' + title)
        return 404

    def find_file_id_on_cloud(self, title=''):
        """Read GoogleDriveFile instance with title 'Hello.txt'
        :param title:The title of the text file
        :return file_id
        """
        # results=service.files().list().execute()
        # file_list=results.get('items',[])
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))
            if file['title'] == title:
                print('found : ' + title)
                return file['id']
                print('file not found : ' + title)
        return 404

    def download_file_from_cloud(self, file_id, path):
        """Download a Drive file's content to the local filesystem.
          :param file_title: ID of the Drive file that will downloaded.
          :param path: where the file is write
          :return the success
        """
        if self.internet_on():
            local_fd = open(path + "commands.csv", "wb")
            request = self.drive.auth.service.files().get_media(fileId=file_id)
            media_request = http.MediaIoBaseDownload(local_fd, request)
            while True:
                try:
                    download_progress, done = media_request.next_chunk()
                except errors.HttpError as error:
                    print
                    'An error occurred: %s' % error
                    return False
                if download_progress:
                    print
                    'Download Progress: %d%%' % int(download_progress.progress() * 100)
                if done:
                    print
                    'Download Complete'
                    return True
        else:
            return False

    def delete_file_on_cloud(self, file_title):
        # HTTP request DELETE
        # https: // www.googleapis.com / drive / v2 / files / fileId
        """Permanently delete a file, skipping the trash.
          :param file_title: ID of the file to delete.
        """
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))
            if file['title'] == file_title:
                print('found : ' + file_title)
                self.drive.auth.service.files().delete(fileId=file['id']).execute()
        print('file not found : ' + file_title)
        return 404

    # def check_last_modification(self,file_id):
    # GET https://www.googleapis.com/drive/v2/changes/changeId

    @staticmethod
    def internet_on():
        """Check if the connection to the internet works
               :return the success
        """
        try:
            urlopen('http://216.58.192.142', timeout=1)
            return True
        except URLError as err:
            return False
