# さくらんぼの検出サイズを表示
# トリミング画像サイズ検討用

# T19JM042 長谷季樹

# 2022/06/29    作成

# 2022/06/29 結果(1h10m)
#   width_max=2982, height_max=2538
#   width_max_num=783, height_max_num=298
#   detecthion miss = 3

import cherry
import picture
import cv2

width_max = 0
height_max = 0
width_max_num = None
height_max_num = None
detection_miss = []

# 画像表示用関数
# リサイズして表示
def print_picture(window_name, picture):
        
        magnification = 0.125
        img = cv2.resize(picture, dsize=None, fx=magnification, fy=magnification)
        cv2.imshow(window_name, img)
        # cv2.waitKey(0)

for i in range(1, 812):

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
    except:
        detection_miss.append(i)
        continue

    for dir in cherry_01.pictures:

        # 幅, 高さ取得
        width = cherry_01.pictures[dir].width
        height = cherry_01.pictures[dir].height

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