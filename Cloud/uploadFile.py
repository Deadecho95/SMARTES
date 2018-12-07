
# --------------------------------------------------------------------------- #
# Client to write and read file on the Raspberry PI
# --------------------------------------------------------------------------- #

import os.path


class UploadFile:
    def __init__(self):
        commandFile=2

    def addtotext(self, nametable, value=[]):
        length = value.length()
        # value.

    def writeFile(self, title):
        fichier = open(title, "w+")
        if os.path.exists(title):
            os.remove()
