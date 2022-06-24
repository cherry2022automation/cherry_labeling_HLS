# サクランボオブジェクト
# サクランボの写真,品種,等級,測定値やそれに関する処理など

# T19JM042 長谷季樹

# 2022/06/24    画像読み込み処理記述 → 確認
#               サクランボデータ,画像読み込み処理記述(エクセルデータ使用)

import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()  # opencvの読み込み画像サイズの上限を変更
import cv2
import openpyxl

class cherry():

    # サクランボデータのファイルパス
    cherry_data_pass = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\cherry_data.xlsx"
    cherry_data_sheet_name = "all numerical data"
    cherry_picture_directory = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\original\\"

    # サクランボデータ
    picture_T = None
    picture_B = None
    picture_L = None
    picture_R = None

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

    # 単一の画像ファイルを読み込み,変数pictureに保存
    def open_picture(self, file_name):
        self.picture_T = cv2.imread("{}{}_TOP.bmp".format(self.cherry_picture_directory, file_name))
        self.picture_B = cv2.imread("{}{}_BUTTOM.bmp".format(self.cherry_picture_directory, file_name))
        self.picture_L = cv2.imread("{}{}_LEFT.bmp".format(self.cherry_picture_directory, file_name))
        self.picture_L = cv2.rotate(self.picture_L, cv2.ROTATE_90_CLOCKWISE)
        self.picture_R = cv2.imread("{}{}_RIGHT.bmp".format(self.cherry_picture_directory, file_name))
        self.picture_R = cv2.rotate(self.picture_R, cv2.ROTATE_90_COUNTERCLOCKWISE)

# 画像の読み込み、表示テスト
if __name__ == "__main__":

    cherry_01 = cherry()

    cherry_01.get_data(1)
    cherry_01.print_data()

    cv2.imshow("cherry_01_T", cherry_01.picture_T)
    cv2.imshow("cherry_01_B", cherry_01.picture_B)
    cv2.imshow("cherry_01_L", cherry_01.picture_L)
    cv2.imshow("cherry_01_R", cherry_01.picture_R)
    cv2.waitKey(0)
    cv2.destroyAllWindows()