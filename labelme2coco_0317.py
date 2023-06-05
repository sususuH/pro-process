# step0

import os
import json
import shutil

import numpy as np
import glob
from sklearn.model_selection import train_test_split
import mediapipe as mp
import cv2

np.random.seed(41)

classname_to_id = {"Player": 1}

# labels = ["Chin",  # 1
#         "LShoulder",  # 2
#         "RShoulder",  # 3
#         "LElbow",  # 4
#         "RElbow",  # 5
#         "LWristUp",  # 6
#         "LWristDown",  # 7
#         "RWristUp",  # 8
#         "RWristDown",  # 9
#         "LHand",  # 10
#         "RHand",  # 11
#         "RacketEndUp",  # 12
#         "RacketMUp",  # 13
#         "RacketHead",  # 14
#         "RacketMDown",  # 15
#         "RacketEndDown",  # 16
#         "LHip",  # 17
#         "RHip",  # 18
#         "LKnee",  # 19
#         "RKnee",  # 20
#         "LTiptoe",  # 21
#         "RTiptoe"]  # 22

# labels = ["Chin",  # 1
#         "Lshoulder",  # 2
#         "Rshoulder",  # 3
#         "Lelbow",  # 4
#         "Relbow",  # 5
#         "Lwristup",  # 6
#         "Lwristdown",  # 7
#         "Rwristup",  # 8
#         "Rwristdown",  # 9
#         "Lhand",  # 10
#         "Rhand",  # 11
#         "Racketendup",  # 12
#         "Racketmup",  # 13
#         "Rackethead",  # 14
#         "Racketmdown",  # 15
#         "Racketenddown",  # 16
#         "Lhip",  # 17
#         "Rhip",  # 18
#         "Lknee",  # 19
#         "Rknee",  # 20
#         "Ltiptoe",  # 21
#         "Rtiptoe"]  # 22

# 首先提取拍子的5个关键点
# labels = [
#     'nose',
#     'left_eye',
#     'right_eye',
#     'left_ear',
#     'right_ear',
#     'left_shoulder',
#     'right_shoulder',
#     'left_elbow',
#     'right_elbow',
#     'left_wrist',
#     'right_wrist',
#     'left_hip',
#     'right_hip',
#     'left_knee',
#     'right_knee',
#     'left_ankle',
#     'right_ankle',
#     "Racketendup",  # 17
#     "Racketmup",  # 18
#     "Rackethead",  # 19
#     "Racketmdown",  # 20
#     "Racketenddown",  # 21
# ]

# labels = [
#     "Racketendup",  # 0
#     "Racketmup",  # 1
#     "Rackethead",  # 2
#     "Racketmdown",  # 3
#     "Racketenddown",  # 4
# ]

# labels = [
#     "Rackethead",  # 0
#     "Racketbottom",  # 1
# ]

labels = [
    "RacketTop",  
    "RacketT",  
    "RacketFrontCover",
]

