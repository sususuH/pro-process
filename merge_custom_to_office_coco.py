# time: 7-21
# author: zrg
# step2: 将得到val2017_office_coco  train2017_office_coco与自己数据集合并
"""
将处理好的网球拍关键点信息和处理好coco(coco_addqi1)的person类融入为最终的人体网球拍(coco_qi
)关键点信息

1. info里面信息不要变
2. licenses里面信息不变
3. categories里面信息保存不变

# 测试coco的image_id最大为多少
# val: 最大图片id为 581781
# train: 最大图片id为 581929

4. images里面的信息
    1. 为了防止和coco_office官方的images_id重复，我们的id都加上base_id = 900000
    2. 将我们自己的images都extends到官方的coco json images里面去

5. annotations
    1. 将里面的id都加上900000， 里面的image_id也都加上900000
    2. 将我们的annotations都extends到官方的annotations里面去
"""

import json

# for test_code
# src_file_add_coco = "/home/zranguai/Desktop/datasets/test/coco_addqi2/add_information_to_office_coco.json"
# src_file_custom_custom = "/home/zranguai/Desktop/datasets/test/coco_addqi2/val_Threebox.json"
# dst_office_json = "/home/zranguai/Desktop/datasets/test/coco_addqi2/val_final.json"

# val
# src_file_add_coco = "/home/su/su/hrnet/pre-process/test/coco/annotations/val2017.json"  # coco
# src_file_custom_custom = "/home/su/su/hrnet/pre-process/test/cropimg_json/annotations/val_0320.json"  # custom
# dst_office_json = "/home/su/su/hrnet/pre-process/test/coco_0320/annotations/val2017_final.json"

# train
src_file_add_coco = "/home/su/su/hrnet/pre-process/test/coco/annotations/train2017.json"  # coco
src_file_custom_custom = "/home/su/su/hrnet/pre-process/test/cropimg_json/annotations/train_0320.json"  # custom
dst_office_json = "/home/su/su/hrnet/pre-process/test/coco_0320/annotations/train2017_final.json"

f1 = open(src_file_add_coco, mode="r", encoding="utf-8")  # coco
f2 = open(src_file_custom_custom, mode="r", encoding="utf-8")  # custom

j_f1 = json.loads(f1.read())  # coco
j_f2 = json.loads(f2.read())  # custom

# 将f1不变的结果先保存到f3
newj_f3 = {}
newj_f3["info"] = j_f1["info"]
newj_f3["license"] = j_f1["license"]
newj_f3["categories"] = j_f1["categories"]

# 读取custom数据集images进行id改造
base_id = 20000
for img in j_f2["images"]:
    img["id"] = img["id"] + base_id

# 读取custom数据集annotations进行id, image_id改造
for anno in j_f2["annotations"]:
    anno["id"] = anno["id"] + base_id
    anno["image_id"] = anno["image_id"] + base_id

# 将custom的images和annotations 加到coco中去
j_f1["images"].extend(j_f2["images"])
j_f1["annotations"].extend(j_f2["annotations"])

# 将结果存到newj_f3中
newj_f3["images"] = j_f1["images"]
newj_f3["annotations"] = j_f1["annotations"]

# 写进文件
with open(dst_office_json, mode='w', encoding='utf-8') as out:
    out.write(json.dumps(newj_f3, ensure_ascii=False))

f1.close()
f2.close()

print("all done")

