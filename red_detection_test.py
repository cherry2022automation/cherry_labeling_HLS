import cherry
import cv2

from picture import picture


pic_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025\\"


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

    for i in [923, 924, 1536, 1643, 1668]:

        cherry_01 = cherry.cherry(i, picture_dir=pic_dir)

        # データ表示
        cherry_01.print_data()

        # 元画像表示
        print_picture("all", cherry_01.original_combine)

        # マスク画像
        cherry_01.cherry_detection(hsv_1_min=hsv_1_min, hsv_1_max=hsv_1_max, hsv_2_min=hsv_2_min, hsv_2_max=hsv_2_max, area_filter_min=area_filter_min, area_filter_max=area_filter_max)
        print_picture("hsv masked image", cherry_01.masked_img_combine)
        print_picture("hsv monochrome", cherry_01.monochrome_img_combine)
        print_picture("detection", cherry_01.detection_img_combine)
        print_picture("cherry masked img", cherry_01.cherry_masked_img_combine)

        cherry_01.trimming(trim_size)
        print_picture("trimming", cherry_01.trimming_img_combine)
        
        cv2.waitKey(0)