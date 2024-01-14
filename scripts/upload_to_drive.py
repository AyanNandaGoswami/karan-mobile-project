from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime
import os

# Authenticate and create the GoogleDrive instance
gauth = GoogleAuth()
gauth.CommandLineAuth()  # Use CommandLineAuth instead of LocalWebserverAuth
drive = GoogleDrive(gauth)

PARENT_FOLDER_ID = '1QGvoBRFquE0ktklFFf4GRLXteNj-pcMO'


def take_backup():
    backup_command = 'mysqldump -u admin -p karan_enterprise_db > backup.sql'
    os.system(backup_command)


def upload_file():
    file_name = f'karan_enterprise_{datetime.datetime.now().date()}.sql'
    file = drive.CreateFile({'title': file_name, 'parents': [{'kind': 'drive#fileLink', 'id': PARENT_FOLDER_ID}]})
    file.SetContentFile('/home/ubuntu/karan-mobile-project/scripts/backup.sql')
    file.Upload()

    # delete backup file
    os.system('rm backup.sql')


if __name__ == '__main__':
    take_backup()
    upload_file()


