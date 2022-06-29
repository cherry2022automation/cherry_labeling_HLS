# 画像関連のオブジェクト
# 画像の色検出, モノクロ化, トリミング処理など

# T19JM042 長谷季樹

# 2022/06/29    作成
#               マスク処理追加 (cherry.pyから移動)
#               さくらんぼ検出処理追加

import cv2
import numpy as np
import copy

class picture():

    # 画像データ
    original = None
    masked_img = None
    monochrome_img = None
    detection_img = None
    label_img = None

    # マスク情報
    mask = None

    # サクランボ検出時のラベリング結果
    x = None
    y = None
    width = None
    height = None
    area = None
    diameter = None

    # マスク処理パラメータ
    h_min_1 = 0
    h_max_1 = 15
    h_min_2 = 150
    h_max_2 = 179
    s_min = 70
    s_max = 255
    v_min = 10
    v_max = 255
    mask_color = [255, 255, 0]

    # ラベリング時サイズフィルタ
    area_filter_min = 1000000
    area_filter_max = 3000000

    # 赤色マスク処理
    def mask_red(self):
        
        # マスク処理
        self.mask, self.masked_img , self.monochrome_img = self.detect_red_color(self.original)

    # さくらんぼ検出
    def cherry_detection(self):
        stats = self.labelling(self.monochrome_img)
        self.get_status(stats)
        self.detection_img = copy.copy(self.original)
        self.detection_img = cv2.rectangle(self.detection_img, (self.x, self.y), (self.x+self.width, self.y+self.height), (255,255,0), thickness=10)

    # ラベリング結果取得
    def get_status(self, stats):

        for stat in stats:
            area = stat[cv2.CC_STAT_AREA]
            if self.area_filter_min <= area and area <= self.area_filter_max:
                self.x = stat[cv2.CC_STAT_LEFT]
                self.y = stat[cv2.CC_STAT_TOP]
                self.width = stat[cv2.CC_STAT_WIDTH]
                self.height = stat[cv2.CC_STAT_HEIGHT]
                self.area = stat[cv2.CC_STAT_AREA]
                self.diameter = (self.width + self.height) / 2

    def print_status(self):
        print("x        :{}".format(self.x))
        print("y        :{}".format(self.y))
        print("width    :{}".format(self.width))
        print("height   :{}".format(self.height))
        print("area     :{}".format(self.area))
        print("diameter :{}".format(self.diameter))

    # ラベリング処理(未実装)
    def labelling(self, img):
        
        # グレースケールに変換する。
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 2値化する
        ret, bin_img = cv2.threshold(gray, 0, 255, cv2.THRESH_TRIANGLE)
        # カーネルを作成する。
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        # オープニング処理
        bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel, iterations=3)
        # クロージング処理
        bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel, iterations=3)
        # 連結成分のラベリングを行う。
        retval, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_img)

        return stats

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
    
        # マスキング処理 (確認用)
        masked_img = cv2.bitwise_and(img, img, mask=mask)
        masked_img[mask==0] = self.mask_color
        
        # モノクロ化 (処理用)
        monochrome_img = copy.copy(masked_img)
        monochrome_img[mask==0] = [0,0,0]
        monochrome_img[mask!=0] = [255,255,255]
    
        return mask, masked_img, monochrome_img
