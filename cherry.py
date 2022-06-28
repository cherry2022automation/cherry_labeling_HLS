# サクランボオブジェクト
# サクランボの写真,品種,等級,測定値やそれに関する処理など

# T19JM042 長谷季樹

# 2022/06/24    画像読み込み処理追加
#               サクランボデータ,画像読み込み処理追加(エクセルデータ使用)
#               リサイズ表示追加
#               初期化関数追加
#               画像結合処理追加
# 2022/06/28    マスク処理(赤)追加

from json import detect_encoding
import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()  # opencvの読み込み画像サイズの上限を変更
import cv2
import openpyxl
import numpy as np

class cherry():

    # サクランボデータのファイルパス
    cherry_data_pass = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\cherry_data.xlsx"
    cherry_data_sheet_name = "all numerical data"
    cherry_picture_directory = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\original\\"

    # サクランボ画像
    picture_T = None
    picture_B = None
    picture_L = None
    picture_R = None
    picture_combine = None

    # マスク, マスク画像
    mask_T = None
    mask_B = None
    mask_L = None
    mask_R = None
    masked_img_T = None
    masked_img_B = None
    masked_img_L = None
    masked_img_R = None
    masked_img_combine = None

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

    # マスク処理パラメータ
    h_min_1 = 0
    h_max_1 = 15
    h_min_2 = 150
    h_max_2 = 179
    s_min = 70
    s_max = 255
    v_min = 0
    v_max = 255
    mask_color = [255, 255, 0]


    # オブジェクト初期化関数
    # オブジェクト生成時に実行
    def __init__(self, serial_num):
        self.get_data(serial_num)
        pictures = [self.picture_T, self.picture_B, self.picture_L, self.picture_R]
        self.picture_combine = self.combine(pictures)

    # 赤色マスク処理
    def mask_red(self):
        
        # マスク処理
        self.mask_T, self.masked_img_T = self.detect_red_color(self.picture_T)
        self.mask_B, self.masked_img_B = self.detect_red_color(self.picture_B)
        self.mask_L, self.masked_img_L = self.detect_red_color(self.picture_L)
        self.mask_R, self.masked_img_R = self.detect_red_color(self.picture_R)

        # マスク画像を結合
        pictures = [self.masked_img_T, self.masked_img_B, self.masked_img_L, self.masked_img_R]
        self.masked_img_combine = self.combine(pictures)

    # 赤色の検出
    def detect_red_color(self, img):
        # HSV色空間に変換
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
        # 赤色のHSVの値域1
        hsv_min = np.array([self.h_min_1, self.s_min, self.v_min])
        hsv_max = np.array([self.h_max_1, self.s_max, self.v_max])
        mask1 = cv2.inRange(hsv, hsv_min, hsv_max)
    
        # 赤色のHSVの値域2
        hsv_min = np.array([self.h_min_2, self.s_min, self.v_min])
        hsv_max = np.array([self.h_max_2, self.s_max, self.v_max])
        mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    
        # 赤色領域のマスク（255：赤色、0：赤色以外）
        mask = mask1 + mask2
    
        # マスキング処理
        masked_img = cv2.bitwise_and(img, img, mask=mask)
        masked_img[mask==0] = self.mask_color
    
        return mask, masked_img

    # サクランボの写真とデータを読み込み
    # serial_num:サクランボのシリアルナンバー
    def get_data(self, serial_num):

        line = str(serial_num + 1)

        # Excelファイル読み込み
        cherry_data_file = openpyxl.load_workbook(self.cherry_data_pass)
        sheet = cherry_data_file[self.cherry_data_sheet_name]

        self.num = int(sheet["A" + line].value)
        self.file_name = sheet["B" + line].value
        self.variety = sheet["C" + line].value
        self.grade = sheet["D" + line].value
        self.weight = sheet["E" + line].value
        self.polar_diameter = sheet["F" + line].value
        self.equatorial_diameter = sheet["G" + line].value
        self.sugar_content_B = sheet["H" + line].value
        self.sugar_content_S = sheet["I" + line].value

        self.open_picture(self.file_name)

    # 単一の画像ファイルを読み込み,変数pictureに保存
    def open_picture(self, file_name):
        self.picture_T = cv2.imread("{}{}_TOP.bmp".format(self.cherry_picture_directory, file_name))
        self.picture_B = cv2.imread("{}{}_BUTTOM.bmp".format(self.cherry_picture_directory, file_name))
        self.picture_L = cv2.imread("{}{}_LEFT.bmp".format(self.cherry_picture_directory, file_name))
        self.picture_L = cv2.rotate(self.picture_L, cv2.ROTATE_90_CLOCKWISE)
        self.picture_R = cv2.imread("{}{}_RIGHT.bmp".format(self.cherry_picture_directory, file_name))
        self.picture_R = cv2.rotate(self.picture_R, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # サクランボデータの表示(コンソール)
    def print_data(self):
        print("------------------------------------------------------------")
        print("シリアル番号 : {}".format(self.num))
        print("ファイル名　 : {}".format(self.file_name))
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

        height, width, channnels = pictures[0].shape[:3]
        
        # 余白生成
        blank_height = int( (height*2 - width) / 2) 
        blank_width = height
        blank = np.zeros((blank_height, blank_width, 3))
        blank = blank.astype('uint8')

        # 画像結合
        img_left = cv2.vconcat([blank, pictures[2], blank])
        img_right = cv2.vconcat([blank, pictures[3], blank])
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

        cherry_01 = cherry(i)

        # データ表示
        cherry_01.print_data()

        # 元画像表示
        print_picture("all", cherry_01.picture_combine)

        # マスク画像
        cherry_01.mask_red()
        print_picture("red", cherry_01.masked_img_combine)

        cv2.waitKey(0)