class Lableme2CoCo:
    def __init__(self):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0

    def save_coco_json(self, instance, save_path):
        json.dump(instance, open(save_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    def to_coco(self, json_path_list):
        self._init_categories()
        instance = {}
        instance['info'] = {'description': 'COCO 2017 Dataset ',
                            'version': 1.0,
                            'year': 2022,
                            'contributor': "COCO",
                            'date_created': "2022/07/05"}
        instance['license'] = ['COCO']
        instance['images'] = self.images
        instance['categories'] = self.categories

        for json_path in (json_path_list):
            print("--------->", json_path)
            obj = self.read_jsonfile(json_path)
            self.images.append(self._image(obj, json_path))
            shapes = obj['shapes']

            # check number of people in the image
            num_player = 0
            isIndividual = False
            for shape in shapes:
                if shape['group_id'] == None:
                    isIndividual = True
                    continue
                if shape['group_id'] > num_player:
                    num_player = shape['group_id']

            print("Start annotate for img: ", json_path, "There are", num_player + 1, "player in total")
            # do annotation for each person
            for player in range(num_player + 1):
                print("Player", player + 1, "...")
                # start with person = 0, create annotation dict for each person
                person_annotation = []
                keypoints = [None] * 3  # change 24 --> 22 --> 5 -> 3(for two points)

                part_index = 0
                for shape in shapes:
                    # iterate through keypoints, add to dict if belongs to person
                    # if shape['group_id'] != person and isIndividual == False:
                    #     continue
                    # get the body part this keypoint represents

                    # store the keypoint data to keypoints[] at its respective index
                    if shape['shape_type'] == "point":  # 去掉框的point
                        # keypoints[part_index] = shape['points'][0]
                        # part_index = part_index + 1

                        # ---------------------for tennis新增模块 7-6----------
                        # print(shape['shape_type'],11111)
                        if shape['label'] == labels[0]:
                            keypoints[0] = shape['points'][0]
                        elif shape['label'] == labels[1]:
                            keypoints[1] = shape['points'][0]
                        elif shape['label'] == labels[2]:
                            keypoints[2] = shape['points'][0]
                        # elif shape['label'] == labels[3]:
                        #     keypoints[3] = shape['points'][0]
                        # elif shape['label'] == labels[4]:
                        #     keypoints[4] = shape['points'][0]
                        # elif shape['label'] == labels[5]:
                        #     keypoints[5] = shape['points'][0]
                        # elif shape['label'] == labels[6]:
                        #     keypoints[6] = shape['points'][0]
                        # elif shape['label'] == labels[7]:
                        #     keypoints[7] = shape['points'][0]
                        # elif shape['label'] == labels[8]:
                        #     keypoints[8] = shape['points'][0]
                        # elif shape['label'] == labels[9]:
                        #     keypoints[9] = shape['points'][0]
                        # elif shape['label'] == labels[10]:
                        #     keypoints[10] = shape['points'][0]
                        # elif shape['label'] == labels[11]:
                        #     keypoints[11] = shape['points'][0]
                        # elif shape['label'] == labels[12]:
                        #     keypoints[12] = shape['points'][0]
                        # elif shape['label'] == labels[13]:
                        #     keypoints[13] = shape['points'][0]
                        # elif shape['label'] == labels[14]:
                        #     keypoints[14] = shape['points'][0]
                        # elif shape['label'] == labels[15]:
                        #     keypoints[15] = shape['points'][0]
                        # elif shape['label'] == labels[16]:
                        #     keypoints[16] = shape['points'][0]
                        # elif shape['label'] == labels[17]:
                        #     keypoints[17] = shape['points'][0]
                        # elif shape['label'] == labels[18]:
                        #     keypoints[18] = shape['points'][0]
                        # elif shape['label'] == labels[19]:
                        #     keypoints[19] = shape['points'][0]
                        # elif shape['label'] == labels[20]:
                        #     keypoints[20] = shape['points'][0]
                        # elif shape['label'] == labels[21]:
                        #     keypoints[21] = shape['points'][0]

                # edit the keypoint data to fit COCO annotation format
                # annotation in 7-6
                # num_keypoints = 0
                # for keypoint_i in range(22):
                #     # store keypoint for person in annotation
                #     if keypoints[keypoint_i] == None:
                #         person_annotation.extend([0, 0, 0])
                #     else:
                #         person_annotation.extend([keypoints[keypoint_i][0], keypoints[keypoint_i][1], 2])
                #         num_keypoints += 1

                        # annotate all other information for this person

                # ---------------------for tennis新增模块 7-6----------
                num_keypoints = 0
                for kep_i, kep_val in enumerate(keypoints):
                    if kep_val == None:
                        person_annotation.extend([0, 0, 0])
                    else:
                        person_annotation.extend([keypoints[kep_i][0], keypoints[kep_i][1], 2])
                        num_keypoints += 1
                print(person_annotation)


                annotation = {}
                annotation['id'] = self.ann_id
                annotation['image_id'] = self.img_id
                annotation['category_id'] = 1
                annotation['iscrowd'] = 0
                annotation['num_keypoints'] = num_keypoints
                annotation['keypoints'] = person_annotation

                # todo: for annotation["bbox"] detect bbx by using mediapipe and use it as label------
                tennis_label = ("Racketendup", "Racketmup", "Rackethead", "Racketmdown",
                                "Racketenddown")
                new_minx = 100000000000
                new_miny = 100000000000
                new_maxx = 0
                new_maxy = 0
                new_width = 0
                new_height = 0

                # for shape in shapes:
                #     if shape["label"] in tennis_label:
                #         if shape['shape_type'] == 'point':
                #             if shape['points'][0][0] < new_minx:
                #                 new_minx = shape['points'][0][0]  # 最左边
                #             if shape['points'][0][1] < new_miny:
                #                 new_miny = shape['points'][0][1]  # 最上点
                #             if shape['points'][0][0] > new_maxx:
                #                 new_maxx = shape['points'][0][0]  # 最右
                #             if shape['points'][0][1] > new_maxy:
                #                 new_maxy = shape['points'][0][1]  # 最下
                # new_width = new_maxx - new_minx  # 切割的图片宽
                # new_height = new_maxy - new_miny

                for shape in shapes:
                    if shape["label"] == "Racket":
                        x1, y1 = shape["points"][0]
                        x2, y2 = shape["points"][1]

                my_width = x2 - x1
                my_height = y2 - y1
                annotation["bbox"] = [x1, y1, my_width, my_height]
                annotation["area"] = my_width * my_height
                # annotation['bbox'] = [new_minx, new_miny, new_width, new_height]
                # annotation['area'] = new_width * new_height

                # ---------------这里上面书写bbox逻辑------------------------------
                """
                mp_pose = mp.solutions.pose
                # For static images:
                with mp_pose.Pose(static_image_mode=True,
                                  model_complexity=1,
                                  enable_segmentation=True,
                                  min_detection_confidence=0.5) as pose:

                    image = cv2.imread(json_path.split('.json')[0] + '.' + obj['imagePath'].split('.')[-1])

                    image_height, image_width, _ = image.shape
                    # Convert the BGR image to RGB before processing.
                    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                    # -------------------------# 有些文件不能用移除代码---------------
                    # mask_img = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
                    if isinstance(results.segmentation_mask, type(None)):
                        print("REMOVE remove------->", json_path)
                        json_src_p = json_path
                        ppp = json_path.split(".")[0]
                        img_src_p = ppp + ".jpg"

                        dst_pp_dir = "/home/zranguai/Desktop/datasets/test/crop_807_temp"
                        rm_img = os.path.join(dst_pp_dir, os.path.basename(img_src_p))
                        rm_json = os.path.join(dst_pp_dir, os.path.basename(json_src_p))
                        shutil.move(json_src_p, rm_json)
                        shutil.move(img_src_p, rm_img)
                        continue
                    # ---------------------------------------------

                    # print(results.segmentation_mask)
                    mask_img = np.array(results.segmentation_mask, dtype=np.uint8) * 255

                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 100))  # 定义矩形结构元素

                    mask_img = cv2.morphologyEx(mask_img, cv2.MORPH_CLOSE, kernel, iterations=1)  # 闭运算1

                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))  # 定义矩形结构元素
                    mask_img = cv2.dilate(mask_img, kernel, iterations=3)
                    thresh = cv2.Canny(mask_img, 128, 256)
                    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cv2.drawContours(image, contours, -1, (0, 0, 255), 3)

                    # -----------------------移除错误文件---------------
                    # if isinstance(cv2.boundingRect(contours[0]), type(IndexError)):
                    try:
                        x, y, w, h = cv2.boundingRect(contours[0])
                    except IndexError:
                        print("IndexError remove------->", json_path)
                        json_src_p = json_path
                        ppp = json_path.split(".")[0]
                        img_src_p = ppp + ".jpg"

                        dst_pp_dir = "/home/zranguai/Desktop/datasets/test/crop_807_temp"
                        rm_img = os.path.join(dst_pp_dir, os.path.basename(img_src_p))
                        rm_json = os.path.join(dst_pp_dir, os.path.basename(json_src_p))
                        shutil.move(json_src_p, rm_json)
                        shutil.move(img_src_p, rm_img)
                        continue
                    # ----------------------------------------

                    # x, y, w, h = cv2.boundingRect(contours[0])
                """

                # annotation['bbox'] = [x, y, w, h ]
                #
                # # add person annotation to image annotation
                # # print("Annotated data: ", annotation)
                # annotation['area'] = w*h

                self.annotations.append(annotation)
                self.ann_id += 1

            # next image
            self.img_id += 1

        # store to output .json instance
        instance['annotations'] = self.annotations
        return instance

    def _init_categories(self):
        for k, v in classname_to_id.items():
            category = {}
            category['supercategory'] = k
            category['id'] = v
            category['name'] = k
            # category['keypoints'] = ["Chin",  # 1
            #                          "Lshoulder",  # 2
            #                          "Rshoulder",  # 3
            #                          "Lelbow",  # 4
            #                          "Relbow",  # 5
            #                          "Lwristup",  # 6
            #                          "Lwristdown",  # 7
            #                          "Rwristup",  # 8
            #                          "Rwristdown",  # 9
            #                          "Lhand",  # 10
            #                          "Rhand",  # 11
            #                          "Racketendup",  # 12
            #                          "Racketmup",  # 13
            #                          "Rackethead",  # 14
            #                          "Racketmdown",  # 15
            #                          "Racketenddown",  # 16
            #                          "Lhip",  # 17
            #                          "Rhip",  # 18
            #                          "Lknee",  # 19
            #                          "Rknee",  # 20
            #                          "Ltiptoe",  # 21
            #                          "Rtiptoe"]
            # category['keypoints'] = ['nose',
            #                             'left_eye',
            #                             'right_eye',
            #                             'left_ear',
            #                             'right_ear',
            #                             'left_shoulder',
            #                             'right_shoulder',
            #                             'left_elbow',
            #                             'right_elbow',
            #                             'left_wrist',
            #                             'right_wrist',
            #                             'left_hip',
            #                             'right_hip',
            #                             'left_knee',
            #                             'right_knee',
            #                             'left_ankle',
            #                             'right_ankle',
            #                             "Racketendup",  # 17
            #                             "Racketmup",  # 18
            #                             "Rackethead",  # 19
            #                             "Racketmdown",  # 20
            #                             "Racketenddown",  # 21
            #                         ]

            # category['keypoints'] = [
            #                          "Racketendup",  # 17
            #                          "Racketmup",  # 18
            #                          "Rackethead",  # 19
            #                          "Racketmdown",  # 20
            #                          "Racketenddown",  # 21
            #                          ]

            # category['keypoints'] = [
            #     "Rackethead",  # 17
            #     "Racketbottom",  # 18
            # ]

            category['keypoints'] = [
                "RacketTop",  
                "RacketT",  
                "RacketFrontCover",
            ]

            # category['skeleton'] = [
            #                         [0,17],
            #                         [17,19],
            #                         [19,21],
            #                         [0,16],
            #                         [16,18],
            #                         [18,20],
            #                         [0,1],
            #                         [1,3],
            #                         [3,5],
            #                         [3.6],
            #                         [5,9],
            #                         [0,2],
            #                         [2,4],
            #                         [4,7],
            #                         [4,8],
            #                         [7,10],
            #                         [10,11],
            #                         [11,12],
            #                         [12,13],
            #                         [13,14],
            #                         [14,15],
            #                         [15,11]
            # ]


            # category['skeleton'] = [
            #     [16, 14],
            #     [14, 12],
            #     [17, 15],
            #     [15, 13],
            #     [12, 13],
            #     [6, 12],
            #     [7, 13],
            #     [6, 7],
            #     [6, 8],
            #     [7, 9],
            #     [8, 10],
            #     [9, 11],
            #     [2, 3],
            #     [1, 2],
            #     [1, 3],
            #     [2, 4],
            #     [3, 5],
            #     [4, 6],
            #     [5, 7],
            #     [11, 18],
            #     [11, 22],
            #     [18, 19],
            #     [19, 20],
            #     [20, 21],
            #     [21, 22]
            # ]

            category["skeleton"] = [
                [1, 2],
                [2, 3],
                # [3, 4],
                # [4, 5],
                # [5, 1]
            ]

            self.categories.append(category)

    def _image(self, obj, path):
        image = {}
        # img_x = utils.img_b64_to_arr(obj['imageData'])
        # image["height"] = img_x.shape[0]
        # image["width"] = img_x.shape[1]
        image["height"] = obj['imageHeight']
        image["width"] = obj['imageWidth']
        image['id'] = self.img_id
        image['file_name'] = os.path.basename(path).replace(".json", ".jpg")
        return image

    # read json file, return json object
    def read_jsonfile(self, path):
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)


if __name__ == '__main__':
    print("---------------------------------")
    train = Lableme2CoCo()
    val = Lableme2CoCo()

    # name of the folders containing labelme format json files
    #folders = ["Newbox", "CSB", "CSN", "CMB",
    #           "SMN", "SSB", "SSN", "SMB"]
    # folders = ["Newbox"]
    # folders = ["Threebox"]
    # folders = ["cro_tennis_816"]
    folders = ["cropimg"]
    # loop through the directories and start converting
    for folder in folders:
        print("Saving in ", folder)

        # set the paths
        json_path = os.path.join("/home/su/su/hrnet/pre-process/test/" + folder)  # path to labelme json folder
        json_list_path = glob.glob(json_path + "/*.json")  # labelme json files in folder
        train_path, val_path = train_test_split(json_list_path, test_size=0.1)  # 比例0.2 -> 0.1 split to train and test data set
        train_save_path = "/home/su/su/hrnet/pre-process/test/cropimg_json/annotations/person_keypoints_train2017.json"  # path to save COCO json files (train)
        val_save_path = "/home/su/su/hrnet/pre-process/test/cropimg_json/annotations/person_keypoints_val2017.json"  # path to save COCO json files (validation)

        # convert to COCO format
        train_instance = train.to_coco(train_path)
        val_instance = val.to_coco(val_path)

        # save the converted COCO json files
        # json.dump(train_instance, open(train_save_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        # json.dump(val_instance, open(val_save_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


        # # 拷贝图片
        save_coco_path = "/home/su/su/hrnet/pre-process/test/cropimg_json"  # 保存coco图片路径
        # for file in train_path:
        #     shutil.copy(file.replace("json", "jpg"), os.path.join(save_coco_path, "images", "train2017"))

        # for file in val_path:
        #     shutil.copy(file.replace("json", "jpg"), os.path.join(save_coco_path, "images", "val2017"))
