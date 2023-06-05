# time: 7-21
# author: zranguai
# step1: 得到val2017_office_coco  train2017_office_coco
"""
处理官方coco的json成为我们需要的格式
1. info里面信息不要变
2. licenses里面信息不变
3. images里面信息不变
4. (重点) annotations(list)里面信息
    1. 依次遍历annotations内部, 往keypoints(list)里面添加 5个 [0, 0, 0]
5. (次重点) categories下0
    1. keypoints(list),增加(or覆盖)5个
    {
    17: "Racketendup",  # 17
    18: "Racketmup",  # 18
    19: "Rackethead",  # 19
    20: "Racketmdown",  # 20
    21: "Racketenddown",  # 21
    }
    2. skeleton(list),增加(or覆盖)5个
                category['skeleton'] = [
                [16, 14],
                [14, 12],
                [17, 15],
                [15, 13],
                [12, 13],
                [6, 12],
                [7, 13],
                [6, 7],
                [6, 8],
                [7, 9],
                [8, 10],
                [9, 11],
                [2, 3],
                [1, 2],
                [1, 3],
                [2, 4],
                [3, 5],
                [4, 6],
                [5, 7],

                [11, 18],
                [11, 22],
                [18, 19],
                [19, 20],
                [20, 21],
                [21, 22]
            ]
"""


import json


# val
json_file = "/home/zranguai/Desktop/datasets/test/extra_coco/annotations_office/val2017.json"

dst_file = "/home/zranguai/Desktop/datasets/test/extra_coco/annotations/val2017.json"

# train
# json_file = "/home/zranguai/Desktop/datasets/test/extra_coco/annotations_office/train2017.json"
#
# dst_file = "/home/zranguai/Desktop/datasets/test/extra_coco/annotations/train2017.json"

with open(json_file, mode='r', encoding='utf-8') as f:
    j = json.loads(f.read())
    new_j = {}
    new_j['info'] = j['info']
    new_j['licenses'] = j['licenses']
    new_j['images'] = j['images']

    # new_j['annotations'] = j['annotations']
    # new_j['categories'] = j['categories']

    change_j = {}
    change_j["annotations"] = j['annotations']
    change_j["categories"] = j["categories"]

    # 改变annotations
    keypoints_add = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for anno in change_j["annotations"]:
        # 新增关键点, 一共22个
        anno["keypoints"].extend(keypoints_add)

    # 改变categofies
    keypoints_cate = [
                        'nose',
                        'left_eye',
                        'right_eye',
                        'left_ear',
                        'right_ear',
                        'left_shoulder',
                        'right_shoulder',
                        'left_elbow',
                        'right_elbow',
                        'left_wrist',
                        'right_wrist',
                        'left_hip',
                        'right_hip',
                        'left_knee',
                        'right_knee',
                        'left_ankle',
                        'right_ankle',
                        "Racketendup",  # 17
                        "Racketmup",  # 18
                        "Rackethead",  # 19
                        "Racketmdown",  # 20
                        "Racketenddown",  # 21
                    ]
    skeleton_cate = [
                        [16, 14],
                        [14, 12],
                        [17, 15],
                        [15, 13],
                        [12, 13],
                        [6, 12],
                        [7, 13],
                        [6, 7],
                        [6, 8],
                        [7, 9],
                        [8, 10],
                        [9, 11],
                        [2, 3],
                        [1, 2],
                        [1, 3],
                        [2, 4],
                        [3, 5],
                        [4, 6],
                        [5, 7],
                        [11, 18],
                        [11, 22],
                        [18, 19],
                        [19, 20],
                        [20, 21],
                        [21, 22]
                    ]
    change_j["categories"][0]["supercategory"] = "Player"
    change_j["categories"][0]["name"] = "Player"
    change_j["categories"][0]["keypoints"] = keypoints_cate
    change_j["categories"][0]["skeleton"] = skeleton_cate

    # 赋值回new_j
    new_j['annotations'] = change_j["annotations"]
    new_j['categories'] = change_j["categories"]

    # 写进文件中去
    with open(dst_file, mode='w', encoding='utf-8') as out:
        out.write(json.dumps(new_j, ensure_ascii=False))
print("all done")
