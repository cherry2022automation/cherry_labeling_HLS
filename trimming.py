# failed number
# [44, 107, 149, 196, 232, 292, 321, 502, 513, 527, 553, 563, 564, 665, 750, 769, 890, 911, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 952, 959, 986, 1005, 1047, 1060, 1099, 1115, 1116, 1117, 1118, 1143, 1168, 1183, 1197, 1247, 1250, 1274, 1285, 1307, 1309, 1313, 1317, 1319, 1320, 1338, 1342, 1350, 1356]

import cv2
import os
import cherry

# 変更を行う変数 ========================================================================

# トリミング元ディレクトリ
open_dir = cherry.cherry.cherry_picture_directory

# 出力先ディレクトリ
output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\trimming_2500\\"

trm_size = 2500

hsv_1_min = [0, 80, 30]
hsv_1_max = [15, 255, 255]
hsv_2_min = [160, 80, 30]
hsv_2_max = [179, 255, 255]

area_filter_min = 1000000
area_filter_max = 3000000

# ======================================================================================

failed_num = []

# ディレクトリ内に存在する画像のシリアル番号をリスト化
def get_serial_nums(files):
    serial_nums = []
    for file in files:
        try:
            file_names = file.split("_", 1)
            num = int(file_names[0])
            if num in serial_nums:
                continue
            serial_nums.append(num)
        except:
            pass
    return serial_nums

def trim():

    print("========== trim start ==========")

    # ディレクトリ内のファイル名を取得
    open_files = os.listdir(open_dir)
    already_files = os.listdir(output_dir)

    # ディレクトリ内の画像のシリアル番号リストを取得
    open_serial_num = get_serial_nums(open_files)
    already_serial_num = get_serial_nums(already_files)

    # 出力先に存在しない画像のみトリミングして保存
    for num in open_serial_num:

        if num in already_serial_num:
            continue

        try:

            print("\rtry : {}".format(num), end='')

            cherry_01 = cherry.cherry(num, picture_dir=open_dir)

            if cherry_01.enable == False:
                continue

            # さくらんぼ検出
            cherry_01.cherry_detection(hsv_1_min=hsv_1_min, hsv_1_max=hsv_1_max, hsv_2_min=hsv_2_min, hsv_2_max=hsv_2_max, area_filter_min=area_filter_min, area_filter_max=area_filter_max)

            # トリミング
            cherry_01.trimming(trm_size)
            
            for dir in cherry_01.pictures:
                cv2.imwrite(output_dir + cherry_01.file_name + "_" + dir + ".jpeg", cherry_01.pictures[dir].trim_img)
            
            print("\r" + str(num) + "done")

        except:
            failed_num.append(num)
            print("\r" + str(num) + "failed")

    print("trim completed")
    print("")
    print("failed number")
    print(failed_num)
    print("")

    return failed_num
        
if __name__ == '__main__':

    trim()