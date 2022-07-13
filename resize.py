# failed number
# [913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931]

import cv2
import os
import cherry

# リサイズ元ディレクトリ
open_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\original\\"

# 出力先ディレクトリ
output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025\\"

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


# ディレクトリ内のファイル名を取得
open_files = os.listdir(open_dir)
already_files = os.listdir(output_dir)

# ディレクトリ内の画像のシリアル番号リストを取得
open_serial_num = get_serial_nums(open_files)
already_serial_num = get_serial_nums(already_files)

# 出力先に存在しない画像のみリサイズして保存
for num in open_serial_num:

    if num in already_serial_num:
        continue

    try:

        cherry_01 = cherry.cherry(num, picture_dir=open_dir, rotate=False)
        
        for dir in cherry_01.pictures:
            cherry_01.pictures[dir].resize(1/5)
            cv2.imwrite(output_dir + cherry_01.file_name + "_" + dir + ".jpeg", cherry_01.pictures[dir].resize_img)
        
        print(str(num) + "done")
    
    except:
        failed_num.append(num)
        print(str(num) + "faild")


print("------------------------------")
print("Processing completed")
print("")
print("failed number")
print(failed_num)
print("------------------------------")
    