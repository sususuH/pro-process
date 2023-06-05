import os
import json
import shutil
import time

start_path = '/home/su/su/打网球项目整理/Tennis_Data/total'
file_list = os.listdir(start_path)
end_path = '/home/su/su/打网球项目整理/Tennis_Data/select'  

std = {}
## 读取文件夹下的jpg和json同时存在的文件，并存入字典
for file in file_list:
    if file[-4:] == '.jpg':
        str1 = file[:-4] + '.json'
        if str1 in file_list:
            std[file] = str1

for jpg_name in list(std.keys()):
    json_name = jpg_name[:-4] + ".json"
    json_path = os.path.join(start_path, json_name)
    with open('{}'.format(json_path), 'r') as fr:
        json_content = json.load(fr)
        num = 0
        for i in range(len(json_content['shapes'])):
            if json_content['shapes'][i]['label'] == 'rackets':
                num += 1
        if num > 1 & num == 0:
            std.pop('{}'.format(jpg_name))
            # print(json_content['shapes'][i])   
        if num == 1 :
            for i in range(len(json_content['shapes'])):
                ### 更换标签的名字
                if json_content['shapes'][i]['label'] == 'rackets':
                    json_content['shapes'][i]['label'] = 'Racket'
                elif json_content['shapes'][i]['label'] == 'person':
                    json_content['shapes'][i]['label'] = 'Person'
                elif json_content['shapes'][i]['label'] == 'tennis':
                    json_content['shapes'][i]['label'] = 'Tennis'

                point = []
                score = 0
                ### 将网球拍上用框标记的点转换成点
                if json_content['shapes'][i]['shape_type'] == 'rectangle' and json_content['shapes'][i]['label'] in ['RacketTop','RacketT','RacketFrontCover']:
                    score = (json_content['shapes'][i]['points'][0][0] + json_content['shapes'][i]['points'][1][0])/2
                    point.append(score)
                    score = (json_content['shapes'][i]['points'][0][1]+json_content['shapes'][i]['points'][1][1])/2
                    point.append(score)
                    json_content['shapes'][i]['points'] = [point]
        
    ### 保存修改后的json文件，和复制jpg文件到指定目录
    with open('{}'.format(os.path.join(end_path,json_name)), 'w') as fw:
        json.dump(json_content, fw, indent=4)
        start_copy_img_path = os.path.join(start_path, jpg_name)
        end_copy_img_path = os.path.join(end_path, jpg_name)
        shutil.copy(start_copy_img_path,end_copy_img_path)

print('done!')



