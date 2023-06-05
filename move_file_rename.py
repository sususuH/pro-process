import shutil
import os
 
start_path = './'
end_path = './merger'
file = os.listdir(start_path)

str2 = []
str3 = []
str4 = ['./merger/crops','./merger/labels']

dict_a = {}

num = '0000020000'
for str1 in file:
    if str1[0:7] == 'predict':
        str2.append(f'./{str1}/crops')
        str3.append(f'./{str1}/labels')
        
if not os.path.exists(str4[0]):
        os.makedirs(str4[0])

if not os.path.exists(str4[1]):
    os.makedirs(str4[1])

for i in range(len(str2)):
    for n in os.listdir(str2[i]):
        imgs_path = str2[i] + '/' + n
        labels_path = str3[i] + '/' + n.split('.')[0] +'.txt'
        if imgs_path.split('/')[3].split('.')[0] == labels_path.split('/')[3].split('.')[0]:
            dict_a[imgs_path] = labels_path


for imgs,labels in dict_a.items():
    new_img = shutil.copy(imgs,str4[0]+f'/{num}.jpg')
    new_labels = shutil.copy(labels,str4[1]+f'/{num}.txt')
    num = str('00000'+str(int(num)+1))

print("crops len:" , len(os.listdir('./merger/crops')))
print("labels len:" , len(os.listdir('./merger/labels')))
print(len(dict_a))
print("done!")
