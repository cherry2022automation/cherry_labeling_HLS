# サクランボオブジェクト
# サクランボの写真,品種,等級,測定値やそれに関する処理など

# T19JM042 長谷季樹

# 2022/06/24    画像読み込み処理記述 → 確認

import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()  # opencvの読み込み画像サイズの上限を変更
import cv2

class cherry():

    # サクランボデータのファイルパス
    cherry_data_pass = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\cherry_data.xlsx"

    # サクランボデータ
    picture = None
    variety = None
    grade = None

    # 単一の画像ファイルを読み込み,変数pictureに保存
    def open_picture(self, file_pass):

        self.picture = cv2.imread(file_pass)

# 画像の読み込み、表示テスト
if __name__ == "__main__":

    file_pass = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\original\\00001_Satonishiki_Tokushu_S_2022-06-17_14-08-25_TOP.bmp"

    cherry_01 = cherry()
    cherry_01.open_picture(file_pass)

    cv2.imshow("cherry_01", cherry_01.picture)

    cv2.waitKey(0)
    cv2.destroyAllWindows()