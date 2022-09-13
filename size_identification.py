# true 1319　　　false 520   5

from numpy import true_divide
import cherry
import cv2

from picture import picture


pic_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640_padding\\"
output_dir = "C:\\Users\\cherr\\Desktop\\data\\Program\\cherry_labeling_HLS\\size_data.csv"

hsv_1_min = [0, 80, 10]
hsv_1_max = [30, 255, 255]
hsv_2_min = [160, 80, 10]
hsv_2_max = [179, 255, 255]

area_filter_min = 20000
area_filter_max = 250000

trim_size = 600

magnification = []
true_num = 0
false_num = 0

def size_check(d):
    if d < 1.9:
        size = "S"
    elif d < 2.2:
        size = "M"
    elif d < 2.5:
        size = "L"
    elif d < 2.8:
        size = "LL"
    elif d < 3.1:
        size = "3L"
    else:
        size = "4L"
    return size

# 画像の読み込み、表示テスト
if __name__ == "__main__":

    g_max = 304 
    g_min = 354
    g_mid = int(g_min + (g_max-g_min)/2)

    output_text = "No.,d,g_y,d_pixel,\n"

    for i in range(1, 1932):

        cherry_01 = cherry.cherry(i, picture_dir=pic_dir)
        if cherry_01.enable == False:
            continue

        print("No. " + str(i))

        cherry_01.open_picture()

        # データ表示
        # cherry_01.print_data()

        # 元画像表示
        # cherry_01.combine(["original"])

        # マスク画像
        cherry_01.cherry_detection(hsv_1_min=hsv_1_min, hsv_1_max=hsv_1_max, hsv_2_min=hsv_2_min, hsv_2_max=hsv_2_max, area_filter_min=area_filter_min, area_filter_max=area_filter_max)

        found_diameter_pixel = cherry_01.picture_B.cherry_height
        if cherry_01.picture_B.cherry_width > found_diameter_pixel:
            found_diameter_pixel = cherry_01.picture_B.cherry_width

        found_diameter = found_diameter_pixel * 0.004661770252 + 0.15
        # if cherry_01.picture_R.cherry_g_y != g_mid:
        #     found_diameter = found_diameter * (cherry_01.picture_R.cherry_g_y - g_mid) * (-0.1101350849)
        found_diameter = found_diameter_pixel * 0.0051

        found_diameter = found_diameter * (cherry_01.picture_R.cherry_g_y/(g_min+(g_max-g_min)/2))

        print(cherry_01.equatorial_diameter, found_diameter)

        # output_text += str(cherry_01.num) + "," + str(cherry_01.equatorial_diameter) + "," + str(cherry_01.picture_R.cherry_g_y) + "," + str(found_diameter_pixel) + ",\n"

        if size_check(cherry_01.equatorial_diameter) == size_check(found_diameter):
            true_num += 1
        else:
            false_num += 1

        print("true " + str(true_num) + "　　　false " + str(false_num))

# with open(output_dir, 'w') as data:
#     data.write(output_text)