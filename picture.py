# 画像関連のオブジェクト
# 画像の色検出, モノクロ化, トリミング処理など

# T19JM042 長谷季樹

# 2022/06/29    作成
#               マスク処理追加 (cherry.pyから移動)
#               さくらんぼ検出処理追加

from pstats import Stats
import cv2
import numpy as np
import copy

class picture():

    # 画像データ
    original = None             # 元画像
    hsv_masked_img = None       # hsv閾値で背景を水色にした画像
    hsv_monochrome_img = None   # hsv閾値で該当領域を白, その他を黒にした画像 
    detection_img = None        # 元画像にサクランボの外接矩形を描画した画像
    trim_img = None             # トリミング後の画像
    resize_img = None           # リサイズ後の画像
    labels = None               # ラベリング結果
    cherry_masked_img = None    # さくらんぼ以外の背景を水色にした画像

    # マスク情報
    hsv_mask = None             # hsv閾値でのマスク結果
    cherry_mask = None      # サクランボ領域以外のマスク

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
    hsv_1_min = [0, 80, 10]
    hsv_1_max = [15, 255, 255]
    hsv_2_min = [160, 80, 10]
    hsv_2_max = [179, 255, 255]

    mask_color = [255, 255, 0]

    # ラベリング時サイズフィルタ
    area_filter_min = 1000000
    area_filter_max = 3000000

    def resize(self, magnification):
        self.resize_img = cv2.resize(self.original, dsize=None, fx=magnification, fy=magnification)

    def trimming(self, size):

        width = int(size/2)
        add_outer_frame_img = self.insert_outer_frame(self.original, width)

        trm_x_min = int( self.g_x - (size/2) + width)
        trm_x_max = int( self.g_x + (size/2) + width)
        trm_y_min = int( self.g_y - (size/2) + width)
        trm_y_max = int( self.g_y + (size/2) + width)

        self.trim_img = add_outer_frame_img[trm_y_min:trm_y_max, trm_x_min:trm_x_max]

    def insert_outer_frame(self, img, width):
    
        #枠追加処理(上下)
        bk1=np.zeros((width,img.shape[1],3),np.uint8)
        array=np.insert(img, 0, bk1, axis=0)
        array=np.insert(array, array.shape[0], bk1, axis=0)

        #枠追加処理(左右)
        bk2=np.zeros((array.shape[0],width,3),np.uint8)
        array=np.insert(array, [0], bk2, axis=1)
        array=np.insert(array, [array.shape[1]], bk2, axis=1)

        return array

    # さくらんぼ検出
    def cherry_detection(self):

        stats, centroids = self.labelling(self.hsv_monochrome_img)
        self.get_status(stats, centroids)
        self.detection_img = copy.copy(self.original)
        self.detection_img = cv2.rectangle(self.detection_img, (self.x, self.y), (self.x+self.width, self.y+self.height), (255,255,0), thickness=10)

    # ラベリング処理
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

        self.labels = labels

        return stats, centroids

    # ラベリング結果取得
    def get_status(self, stats, centroids):

        for i in range(len(stats)):

            # 領域サイズでサクランボを識別
            area = stats[i][cv2.CC_STAT_AREA]
            if self.area_filter_min <= area and area <= self.area_filter_max:

                # 該当データを取得
                self.x = stats[i][cv2.CC_STAT_LEFT]
                self.y = stats[i][cv2.CC_STAT_TOP]
                self.width = stats[i][cv2.CC_STAT_WIDTH]
                self.height = stats[i][cv2.CC_STAT_HEIGHT]
                self.area = stats[i][cv2.CC_STAT_AREA]
                self.diameter = (self.width + self.height) / 2

                # 重心取得
                self.g_x, self.g_y = centroids[i]
                self.g_x = int(self.g_x)
                self.g_y = int(self.g_y)

                # サクランボ領域のみのマスクを取得
                self.cherry_mask = np.zeros(self.original.shape[:2], np.uint8)
                self.cherry_mask[self.labels==i] = 255

                self.cherry_masked_img = copy.copy(self.original)
                self.cherry_masked_img[self.labels!=i] = self.mask_color

    def print_status(self):
        print("x        :{}".format(self.x))
        print("y        :{}".format(self.y))
        print("g_x      :{}".format(self.g_x))
        print("g_y      :{}".format(self.g_y))
        print("width    :{}".format(self.width))
        print("height   :{}".format(self.height))
        print("area     :{}".format(self.area))
        print("diameter :{}".format(self.diameter))

    # 赤色マスク処理
    def mask_red(self):
        
        # マスク処理
        self.hsv_mask, self.hsv_masked_img , self.hsv_monochrome_img = self.detect_red_color(self.original)

    # 赤色の検出
    def detect_red_color(self, img):
        # HSV色空間に変換
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
        # 赤色のHSVの値域1
        hsv_min = np.array(self.hsv_1_min)
        hsv_max = np.array(self.hsv_1_max)
        mask1 = cv2.inRange(hsv, hsv_min, hsv_max)
    
        # 赤色のHSVの値域2
        hsv_min = np.array(self.hsv_2_min)
        hsv_max = np.array(self.hsv_2_max)
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
