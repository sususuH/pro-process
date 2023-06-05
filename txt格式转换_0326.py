import os

str1 = 'val'
path = f'/home/su/su/yolo/yolov8_tracking-master/runs/detect/dataset_train_racket0.85/merger/coco_0.85/labels/{str1}'
datanames = os.listdir(path)
for dir in datanames:
    path2 = path + '/' + dir
    path1 = f'/home/su/su/yolo/yolov8_tracking-master/runs/detect/dataset_train_racket0.85/merger/coco_0.85/M/{str1}/' + dir
    with open(path1,'w',encoding ='utf - 8') as file:
        with open(path2,'r',encoding ='utf - 8') as infile:
            for line in infile:
                data_line =  line.strip("\n").split(',')
                data = []
                # print(data_line,111)
                for num in range(len(data_line)):
                    data_line[num] =data_line[num]
                    # print(data_line[num])
                    data.append(data_line[num])
                # print(data[0])
                data = data[0].split(' ')
                data[0] = 2
                # if len(data) > 2:
                data2 = str(data[0]) + ' ' + str(data[1]) + ' ' + str(data[2]) + ' ' + str(data[3]) + ' ' + str(data[4]) + "\n"
                # print(data2)
                # else:
                #     data2 = str(data[0]) + "\n"
                file.write(data2)

            