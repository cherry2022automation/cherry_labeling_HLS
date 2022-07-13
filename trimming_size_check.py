# さくらんぼの検出サイズを表示
# トリミング画像サイズ検討用

# T19JM042 長谷季樹

# 2022/06/29    作成

# 2022/06/29 結果(1h10m)
#   width_max=2289, height_max=2422
#   width_max_num=786, height_max_num=566
#   detecthion miss = 3
#   [44, 527, 564]

import cherry
import picture
import cv2
import csv

output_csv_pass = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\detection_01\\cherry_size.csv"
output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\detection_01\\"

cherry_num = 1136

width_max = 0
height_max = 0
width_max_num = None
height_max_num = None
detection_miss = []

# リサイズ
def resize(picture):
        
        magnification = 0.125
        img = cv2.resize(picture, dsize=None, fx=magnification, fy=magnification)
        return img


with open(output_csv_pass, 'w') as f:
    writer = csv.writer(f)

    for i in range(1, cherry_num+1):

        cherry_01 = cherry.cherry(i)

        if cherry_01.enable == False:
            continue

        cherry_01.original_combine_en = False
        cherry_01.masked_img_combine_en = False
        cherry_01.monochrome_img_combine_en = False
        # cherry_01.detection_img_combine_en = False

        # さくらんぼ検出
        try:
            cherry_01.cherry_detection()
            cv2.imwrite(output_dir + cherry_01.file_name + "_detection.jpeg", resize(cherry_01.detection_img_combine))
        except:
            detection_miss.append(i)
            continue

        for dir in cherry_01.pictures:

            # 幅, 高さ取得
            width = cherry_01.pictures[dir].width
            height = cherry_01.pictures[dir].height

            output_line = [cherry_01.num, dir, width, height]
            writer.writerow(output_line)
            
            # 表示
            print("{} {} : width={} height={}".format(cherry_01.num, dir, width, height))

            # 最大値更新
            if width_max < width:
                width_max = width
                width_max_num = i
            if height_max < height:
                height_max = height
                height_max_num = i

# 最大値更新
print("width_max={}, height_max={}".format(width_max, height_max))
print("width_max_num={}, height_max_num={}".format(width_max_num, height_max_num))
print("detecthion miss = {}".format(len(detection_miss)))
print(detection_miss)