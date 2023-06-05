# time: 7-24
# author: zrg
"""
从标准的coco数据集中抽取一定的数量和我们的进行混合训练

1. 读取json文件， 设置提取数量 extra_num
2. 首先读取images里面的 file_name 和 id, 作为一个key[id]=file_name。 append进去image_id_list里面(1000个)
3. 遍历image_id_list,将里面的图片移入到extract_image文件夹里面
4. 遍历image_id_list找出id, 遍历将annotations里面id相同的进行保存
"""

import os
import shutil
import json

# train # 从标准的coco train里面提取的图片coco的数量
# extra_num = 5000
#
# coco_img_dir = "/home/zranguai/Dataset/coco/train2017"  # coco图片的路径
# extract_img_dir = "/home/zranguai/Desktop/datasets/test/extra_coco/train2017"  # 提取图片目录
#
# src_json_file = "/home/zranguai/Dataset/coco/annotations/person_keypoints_train2017.json"  # 标准的json路径
# extra_json_file = "/home/zranguai/Desktop/datasets/test/extra_coco/annotations/train2017.json"  # 提取的json路径

# val # 从标准的coco val里面提取的图片coco的数量
extra_num = 500

coco_img_dir = "/home/zranguai/Dataset/coco/val2017"  # coco图片的路径
extract_img_dir = "/home/zranguai/Desktop/datasets/test/extra_coco/val2017"  # 提取图片目录

src_json_file = "/home/zranguai/Dataset/coco/annotations/person_keypoints_val2017.json"  # 标准的json路径
extra_json_file = "/home/zranguai/Desktop/datasets/test/extra_coco/annotations/val2017.json"  # 提取的json路径

f_src = open(src_json_file, mode="r", encoding="utf-8")
f_extra_json = open(extra_json_file, mode="w", encoding="utf-8")

j_src = json.loads(f_src.read())

j_extra = {}
# 这些是不变的信息
j_extra["info"] = j_src["info"]
j_extra["licenses"] = j_src["licenses"]
j_extra["categories"] = j_src["categories"]

# 遍历images
extra_image_list = []
for img_index, img in enumerate(j_src["images"]):
    if img_index > extra_num:
        break
    extra_image_list.append(img)

# 提取的images保存起来
j_extra["images"] = extra_image_list

# 遍历extra_image_list,找到file_name把图片拷贝到extract_image
for copy_file in extra_image_list:
    src_img_path = os.path.join(coco_img_dir, copy_file["file_name"])
    dst_img_path = os.path.join(extract_img_dir, copy_file["file_name"])
    shutil.copy(src_img_path, dst_img_path)
print("copy image done")

# 遍历extra_image_list,根据id找符合条件的annotations里面的值
extra_anno_list = []
for image_id in extra_image_list:
    img_id = image_id["id"]  # 找出img的id
    for anno in j_src["annotations"]:
        if anno["image_id"] == img_id:  # 找出anno的image_id(annotation数量都要大于img数量)
            extra_anno_list.append(anno)


# 将anno赋值回去
j_extra["annotations"] = extra_anno_list

f_src.close()

# 写入新的标注文件
f_extra_json.write(json.dumps(j_extra, ensure_ascii=False))

print("all done")
