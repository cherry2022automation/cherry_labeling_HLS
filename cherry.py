# サクランボオブジェクト
# サクランボの写真,品種,等級,測定値やそれに関する処理など

# T19JM042 長谷季樹

# 2022/06/24    画像読み込み処理追加
#               サクランボデータ,画像読み込み処理追加(エクセルデータ使用)
#               リサイズ表示追加
#               初期化関数追加
#               画像結合処理追加
# 2022/06/28    マスク処理(赤)追加
#               モノクロ生成処理追加
# 2022/06/29    pictureオブジェクト追加
#               没画像判定追加
#               さくらんぼ検出処理追加
#               画像結合をオプション化

from json import detect_encoding
import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()  # opencvの読み込み画像サイズの上限を変更
import cv2
import openpyxl
import numpy as np
import copy
import picture

class cherry():

    # サクランボデータのファイルパス
    cherry_picture_directory = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\original\\"
    cherry_data_pass = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\cherry_data.xlsx"

    cherry_data_sheet_name = "all numerical data"
    

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
    masked_img_combine = None
    monochrome_img_combine = None
    detection_img_combine = None
    trimming_img_combine = None

    # 画像結合有効/無効
    original_combine_en = True
    masked_img_combine_en = True
    monochrome_img_combine_en = True
    detection_img_combine_en = True
    trimming_img_combine_en = True

    # Excelシート内のデータ
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
    def __init__(self, serial_num, picture_dir=None, rotate=True):

        self.picture_T = picture.picture()
        self.picture_B = picture.picture()
        self.picture_L = picture.picture()
        self.picture_R = picture.picture()
        self.pictures = {"TOP":self.picture_T, "BUTTOM":self.picture_B, "LEFT":self.picture_L, "RIGHT":self.picture_R}

        if picture_dir!=None:
            self.cherry_picture_directory = picture_dir

        self.get_data(serial_num, rotate)

        if self.enable == True:

            if self.original_combine_en == True:
                pictures = [self.picture_T.original, self.picture_B.original, self.picture_L.original, self.picture_R.original]
                self.original_combine = self.combine(pictures)

    def trimming(self, size):
        for dir in self.pictures:
            self.pictures[dir].trimming(size)

        if self.trimming_img_combine_en == True:
            pictures = [self.picture_T.trim_img, self.picture_B.trim_img, self.picture_L.trim_img, self.picture_R.trim_img]
            self.trimming_img_combine = self.combine(pictures)

    # サクランボ検出
    def cherry_detection(self, area_filter_min=None, area_filter_max=None, hsv_1_min=None, hsv_1_max=None, hsv_2_min=None, hsv_2_max=None):

        self.mask_red()

        for dir in self.pictures:

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

            self.pictures[dir].cherry_detection()

        if self.detection_img_combine_en == True:
            pictures = [self.picture_T.detection_img, self.picture_B.detection_img, self.picture_L.detection_img, self.picture_R.detection_img]
            self.detection_img_combine = self.combine(pictures)

    # マスク処理 +結合画像生成
    def mask_red(self):

        for dir in self.pictures:
            self.pictures[dir].mask_red()

        # マスク画像を結合
        if self.masked_img_combine_en == True:
            pictures = [self.picture_T.masked_img, self.picture_B.masked_img, self.picture_L.masked_img, self.picture_R.masked_img]
            self.masked_img_combine = self.combine(pictures)

        # モノクロ画像結合
        if self.monochrome_img_combine_en == True:
            pictures = [self.picture_T.monochrome_img, self.picture_B.monochrome_img, self.picture_L.monochrome_img, self.picture_R.monochrome_img]
            self.monochrome_img_combine = self.combine(pictures)

    # サクランボの写真とデータを読み込み
    # serial_num:サクランボのシリアルナンバー
    def get_data(self, serial_num, rotate):

        line = str(serial_num + 1)

        # Excelファイル読み込み
        cherry_data_file = openpyxl.load_workbook(self.cherry_data_pass)
        sheet = cherry_data_file[self.cherry_data_sheet_name]

        self.num = sheet["A" + line].value
        self.file_name = sheet["B" + line].value
        self.variety = sheet["C" + line].value
        self.grade = sheet["D" + line].value
        self.weight = sheet["E" + line].value
        self.polar_diameter = sheet["F" + line].value
        self.equatorial_diameter = sheet["G" + line].value
        self.sugar_content_B = sheet["H" + line].value
        self.sugar_content_S = sheet["I" + line].value

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

        # 撮影成功した画像かを判定
        if self.weight != None:
            self.enable = True

            # 画像読み込み
            try:
                self.open_picture(self.file_name, rotate)
            except:
                self.enable = False
                print("画像読み込みに失敗しました")

    # 単一の画像ファイルを読み込み,pictureオブジェクトに保存
    def open_picture(self, file_name, rotate):

        self.picture_T.original = cv2.imread("{}{}_TOP.jpeg".format(self.cherry_picture_directory, file_name))
        self.picture_B.original = cv2.imread("{}{}_BUTTOM.jpeg".format(self.cherry_picture_directory, file_name))
        self.picture_L.original = cv2.imread("{}{}_LEFT.jpeg".format(self.cherry_picture_directory, file_name))
        self.picture_R.original = cv2.imread("{}{}_RIGHT.jpeg".format(self.cherry_picture_directory, file_name))

        if rotate==True:
            self.picture_L.original = cv2.rotate(self.picture_L.original, cv2.ROTATE_90_CLOCKWISE)
            self.picture_R.original = cv2.rotate(self.picture_R.original, cv2.ROTATE_90_COUNTERCLOCKWISE)

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

    # 4つ並べた画像を生成
    def combine(self, pictures):

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

    for i in range(783, 790):

        cherry_01 = cherry(i)

        # データ表示
        cherry_01.print_data()

        # 元画像表示
        print_picture("all", cherry_01.original_combine)

        # マスク画像
        cherry_01.cherry_detection()
        print_picture("red", cherry_01.masked_img_combine)
        print_picture("monochrome", cherry_01.monochrome_img_combine)
        print_picture("detection", cherry_01.detection_img_combine)

        cherry_01.trimming(2500)
        print_picture("trimming", cherry_01.trimming_img_combine)
        
        cv2.waitKey(0)