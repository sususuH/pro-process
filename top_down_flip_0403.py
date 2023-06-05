# 上下翻转代码
import cv2
import json
import os
import base64


src_img_json_dir = "/home/su/su/labels_crop1-8/source_new_merger/source_and_new0.2/new_total_crop0.20"
dst_img_json_dir = "/home/su/su/labels_crop1-8/source_new_merger/source_and_new0.2/new_total_crop0.20_flip"


def flip(src_img_detail_path, src_json_detail_path, dst_img_detail_path, dst_json_detail_path):
    # 图片以及标签进行上下翻转
    flip_code = 0  # 1:水平翻转 0：垂直翻转
    src_img = cv2.imread(src_img_detail_path)  # 读取图片

    f_src = open(src_json_detail_path, mode='r', encoding="utf-8")
    j = json.loads(f_src.read())

    new_j = {}
    new_j['version'] = j['version']
    new_j['flags'] = j['flags']
    new_j['shapes'] = j['shapes']  # 需要改变 --> 已经改变
    new_j['imagePath'] = dst_img_detail_path.split("/")[-1]  # 需要改变
    # new_j['imageData'] = j['imageData']  # 需要改变
    new_j['imageHeight'] = j['imageHeight']
    new_j['imageWidth'] = j['imageWidth']

    # 需要对5个点以及Racket框进行翻转
    h, w, _ = src_img.shape
    img_flip = cv2.flip(src_img, flipCode=flip_code)  # 图片翻转
    # base64_encode = base64.b64encode(img_flip.tobytes()).decode('utf-8')
    # new_j['imageData'] = base64_encode

    if flip_code == 0:
        for shape in new_j['shapes']:
            # if shape['shape_type'] == 'rectangle':
            #     point_0 = shape['points'][0]
            #     point_1 = shape['points'][1]

            #     shape['points'][0][1] = h - point_0[1]
            #     shape['points'][1][1] = h - point_1[1]
            if shape['shape_type'] == 'point':
                shape['points'][0][1] = h - shape['points'][0][1]

    # 写入图片和标签
    cv2.imwrite(dst_img_detail_path, img_flip)

    f=open(dst_img_detail_path, 'rb')
    base64_encode = base64.b64encode(f.read()).decode('utf-8')
    new_j['imageData'] = base64_encode

    with open(dst_json_detail_path, mode='w', encoding='utf-8') as out:
        out.write(json.dumps(new_j, ensure_ascii=False))


    # show_flip
    # for shape in new_j['shapes']:
    #     if shape['shape_type'] == 'point' and shape['label'] in ('Racketendup'):
    #         x = shape['points'][0][0]
    #         y = shape['points'][0][1]
    #         cv2.circle(img_flip, (int(x), int(y)), 1, (0, 0, 255), 3)
    #         cv2.putText(img_flip, f"{shape['label']}", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.1, (255, 255, 255), 2)

    # for shape in new_j['shapes']:
    #     if shape['shape_type'] == "rectangle":
    #         x1, y1 = shape['points'][0]
    #         x2, y2 = shape['points'][1]
    #         cv2.rectangle(img_flip, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 1)
    # cv2.imshow("flip_name", img_flip)
    # cv2.imwrite("result.jpg", img_flip)
    # cv2.waitKey(0)


def flop_top_down(src_img_dir_path, dst_img_dir_path):
    for img_path in os.listdir(src_img_dir_path):
        if img_path.split(".")[1] == "json":
            continue
        src_img_detail_path = os.path.join(src_img_dir_path, img_path)
        src_json_detail_path = src_img_detail_path.replace(".jpg", ".json")

        dst_img_detail_path = os.path.join(dst_img_dir_path, img_path.replace("Peo", "flipPeo"))
        dst_json_detail_path = dst_img_detail_path.replace(".jpg", ".json")

        # 翻转图片和json
        flip(src_img_detail_path, src_json_detail_path, dst_img_detail_path, dst_json_detail_path)


if __name__ == '__main__':
    flop_top_down(src_img_json_dir, dst_img_json_dir)
    print("all done")
