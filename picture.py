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
    trim_img = None

    # マスク情報
    mask = None

    # サクランボ検出時のラベリング結果
    x = None
    y = None
    g_x = None
    g_y = None
    width = None
    height = None
    area = None
    diameter = None

    # マスク処理パラメータ
    h_min_1 = 0
    h_max_1 = 15
    h_min_2 = 160
    h_max_2 = 179
    s_min = 80
    s_max = 255
    v_min = 10
    v_max = 255
    mask_color = [255, 255, 0]

    # ラベリング時サイズフィルタ
    area_filter_min = 1000000
    area_filter_max = 3000000

    def trimming(self, size):
        # trm_x_min = int( self.x + self.width/2 - size/2 )
        # trm_x_max = trm_x_min + size
        # trm_y_min = int( self.y + self.height/2 - size/2 )
        # trm_y_max = trm_y_min + size
        trm_x_min = int( self.g_x - (size/2) )
        trm_x_max = int( self.g_x + (size/2) )
        trm_y_min = int( self.g_y - (size/2) )
        trm_y_max = int( self.g_y + (size/2) )

        self.trim_img = self.original[trm_y_min:trm_y_max, trm_x_min:trm_x_max]

    # 赤色マスク処理
    def mask_red(self):
        
        # マスク処理
        self.mask, self.masked_img , self.monochrome_img = self.detect_red_color(self.original)

    # さくらんぼ検出
    def cherry_detection(self):
        labelling_result = self.labelling(self.monochrome_img)
        self.get_status(labelling_result)
        self.detection_img = copy.copy(self.original)
        self.detection_img = cv2.rectangle(self.detection_img, (self.x, self.y), (self.x+self.width, self.y+self.height), (255,255,0), thickness=10)

    # ラベリング結果取得
    def get_status(self, labelling_result):

        for result in labelling_result:
            area = result[0][cv2.CC_STAT_AREA]
            if self.area_filter_min <= area and area <= self.area_filter_max:
                self.x = result[0][cv2.CC_STAT_LEFT]
                self.y = result[0][cv2.CC_STAT_TOP]
                self.width = result[0][cv2.CC_STAT_WIDTH]
                self.height = result[0][cv2.CC_STAT_HEIGHT]
                self.area = result[0][cv2.CC_STAT_AREA]
                self.diameter = (self.width + self.height) / 2

                self.g_x, self.g_y = result[1]
                self.g_x = int(self.g_x)
                self.g_y = int(self.g_y)

    def print_status(self):
        print("x        :{}".format(self.x))
        print("y        :{}".format(self.y))
        print("g_x      :{}".format(self.g_x))
        print("g_y      :{}".format(self.g_y))
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

        labelling_result = zip(stats, centroids)

        return labelling_result

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
