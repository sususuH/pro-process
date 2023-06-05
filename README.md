## 数据处理代码说明
1. step0:
labelme2coco.py: 转换拍子的数据集为总的json格式, 运行结束后会形成拍子的custom_train.json和custom_val.json
+ 注意事项
```
1. 注意更改line390后的路径
2. 注意有些图片或者json不行会报错将其移除文件夹
```
2. step1:
add_information_to_office_coco.py: 处理官方的数据集为我们使用的格式，形成处理好的总的
train_coco.json和val_coco.json
+ 注意事项
```
1. 注意更改line55后的路径， 改代码运行两次，分别处理官方的train_coco.json和val_coco.json
2. 运行train_coco.json/val_coco.json注意分别更改路径
```
3. step2: 
merge_custom_to_office_coco.py: 将我们的拍子数据集和coco的人的数据集融合在一起。同时也是运行两次分别产生总的train2017.json， val.json

4. step3：
将自定义的数据集下的image/train/*.jpg 拷贝到 总的image/train/
将自定义的数据集下的image/val/*.jpg 拷贝到 总的image/val/

5. 抽取官方代码
extra_coco.py: 从官方的coco中抽取我们需要的代码(也是运行两次)
+ 注意事项
```
1. 抽取的coco的json文件应该是step1处理好的train_coco.json和val_coco.json。
2. 同时注意抽取得到的图片数据集train/和val/替代step1下的train和val。后面的和自定义数据融合步骤一样
```

6. 裁剪代码

   crop_image.py: 裁剪图片并且处理json文件