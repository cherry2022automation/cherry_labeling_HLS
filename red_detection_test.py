from numpy import true_divide
import cherry
import cv2

from picture import picture


pic_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640_padding\\"


hsv_1_min = [0, 80, 10]
hsv_1_max = [30, 255, 255]
hsv_2_min = [160, 80, 10]
hsv_2_max = [179, 255, 255]

area_filter_min = 20000
area_filter_max = 250000

trim_size = 600


# 画像表示用関数
# リサイズして表示
def print_picture(window_name, picture):
        
        magnification = 0.75
        img = cv2.resize(picture, dsize=None, fx=magnification, fy=magnification)
        cv2.imshow(window_name, img)
        # cv2.waitKey(0)

# 画像の読み込み、表示テスト
if __name__ == "__main__":

    for i in range(1, 1500):

        cherry_01 = cherry.cherry(i, picture_dir=pic_dir)
        if cherry_01.enable == False:
            continue

        cherry_01.open_picture()

        # データ表示
        cherry_01.print_data()

        # 元画像表示
        cherry_01.combine(["original"])
        print_picture("original", cherry_01.original_combine)

        # マスク画像
        cherry_01.cherry_detection(hsv_1_min=hsv_1_min, hsv_1_max=hsv_1_max, hsv_2_min=hsv_2_min, hsv_2_max=hsv_2_max, area_filter_min=area_filter_min, area_filter_max=area_filter_max)
        cherry_01.combine(["red_masked_img", "red_monochrome_img", "detection_img", "cherry_masked_img", "cherry_monochrome_img"])
        print_picture("red masked image", cherry_01.red_masked_img_combine)
        print_picture("red monochrome", cherry_01.red_monochrome_img_combine)
        print_picture("detection", cherry_01.detection_img_combine)
        print_picture("cherry masked img", cherry_01.cherry_masked_img_combine)
        print_picture("cherry monochrome inversion img", cherry_01.cherry_monochrome_img_combine)

        # トリミング
        cherry_01.trimming(trim_size)
        cherry_01.combine("trimming_img")
        print_picture("trimming", cherry_01.trimming_img_combine)

        # 白飛び補正
        cherry_01.saturation_padding()
        cherry_01.combine(["detect_saturation_img", "saturation_padding_img"])
        print_picture("detect saturation img", cherry_01.detect_saturation_img_combine)
        print_picture("saturation padding img combine", cherry_01.saturation_padding_img_combine)

        # cherry_01.smoothing(10)
        # cherry_01.combine(["smoothing_img"])
        # print_picture("smoothing img combine", cherry_01.smoothing_img_combine)

        cherry_01.draw_hist(img=cherry_01.original_combine, mask_img=cherry_01.cherry_monochrome_img_combine, percent=True, mooving_ave_size_HLS=[0,4,3])
        
        cv2.waitKey(0)