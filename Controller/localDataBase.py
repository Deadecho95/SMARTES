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

    def __init__(self, path="C:/Users/chena/OneDrive/Documents/GitHub/SMARTES/Files/values.csv",title="Smartes\n"):
        """
        init function
        :param path of the file
        :param title of the file
        """
        self.path = path
        self.file = open(self.path, "w+")
        self.file.close()
        self.header = False


    def add_text(self, values=[]):
        """ Append text to the end of a local file
        :param values : Array of key value table
        """
        date = datetime.datetime.now().now().strftime("%Y-%m-%d %H:%M")
        # Add an Header at the beginning power voltage

        if not self.header:  # add a header
            self.file = open(self.path, "w+")
            i = 0
            self.file.write("datetime" + ";")  # add time
            
            for value in values:    # write header
                if i %2 == 0:
                    self.file.write(str(value) + ";")
                i = i+1
            self.file.write(";\n") # end of line
            self.header = True # header done
            self.file.close()

        # Write the values date;val1;val2;val3
        self.file = open(self.path, "a")
        self.file.write(date + ";")  # write date
        i = 0
        for value in values:    # write values
            if i % 2 == 1:
                self.file.write(str(self.twos_comp(value, 16)) + ";")
            i = i+1

        self.file.write(";\n")
        self.file.close()
    #def readifEmpty(self):
    #    self.file = open(self.path, "r")
     #   if
    """Delete the file
    """
    def delete_file(self):
        os.remove(self.path)

    @staticmethod
    def twos_comp(val, bits):
        """compute the 2's complement of int value val"""
        if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)  # compute negative value
        return val
