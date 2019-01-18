

from urllib.error import URLError

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from urllib.request import urlopen
from googleapiclient import http
from googleapiclient import errors

# --------------------------------------------------------------------------- #
# Client to connect to Google Drive
# --------------------------------------------------------------------------- #


class UploadDrive:

    def __init__(self):
        """Create an instance of UploadDrive."""
        self.gauth = GoogleAuth()
        self.connect()
        self.drive = GoogleDrive(self.gauth)

    def connect(self):
        """Connect to the drive with the flow
             """
        # https: // github.com / gsuitedevs / PyDrive / issues / 104
        self.gauth.LoadCredentialsFile("mycreds.txt")
        if self.gauth.credentials is None:
            # Authenticate if they're not there
            self.gauth.GetFlow()
            self.gauth.flow.params.update({'access_type': 'offline'})
            self.gauth.flow.params.update({'approval_prompt': 'force'})
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            # Initialize the saved creds
            self.gauth.Refresh()
        # Save the current credentials to a file
        self.gauth.SaveCredentialsFile("mycreds.txt")

    def write_file_on_cloud(self, path, title="values.csv"):
        """Create GoogleDriveFile instance
        :param path: path of the file
        :type path: str
        :param title: title in google drive
        :type title: str
        """
        self.connect()
        file1 = self.drive.CreateFile()
        file1.SetContentFile(path)
        file1['title'] = title
        file1.Upload()

    # Auto-iterate through all files that matches this query
    def find_file_title_on_cloud(self, title=''):
        """find a given file by its title on the cloud
        :param title:The title of the text file
        :type title: str
        :return file_id
        """
        self.connect()

        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))
            if file['title'] == title:
                print('found : ' + title)
                return file['title']
        print('file not found : ' + title)
        return 404

    def find_file_id_on_cloud(self, title=''):
        """Find a file by its id on the cloud
        :param title:The title of the text file
        :type title: str
        :return file_id
        """
        # results=service.files().list().execute()
        # file_list=results.get('items',[])
        self.connect()

        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))
            if file['title'] == title:
                print('found : ' + title)
                return file['id']

        return 404

    def download_file_from_cloud(self, file_id, path):
        """Download a Drive file's content to the local filesystem.
        :param file_id: ID of the Drive file that will downloaded.
        :type file_id: str
        :param path: where the file is written
        :type path: str
        :return if the download succeeded
        """
        self.connect()

        if self.internet_on():
            local_fd = open(path + "commands.csv", "wb")
            request = self.drive.auth.service.files().get_media(fileId=file_id)
            media_request = http.MediaIoBaseDownload(local_fd, request)
            while True:
                try:
                    download_progress, done = media_request.next_chunk()
                except errors.HttpError as error:
                    print('An error occurred: %s' % error)
                    return False
                if download_progress:
                    print('Download Progress: %d%%' % int(download_progress.progress() * 100))
                if done:
                    print('Download Complete')
                    return True
        else:
            return False

    def delete_file_on_cloud(self, file_title):
        # HTTP request DELETE
        """Permanently delete a file, skipping the trash.
        :param file_title: ID of the file to delete.
        :type file_title: str
        :return if file didn't delete
        """
        self.connect()

        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))
            if file['title'] == file_title:
                print('found : ' + file_title)
                self.drive.auth.service.files().delete(fileId=file['id']).execute()
        print('file not found : ' + file_title)
        return 404

    @staticmethod
    def internet_on():
        """Check if the connection to the internet works
        :return if there is a internet connexion
        """
        try:
            urlopen('http://216.58.192.142', timeout=1)
            return True
        except URLError as err:
            return False
