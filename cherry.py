# サクランボオブジェクト
# サクランボの写真,品種,等級,測定値やそれに関する処理など

# T19JM042 長谷季樹

import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()  # opencvの読み込み画像サイズの上限を変更
import cv2
import numpy as np
import csv

import picture


class cherry():

    # サクランボデータのファイルパス
    cherry_picture_directory = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\original\\"
    cherry_data_pass = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\cherry_data.csv"

    # 有効/無効
    enable = False

    # サクランボ画像オブジェクト
    picture_T = None
    picture_B = None
    picture_L = None
    picture_R = None
    pictures = None

    # 結合画像
    original_combine = None
    red_masked_img_combine = None
    red_monochrome_img_combine = None
    detection_img_combine = None
    trimming_img_combine = None

    # サクランボのデータ
    num = None
    file_name = None
    variety = None
    grade = None
    weight = None
    polar_diameter = None
    equatorial_diameter = None
    sugar_content_B = None
    sugar_content_S = None

    # オブジェクト初期化関数
    # オブジェクト生成時に実行
    def __init__(self, serial_num, picture_dir=None):

        if picture_dir!=None:
            self.cherry_picture_directory = picture_dir

        self.get_data(serial_num)

    def trimming(self, size):
        for dir in self.pictures:
            self.pictures[dir].trimming(size)

    # サクランボ検出
    def cherry_detection(self, area_filter_min=None, area_filter_max=None, hsv_1_min=None, hsv_1_max=None, hsv_2_min=None, hsv_2_max=None):

        for dir in self.pictures:

            # パラメータ更新
            if area_filter_max != None:
                self.pictures[dir].area_filter_max = area_filter_max
            if area_filter_min != None:
                self.pictures[dir].area_filter_min = area_filter_min
            if hsv_1_min != None:
                self.pictures[dir].hsv_1_min = hsv_1_min
            if hsv_1_max != None:
                self.pictures[dir].hsv_1_max = hsv_1_max
            if hsv_2_min != None:
                self.pictures[dir].hsv_2_min = hsv_2_min
            if hsv_2_max != None:
                self.pictures[dir].hsv_2_max = hsv_2_max

            # 赤色以外をマスク
            self.pictures[dir].mask_red()

            # さくらんぼ検出
            self.pictures[dir].cherry_detection()
        
    # サクランボの写真とデータを読み込み
    # serial_num:サクランボのシリアルナンバー
    def get_data(self, serial_num):

        NUM                 = 0
        FILE_NAME           = 1
        VARIETY             = 2
        GRADE               = 3
        WEIGHT              = 4
        POLAR_DIAMETER      = 5
        EQUATORIAL_DIAMETER = 6
        SUGAR_CONTENT_B     = 7
        SUGAR_CONTENT_S     = 8

        # csvファイルからデータを取得
        with open(self.cherry_data_pass, encoding="utf-8") as d:
            reader = csv.reader(d)
            data = [row for row in  reader]

        # 取得データから該当データを格納
        line = serial_num
        self.num = data[line][NUM]
        self.file_name = data[line][FILE_NAME]
        self.variety = data[line][VARIETY]
        self.grade = data[line][GRADE]
        self.weight = data[line][WEIGHT]
        self.polar_diameter = data[line][POLAR_DIAMETER]
        self.equatorial_diameter = data[line][EQUATORIAL_DIAMETER]
        self.sugar_content_B = data[line][SUGAR_CONTENT_B]
        self.sugar_content_S = data[line][SUGAR_CONTENT_S]

        # 撮影成功した画像かを判定
        if self.weight != "":
            self.enable = True
        else:
            self.enable = False
            return

        # 数値に変換
        try:
            self.num = int(self.num)
            self.weight = float(self.weight)
            self.polar_diameter = float(self.polar_diameter)
            self.equatorial_diameter = float(self.equatorial_diameter)
            self.sugar_content_B = float(self.sugar_content_B)
            self.sugar_content_S = float(self.sugar_content_S)
        except:
            pass

    # 画像ファイルを読み込み,pictureオブジェクトに保存
    def open_picture(self, rotate=False):

        self.picture_T = picture.picture()
        self.picture_B = picture.picture()
        self.picture_L = picture.picture()
        self.picture_R = picture.picture()
        self.pictures = {"TOP":self.picture_T, "BUTTOM":self.picture_B, "LEFT":self.picture_L, "RIGHT":self.picture_R}

        # 画像読み込み
        try:
            
            file_name = self.file_name
            self.picture_T.original = cv2.imread("{}{}_TOP.jpeg".format(self.cherry_picture_directory, file_name))
            self.picture_B.original = cv2.imread("{}{}_BUTTOM.jpeg".format(self.cherry_picture_directory, file_name))
            self.picture_L.original = cv2.imread("{}{}_LEFT.jpeg".format(self.cherry_picture_directory, file_name))
            self.picture_R.original = cv2.imread("{}{}_RIGHT.jpeg".format(self.cherry_picture_directory, file_name))

            if rotate==True:
                self.picture_L.original = cv2.rotate(self.picture_L.original, cv2.ROTATE_90_CLOCKWISE)
                self.picture_R.original = cv2.rotate(self.picture_R.original, cv2.ROTATE_90_COUNTERCLOCKWISE)

        except:
            self.enable = False
            print("画像読み込みに失敗しました")

    # サクランボデータの表示(コンソール)
    def print_data(self):
        print("------------------------------------------------------------")
        print("シリアル番号 : {}".format(self.num))
        print("ファイル名　 : {}".format(self.file_name))
        print("有効/無効　　: {}".format(self.enable))
        print("品種　　　　 : {}".format(self.variety))
        print("等級　　　　 : {}".format(self.grade))
        print("重量　　　　 : {} [g]".format(self.weight))
        print("極径　　　　 : {} [mm]".format(self.polar_diameter))
        print("赤道径　　　 : {} [mm]".format(self.equatorial_diameter))
        print("糖度下　　　 : {}".format(self.sugar_content_B))
        print("糖度上　　　 : {}".format(self.sugar_content_S))
        print("------------------------------------------------------------")

    # 画像結合処理(選択式)
    def combine(self, Selection):

        if "original" in Selection:
            pictures = [self.picture_T.original, self.picture_B.original, self.picture_L.original, self.picture_R.original]
            self.original_combine = self.combine_4_picture(pictures)

        if "red_monochrome_img" in Selection:
            pictures = [self.picture_T.red_monochrome_img, self.picture_B.red_monochrome_img, self.picture_L.red_monochrome_img, self.picture_R.red_monochrome_img]
            self.red_monochrome_img_combine = self.combine_4_picture(pictures)

        if "red_masked_img" in Selection:
            pictures = [self.picture_T.red_masked_img, self.picture_B.red_masked_img, self.picture_L.red_masked_img, self.picture_R.red_masked_img]
            self.red_masked_img_combine = self.combine_4_picture(pictures)

        if "detection_img" in Selection:
            pictures = [self.picture_T.detection_img, self.picture_B.detection_img, self.picture_L.detection_img, self.picture_R.detection_img]
            self.detection_img_combine = self.combine_4_picture(pictures)

        if "cherry_monochrome_img" in Selection:
            pictures = [self.picture_T.cherry_monochrome_img, self.picture_B.cherry_monochrome_img, self.picture_L.cherry_monochrome_img, self.picture_R.cherry_monochrome_img]
            self.cherry_monochrome_img_combine = self.combine_4_picture(pictures)

        if "cherry_masked_img" in Selection:
            pictures = [self.picture_T.cherry_masked_img, self.picture_B.cherry_masked_img, self.picture_L.cherry_masked_img, self.picture_R.cherry_masked_img]
            self.cherry_masked_img_combine = self.combine_4_picture(pictures)

        if "trimming_img" in Selection:
            pictures = [self.picture_T.trim_img, self.picture_B.trim_img, self.picture_L.trim_img, self.picture_R.trim_img]
            self.trimming_img_combine = self.combine_4_picture(pictures)

    # 4つ並べた画像を生成
    def combine_4_picture(self, pictures):

        # 画像サイズ取得
        height_T, width_T, channnels = pictures[0].shape[:3]
        height_B, width_B, channnels = pictures[1].shape[:3]
        height_L, width_L, channnels = pictures[2].shape[:3]
        height_R, width_R, channnels = pictures[3].shape[:3]
        
        # 余白生成
        blank_TL_height = int( (height_T + height_B - height_L) / 2 )
        blank_TR_height = int( (height_T + height_B - height_R) / 2 )
        blank_L_width = int(width_L)
        blank_R_width = int(width_R)

        blank_BL_height = (height_T + height_B) - (blank_TL_height + height_L)
        blank_BR_height = (height_T + height_B) - (blank_TR_height + height_R)
            
        blank_TL = np.zeros((blank_TL_height, blank_L_width, 3)).astype('uint8')
        blank_TR = np.zeros((blank_TR_height, blank_R_width, 3)).astype('uint8')
        blank_BL = np.zeros((blank_BL_height, blank_L_width, 3)).astype('uint8')
        blank_BR = np.zeros((blank_BR_height, blank_R_width, 3)).astype('uint8')

        # 画像結合
        img_left = cv2.vconcat([blank_TL, pictures[2], blank_BL])
        img_right = cv2.vconcat([blank_TR, pictures[3], blank_BR])
        img_middle = cv2.vconcat([pictures[0], pictures[1]])
        combine_img = cv2.hconcat([img_left, img_middle, img_right])

        return combine_img



