import shutil
import os
 
start_path = '/home/su/su/tennis_mp4_0329/chouzhen_result'
end_path = '/home/su/su/tennis_mp4_0329/total_crop'
file = os.listdir(start_path)

num = '0000010000'

for str1 in file:
    str2 = start_path + f'/{str1}'
    file_path = os.listdir(str2)

    for str3 in file_path:
        img_path = str2 + f'/{str3}'
        new_img = shutil.copy(img_path,end_path+f'/{num}.jpg')
        num = str('00000'+str(int(num)+1))

print('done!')
    

