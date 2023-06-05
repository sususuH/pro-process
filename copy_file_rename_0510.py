import shutil
import os
 
start_path = '/home/su/su/labels_crop1-8/new0.2'
end_path = '/home/su/su/labels_crop1-8/rename'
files = os.listdir(start_path)

for file in files:
    start_file_path = os.path.join(start_path, file)
    rename = 'new0.2_' + file
    end_file_path = os.path.join(end_path, rename)
    shutil.copy(start_file_path, end_file_path)

print("done!")
