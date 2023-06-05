import json
import numpy as np
import cv2
import base64
import os

data = []
img_json = [] 
nums = 0
# img_path = r'D:\dataset\SixExcKeypoints'
img_dir = "/home/su/su/labels_crop1-8/source_new_merger/select_source_total/select_source_val"       # 原图片路径

for img_name in os.listdir(img_dir):
    if img_name[-4:] == '.jpg':
    # img_cv = cv2.imread(img_name)
        data.append(img_name)
        str2 = img_name[:-4] + '.json'
    # if img_name[-5:] == '.json':
    # img_cv = cv2.imread(img_name)
        img_json.append(str2)
# print(data)
# print(img_json)

for i in range(len(data)):
    json_file = "{}".format(img_json[i])
    img_path = "{}".format(data[i])
    json_file = os.path.join(img_dir,json_file)
    img_path = os.path.join(img_dir, img_path)
    # dst_file = "./new_0.5/{}".format(img_json[i])
    dst_file = "/home/su/su/labels_crop1-8/source_new_merger/select_source_total/select_source_val_crop0.2/{}".format(img_json[i])      # 剪切后的json文件路径

    img = cv2.imread(img_path)
    print(img_path)
    # img1 = img
    with open(json_file, mode='r', encoding='utf-8') as f:
        j = json.loads(f.read())

        new_j = {}
        new_j['version'] = j['version']
        new_j['flags'] = j['flags']
        new_j['shapes'] = j['shapes']
        new_j['imagePath'] = j['imagePath']
        new_j['imageData'] = j['imageData']
        new_j['imageHeight'] = j['imageHeight']
        new_j['imageWidth'] = j['imageWidth']

        shapes = new_j['shapes']
        new_minx = 100000000000
        new_miny = 100000000000
        new_maxx = 0
        new_maxy = 0
        new_width = 0
        new_height = 0

        # 得到图片的宽高
        img_width = new_j['imageWidth']
        img_height = new_j['imageHeight']
        
        for shape in shapes:
            # if shape['shape_type'] == 'rectangle':
            #     continue
            # # 这里改改，找出最左边，最上点  和最右最下点
            # elif 
            # print(shape['label'])
            # if shape['shape_type'] == 'rectangle' and shape['label'] == 'Racket':
            #     if shape['points'][0][0] < new_minx:
            #         new_minx = shape['points'][0][0]  # 最左边
            #     if shape['points'][0][1] < new_miny:
            #         new_miny = shape['points'][0][1]  # 最上点
            #     if shape['points'][1][0] > new_maxx:
            #         new_maxx = shape['points'][1][0]  # 最右
            #     if shape['points'][1][1] > new_maxy:
            #         new_maxy = shape['points'][1][1]  # 最下

            ## 加入了在初始为右上和左下的情况下，找到最小的xy和最大的xy
            if shape['shape_type'] == 'rectangle' and shape['label'] == 'Racket':
                if shape['points'][0][0] < new_minx and shape['points'][0][0] < shape['points'][1][0]:
                    new_minx = shape['points'][0][0]  # 最左边
                else:
                    new_minx = shape['points'][1][0]  
                if shape['points'][0][1] < new_miny and shape['points'][0][1] < shape['points'][1][1]:
                    new_miny = shape['points'][0][1]  # 最上点
                else:
                    new_miny = shape['points'][1][1]
                if shape['points'][1][0] > new_maxx and shape['points'][0][0] < shape['points'][1][0]:
                    new_maxx = shape['points'][1][0]  # 最右
                else:
                    new_maxx = shape['points'][0][0]
                if shape['points'][1][1] > new_maxy and shape['points'][0][1] < shape['points'][1][1]:
                    new_maxy = shape['points'][1][1]  # 最下
                else:
                    new_maxy = shape['points'][0][1] 

        new_width = new_maxx - new_minx
        new_height = new_maxy - new_miny

        # print(new_minx,111)
        # print(new_miny,222)
        # print(new_maxx,333)
        # print(new_maxy,444)
        
        # 往四周扩5%
        # ratio = 0.05
        # 往四周扩30%
        # ratio = 0.3
        # 往四周扩30%
        ratio = 0.20
        new_minx = max(0, new_minx - new_width * ratio)
        new_miny = max(0, new_miny - new_height * ratio)
        new_maxx = max(0, new_maxx + new_width * ratio)
        new_maxy = max(0, new_maxy + new_height * ratio)

        new_minx = int(new_minx)
        new_miny = int(new_miny)
        new_maxx = int(new_maxx)
        new_maxy = int(new_maxy)

        # if new_maxx < new_minx:
        #     temp = new_maxx
        #     new_maxx = new_minx
        #     new_minx = temp
        # if new_maxy < new_miny:
        #     temp = new_maxy
        #     new_maxy = new_miny
        #     new_miny = temp

        # print(new_minx,111)
        # print(new_miny,222)
        # print(new_maxx,333)
        # print(new_maxy,444)        

        new_width = new_width * (1 + 2 * ratio)
        new_height = new_height * (1 + 2 * ratio)

        # 不能越界
        new_width = min(img_width, new_width)
        new_height = min(img_height, new_height)

        # x,y赋值回去
        label = []
        for shape in shapes:
            if shape['label'] == 'Racket':
                # print("----")
                # print(shape['points'][0][0],555)
                # print(shape['points'][0][1],666)
                # print(shape['points'][1][0],777)
                # print(shape['points'][1][1],888) 
                shape['points'][0][0] = shape['points'][0][0] - new_minx
                shape['points'][0][1] = shape['points'][0][1] - new_miny
                shape['points'][1][0] = shape['points'][1][0] - new_minx
                shape['points'][1][1] = shape['points'][1][1] - new_miny
                if shape['points'][0][0] > shape['points'][1][0]:
                    temp = shape['points'][1][0]
                    shape['points'][1][0] = shape['points'][0][0]
                    shape['points'][0][0] = temp
                if shape['points'][0][1] > shape['points'][1][1]:
                    temp = shape['points'][1][1]
                    shape['points'][1][1] = shape['points'][0][1]
                    shape['points'][0][1] = temp
                # print("----")
                # print(shape['points'][0][0],123)
                # print(shape['points'][0][1],456)
                # print(shape['points'][1][0],789)
                # print(shape['points'][1][1],000)
                # shape['points'][0] = [new_minx, new_miny]
                # shape['points'][1] = [new_maxx, new_maxy]
            # elif shape['points'][0][0] < shape['points'][1][0]:
            #     temp = shape['points'][0][0]
            #     shape['points'][0][0] = shape['points'][1][0]
            #     shape['points'][1][0] = temp
            #     shape['points'][0][0] = shape['points'][0][0] - 
            #     print("---")
            
            # if shape['label'] == 'Audience':
            #     shape['points'][0][0] = shape['points'][0][0] - new_minx
            #     shape['points'][0][1] = shape['points'][0][1] - new_miny
            #     shape['points'][1][0] = shape['points'][1][0] - new_minx
            #     shape['points'][1][1] = shape['points'][1][1] - new_miny
            label.append(shape['label'])
        if 'Person' in label:
            label.remove('Person')
        if 'Racket' in label:
            label.remove('Racket')
        if 'Tennis' in label:
            label.remove('Tennis')
        # print(label)

 

        
        for shape in shapes:
            if shape['label'] in label:  # 8-7 add by oyzk
                # print(shape['points'][0][0],shape['points'][0][1])

                shape['points'][0][0] = shape['points'][0][0] - new_minx
                shape['points'][0][1] = shape['points'][0][1] - new_miny

                # print(shape['points'][0][0],222)
                # print(shape['points'][0][1],333)

                # print(shape['points'][0][0],shape['points'][0][1])
        
        # print(new_minx,111)
        # print(new_miny,222)
        # print(new_maxx,333)
        # print(new_maxy,444)
        img_new = img[new_miny:new_maxy,new_minx:new_maxx]

        new_j['imageWidth'] = new_maxx - new_minx
        new_j['imageHeight'] = new_maxy - new_miny
        new_j['imagePath'] = img_path
        
        str1 =  '/home/su/su/labels_crop1-8/source_new_merger/select_source_total/select_source_val_crop0.2/{}'.format(data[i])     #  剪切后的图片路径
        # print(str1,111)
        # if str1 == './new/35_9.jpg' or str1 == './new/35_8.jpg' :
        #     print(new_minx,1)
        #     print(new_miny,2)
        #     print(new_maxx,3)
        #     print(new_maxy,4)
        #     print(img_new,3333)
        list1 = []
        for shape in shapes:
            list1.append(shape['label'])
        if 'Racket' not in list1:
            nums += 1
            # print(f'{img_path}  中没有网球拍')
            continue

        cv2.imwrite(str1, img_new)  
        # print(img_path,222)

        # 将图片转换成base64
        f = open(str1, 'rb')
        base64_encode = base64.b64encode(f.read()).decode('utf-8')
        new_j['imageData'] = base64_encode

        with open(dst_file, mode='w', encoding='utf-8') as out:
            out.write(json.dumps(new_j, ensure_ascii=False))
print(f"没有网球拍的图片共有：{nums} 张")
print("done")
