import cherry
import cv2
from matplotlib import pyplot as plt
import pickle

pic_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640\\"
hist_data_pass = "C:\\Users\\cherr\\Desktop\\data\\Program\\cherry_labeling_HLS\\HLS_hist_data_test.pkl"

hsv_1_min = [0, 80, 10]
hsv_1_max = [30, 255, 255]
hsv_2_min = [160, 80, 10]
hsv_2_max = [179, 255, 255]

area_filter_min = 20000
area_filter_max = 250000


histograms = {}

for num in range(5):

    num += 1

    print("\rget_histgram No.{}".format(num), end="")

    cherry_01 = cherry.cherry(num, picture_dir=pic_dir)
    if cherry_01.enable == False:
        continue

    cherry_01.open_picture()
    cherry_01.cherry_detection(hsv_1_min=hsv_1_min, hsv_1_max=hsv_1_max, hsv_2_min=hsv_2_min, hsv_2_max=hsv_2_max, area_filter_min=area_filter_min, area_filter_max=area_filter_max)

    cherry_01.combine(["original", "cherry_monochrome_img"])
    hist_h, hist_l, hist_s = cherry_01.get_hist(cherry_01.original_combine, cherry_01.cherry_monochrome_img_combine)

    hist = {"h":hist_h, "l":hist_l, "s":hist_s}
    histograms[str(num)] = hist

with open(hist_data_pass, "wb") as f:
    pickle.dump(histograms, f)