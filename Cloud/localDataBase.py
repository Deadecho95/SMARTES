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
        for value in values:
            self.file.write("\n" + value)

    def delete_text(self):
        os.remove(self.path)