# 画像表示用関数
# リサイズして表示
def print_picture(window_name, picture):
        
        magnification = 0.125
        img = cv2.resize(picture, dsize=None, fx=magnification, fy=magnification)
        cv2.imshow(window_name, img)
        # cv2.waitKey(0)

# 画像の読み込み、表示テスト
if __name__ == "__main__":

    for i in range(1, 10):

        # データ取得
        cherry_01 = cherry(i)
        cherry_01.open_picture(rotate=True)

        if cherry_01.enable==False:
            continue

        # データ表示
        cherry_01.print_data()

        # 元画像表示
        cherry_01.combine(["original"])
        print_picture("original", cherry_01.original_combine)

        # さくらんぼ検出
        cherry_01.cherry_detection()

        # 検出結果表示
        cherry_01.combine(["red_masked_img", "red_monochrome_img", "detection_img", "cherry_masked_img"])
        print_picture("red masked", cherry_01.red_masked_img_combine)
        print_picture("red monochrome", cherry_01.red_monochrome_img_combine)
        print_picture("detection", cherry_01.detection_img_combine)
        print_picture("cherry masked img", cherry_01.cherry_masked_img_combine)

        # トリミング
        cherry_01.trimming(2500)

        # トリミング結果表示
        cherry_01.combine(["trimming_img"])
        print_picture("trimming", cherry_01.trimming_img_combine)
        
        cv2.waitKey(0)