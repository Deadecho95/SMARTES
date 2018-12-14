# --------------------------------------------------------------------------- #
# Client to write and read file on the Raspberry PI
# --------------------------------------------------------------------------- #

import os.path


class LocalDataBase:

    def __init__(self):
        self.path = "command.txt"
        self.file = open(self.path, "w+")
        self.file.write("SMARTES")
        self.file.close()

    # append text to the end of a file
    def add_text(self, values=[]):
        length = values.length()
        self.file.open(self.path, "a")
        i = 0
        for value in values:
            self.file.write(value + ";")
            if i == 1:
                i = 0
                self.file.write(";\n")
            ++i

    def delete_text(self):
        os.remove(self.path)
