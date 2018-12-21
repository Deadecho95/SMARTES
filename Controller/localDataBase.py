# --------------------------------------------------------------------------- #
# Client to write and read file on the Raspberry PI
# --------------------------------------------------------------------------- #

import os.path
import datetime


class LocalDataBase:
    """Read GoogleDriveFile instance with title 'Hello.txt'
          :param title:The title of the text file
          :return file_id
    """

    def __init__(self):
        self.path = "values.csv"
        self.file = open(self.path, "w+")
        self.file.write("SMARTES\n")
        self.file.close()
        self.header = False

    """ Append text to the end of a file
            :param values:Array of key value table      
    """

    def add_text(self, values=[]):
        date = datetime.datetime.now().now().strftime("%Y-%m-%d %H:%M")
        # Add an Header at the beginning power voltage
        if not self.header:
            self.file = open(self.path, "w+")
            i = 0
            self.file.write("datetime" + ";")

            for value in values:
                if i == 0:
                    self.file.write(str(value) + ";")
                if i == 1:
                    i = 0
                ++i
            self.file.write(";\n")
            self.header = True
        # Write the values date;val1;val2;val3
        self.file = open(self.path, "a")
        self.file.write(date + ";")
        i = 0
        for value in values:
            if i == 1:
                self.file.write(str(value) + ";")
                i = -1
            ++i

        self.file.write(";\n")
        self.file.close()

    """Delete the file
      """

    def delete_file(self):
        os.remove(self.path)

