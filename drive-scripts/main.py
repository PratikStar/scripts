# https://www.projectpro.io/recipes/upload-files-to-google-drive-using-python#mcetoc_1g02b3q8jbe
#
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile({
    'q': f"'1UTRbRz6K5RCnj5Jx6Nso0p3P5TE0Mwcn' in parents and trashed=false",
    'supportsAllDrives': True,  # Modified
    'driveId': '0AAAe4JaTB8B7Uk9PVA',  # Modified
    'includeItemsFromAllDrives': True,  # Added
    'corpora': 'drive'  # Added
}).GetList()

for file in file_list:
    print('title: %s, id: %s' % (file['title'], file['id']))

# exit()


myPath = "/Users/pratik/repos"

# The min size of the file in Bytes
mySize = '50000000'

# All the file paths will be stored in this list
filesList = []

for path, subdirs, files in os.walk(myPath):
    for name in files:
        fullpath = str(os.path.join(path, name))

        if os.path.islink(fullpath):
            continue
        fileSize = os.path.getsize(fullpath)

        if int(fileSize) >= int(mySize):
            print("The File: " + fullpath + " is: " + str(fileSize) + " Bytes")
            filesList.append(os.path.join(path, name))


for upload_file in filesList:
    # print(f"Uploading: {upload_file}")
    # gfile = drive.CreateFile({'parents': [{'id': '1UTRbRz6K5RCnj5Jx6Nso0p3P5TE0Mwcn'}]})
    #
    # gfile.SetContentFile(upload_file)
    # gfile.Upload()  # Upload the file.

    f = drive.CreateFile({
        'title': 'test.txt',
        'parents': [{
            'kind': 'drive#fileLink',
            'teamDriveId': '0AAAe4JaTB8B7Uk9PVA',
            'id': '1UTRbRz6K5RCnj5Jx6Nso0p3P5TE0Mwcn'
        }]
    })
    f.SetContentString('Hello World')

    f.Upload(param={'supportsTeamDrives': True})

    exit()
