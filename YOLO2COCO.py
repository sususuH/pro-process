# coding=GBK
import os
import json
import cv2
import random
import time
from PIL import Image

coco_format_save_path='D:\\Code\\SF2023\\smoke-fire\\val\\'   #Ҫ���ɵı�׼coco��ʽ��ǩ�����ļ���
yolo_format_classes_path='D:\\Code\\SF2023\\smoke-fire\\names.txt'     #����ļ���һ��һ����
yolo_format_annotation_path='D:\\Code\\SF2023\\smoke-fire\\labels\\val\\'  #yolo��ʽ��ǩ�����ļ���
img_pathDir='D:\\Code\\SF2023\\smoke-fire\\images\\val\\'    #ͼƬ�����ļ���

with open(yolo_format_classes_path,'r') as fr:                               #�򿪲���ȡ����ļ�
    lines1=fr.readlines()
# print(lines1)
categories=[]                                                                 #�洢�����б�
for j,label in enumerate(lines1):
    label=label.strip()
    categories.append({'id':j+1,'name':label,'supercategory':'None'})         #�������Ϣ��ӵ�categories��
# print(categories)

write_json_context=dict()                                                      #д��.json�ļ��Ĵ��ֵ�
write_json_context['info']= {'description': '', 'url': '', 'version': '', 'year': 2022, 'contributor': '����ss', 'date_created': '2022-07-8'}
write_json_context['licenses']=[{'id':1,'name':None,'url':None}]
write_json_context['categories']=categories
write_json_context['images']=[]
write_json_context['annotations']=[]

#�������Ĵ�����Ҫ���'images'��'annotations'��keyֵ
imageFileList=os.listdir(img_pathDir)                                           #�������ļ����µ������ļ������������ļ�����ӵ��б���
for i,imageFile in enumerate(imageFileList):
    imagePath = os.path.join(img_pathDir,imageFile)                             #��ȡͼƬ�ľ���·��
    image = Image.open(imagePath)                                               #��ȡͼƬ��Ȼ���ȡͼƬ�Ŀ�͸�
    W, H = image.size

    img_context={}                                                              #ʹ��һ���ֵ�洢��ͼƬ��Ϣ
    #img_name=os.path.basename(imagePath)                                       #����path�����ļ��������path��/��\��β����ô�ͻ᷵�ؿ�ֵ
    img_context['file_name']=imageFile
    img_context['height']=H
    img_context['width']=W
    img_context['date_captured']='2022-07-8'
    img_context['id']=i                                                         #��ͼƬ��id
    img_context['license']=1
    img_context['color_url']=''
    img_context['flickr_url']=''
    write_json_context['images'].append(img_context)                            #����ͼƬ��Ϣ��ӵ�'image'�б���


    txtFile=imageFile[:6]+'.txt'                                            #��ȡ��ͼƬ��ȡ��txt�ļ�
    with open(os.path.join(yolo_format_annotation_path,txtFile),'r') as fr:
        lines=fr.readlines()                                                   #��ȡtxt�ļ���ÿһ�����ݣ�lines2��һ���б�������һ��ͼƬ�����б�ע��Ϣ
    for j,line in enumerate(lines):

        bbox_dict = {}                                                          #��ÿһ��bounding box��Ϣ�洢�ڸ��ֵ���
        # line = line.strip().split()
        # print(line.strip().split(' '))

        class_id,x,y,w,h=line.strip().split(' ')                                          #��ȡÿһ����ע�����ϸ��Ϣ
        class_id,x, y, w, h = int(class_id), float(x), float(y), float(w), float(h)       #���ַ�������תΪ�ɼ����int��float����

        xmin=(x-w/2)*W                                                                    #����ת��
        ymin=(y-h/2)*H
        xmax=(x+w/2)*W
        ymax=(y+h/2)*H
        w=w*W
        h=h*H

        bbox_dict['id']=i*10000+j                                                         #bounding box��������Ϣ
        bbox_dict['image_id']=i
        bbox_dict['category_id']=class_id+1                                               #ע��Ŀ�����Ҫ��һ
        bbox_dict['iscrowd']=0
        height,width=abs(ymax-ymin),abs(xmax-xmin)
        bbox_dict['area']=height*width
        bbox_dict['bbox']=[xmin,ymin,w,h]
        bbox_dict['segmentation']=[[xmin,ymin,xmax,ymin,xmax,ymax,xmin,ymax]]
        write_json_context['annotations'].append(bbox_dict)                               #��ÿһ�����ֵ�洢��bounding box��Ϣ��ӵ�'annotations'�б���

name = os.path.join(coco_format_save_path,"val"+ '.json')
with open(name,'w') as fw:                                                                #���ֵ���Ϣд��.json�ļ���
    json.dump(write_json_context,fw,indent=2)

# python main.py --img_path D:\Code\SF2023\smoke-fire\images\train  --mode YOLO2COCO --label_path D:\Code\SF2023\smoke-fire\labels\train  --save_path D:\Code\SF2023\smoke-fire