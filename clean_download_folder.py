import os
from datetime import datetime
import shutil

# CONSTANTS
MAX_DAYS_MOVE = 14
MAX_DAYS_DELETE = 20

# Conigure current directory to downloads folder
os.chdir(r'C:\Users\User\Downloads')

unused_folder = os.path.join(os.getcwd(), 'Unused')
log_file = os.path.join(unused_folder, 'log.txt')

# Returns how many days from today was the file/folder last accessed    
def get_time_diff(name, dirpath):
    file_path = os.path.join(dirpath, name)
    accessed_time = datetime.fromtimestamp(os.stat(file_path).st_atime)
    time_diff = (datetime.today()-accessed_time).days
    return time_diff

# Moves file/folder from download folder to Unused folder
def move_file(file, dirpath):
    old_path = os.path.join(dirpath, file)
    new_path = os.path.join(unused_folder, file)
    os.rename(old_path, new_path)

# open log file to track what has changed
with open(log_file, 'w') as f:
    # Go through unused folder and delete files/folders that have been there for more than MAX_DAYS_DELETE days
    for dirpath, dirname, filenames in os.walk(unused_folder):
        f.write(datetime.today().strftime('-----DELETED %m/%d/%Y, %H:%M:%S-----\n\n'))
        for folder in dirname: 
            time_diff = get_time_diff(folder, dirpath)
            if time_diff>MAX_DAYS_DELETE:
                shutil.rmtree(os.path.join(dirpath, folder))
                f.write(folder+"\n")
        for file in filenames:
            time_diff = get_time_diff(file, dirpath)
            if time_diff>MAX_DAYS_DELETE:
                os.remove(os.path.join(dirpath, file))
                f.write(file+"\n")
        break
        
    # Go through download folder and move files/folders that have been there for more than MAX_DAYS_MOVE days to the Unused folder
    for dirpath, dirname, filenames in os.walk(os.getcwd()):
        f.write(datetime.today().strftime('\n\n-----MOVED %m/%d/%Y, %H:%M:%S-----\n\n'))
        for folder in dirname:
            # skip unused folder 
            if folder == 'Unused':
                continue
            time_diff = get_time_diff(dirpath, folder)
            if time_diff>MAX_DAYS_MOVE:
                move_file(folder, dirpath)
                f.write(folder+"\n")

        for file in filenames:
            time_diff = get_time_diff(dirpath, file)
            if time_diff>MAX_DAYS_MOVE:
                move_file(file, dirpath)
                f.write(file+"\n")
        break