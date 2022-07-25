import cv2
import os
import cherry

# 変更を行う変数 ========================================================================

# パディング元ディレクトリ
open_dir = cherry.cherry.cherry_picture_directory

# 出力先ディレクトリ
output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\trimming_2500\\"

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

def padding():

    print("========== padding start ==========")

    # ディレクトリ内のファイル名を取得
    open_files = os.listdir(open_dir)
    already_files = os.listdir(output_dir)

    # ディレクトリ内の画像のシリアル番号リストを取得
    open_serial_num = get_serial_nums(open_files)
    already_serial_num = get_serial_nums(already_files)

    # 出力先に存在しない画像のみパディングして保存
    for num in open_serial_num:

        if num in already_serial_num:
            continue

        try:

            print("\rtry : {}".format(num), end='')

            cherry_01 = cherry.cherry(num, picture_dir=open_dir)

            if cherry_01.enable == False:
                continue

            cherry_01.open_picture()

            # さくらんぼ検出
            cherry_01.cherry_detection(hsv_1_min=hsv_1_min, hsv_1_max=hsv_1_max, hsv_2_min=hsv_2_min, hsv_2_max=hsv_2_max, area_filter_min=area_filter_min, area_filter_max=area_filter_max)

            # パディング
            cherry_01.saturation_padding()
            
            for dir in cherry_01.pictures:
                cv2.imwrite(output_dir + cherry_01.file_name + "_" + dir + ".jpeg", cherry_01.pictures[dir].saturation_padding_img)
            
            print("\r" + str(num) + "done")

        except:
            failed_num.append(num)
            print("\r" + str(num) + "failed")

    print("padding completed")
    print("")
    print("failed number")
    print(failed_num)
    print("")

    return failed_num
        
if __name__ == '__main__':

    padding()