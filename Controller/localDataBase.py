# --------------------------------------------------------------------------- #
# Client to write and read file on the Raspberry PI
# --------------------------------------------------------------------------- #

import os.path
import datetime

# --------------------------------------------------------------------------- #
# Client to handle local files
# --------------------------------------------------------------------------- #


class LocalDataBase:
    """Create an instance of UploadDrive."""

    """Read GoogleDriveFile instance with title 'Hello.txt'
    :param path : The title of the text file
    :type path : The path of the file
    """

    def __init__(self, path="Files/values.csv",title="Smartes\n"):
        self.path = path
        self.file = open(self.path, "w+")
        self.file.close()
        self.header = False

    """ Append text to the end of a local file
    :param values : Array of key value table
    :type values : tab [string,int]     
    """
    def add_text(self, values=[]):
        date = datetime.datetime.now().now().strftime("%Y-%m-%d %H:%M")
        # Add an Header at the beginning power voltage
        self.file = open(self.path, "w+")

        if not self.header:
            
            i = 0
            self.file.write("datetime" + ";")
            
            for value in values:
                if i %2 == 0:
                    self.file.write(str(value) + ";")
                else:
                    ++i
            self.file.write(";\n") # end of line
            self.header = True # header done


        # Write the values date;val1;val2;val3
        self.file = open(self.path, "a")
        self.file.write(date + ";")
        i = 0
        for value in values:
            if i % 2 == 1:
                self.file.write(str(value) + ";")
            else:
                ++i

        self.file.write(";\n")
        self.file.close()
    #def readifEmpty(self):
    #    self.file = open(self.path, "r")
     #   if
    """Delete the file
    """
    def delete_file(self):
        os.remove(self.path)

