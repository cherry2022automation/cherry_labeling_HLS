import cv2
import os
import cherry

# 変更を行う変数 ========================================================================

# ラベル貼り元ディレクトリ
open_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640\\"

# 出力先ディレクトリ
output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640_label\\"

# 拡大率
magnification = 0.25
text_size = 12

# =====================================================================================

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


def put_label():

    print("========== put label start ==========")

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

            cherry_01 = cherry.cherry(num, picture_dir=open_dir)
            cherry_01.open_picture()
            
            for dir in cherry_01.pictures:
                img = cherry_01.pictures[dir].original
                cv2.putText(img,
                    text=str(cherry_01.num),
                    org=(0+20, 640-20),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=3.0,
                    color=(0, 0, 0),
                    thickness=8,
                    lineType=cv2.LINE_4)
                cv2.imwrite(output_dir + cherry_01.file_name + "_" + dir + ".jpeg", img)
            
            print(str(num) + "done")
        
        except:
            failed_num.append(num)
            print(str(num) + "faild")

    print("\rput label completed")
    print("")
    print("failed number")
    print(failed_num)
    print("")

    return failed_num
        
if __name__ == "__main__":
    put_label()