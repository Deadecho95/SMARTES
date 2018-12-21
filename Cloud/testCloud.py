from Cloud.uploadDrive import UploadDrive


def testcloud():

    drivetest = UploadDrive()
    drivetest.write_file_on_cloud("aa")
    drivetest.write_file_on_cloud("/files")
