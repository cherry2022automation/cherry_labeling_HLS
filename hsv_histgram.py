import cherry
import cv2
from matplotlib import pyplot as plt
import pickle

pic_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640\\"
hist_data_pass = "C:\\Users\\cherr\\Desktop\\data\\Program\\cherry_labeling_HLS\\HLS_hist_data.pkl"

hsv_1_min = [0, 80, 10]
hsv_1_max = [30, 255, 255]
hsv_2_min = [160, 80, 10]
hsv_2_max = [179, 255, 255]

area_filter_min = 20000
area_filter_max = 250000


def get_hist(img, mask_img):

    hls_img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    h, l, s = hls_img[:,:,0], hls_img[:,:,1], hls_img[:,:,2]
    mask = mask_img[:,:,0]

    hist_h = cv2.calcHist([h],[0],mask,[256],[0,256])
    hist_l = cv2.calcHist([l],[0],mask,[256],[0,256])
    hist_s = cv2.calcHist([s],[0],mask,[256],[0,256])

    return hist_h, hist_l, hist_s


histograms = {}

for num in range(1931):

    num += 1

    print("\rget_histgram No.{}".format(num), end="")

    cherry_01 = cherry.cherry(num, picture_dir=pic_dir)
    if cherry_01.enable == False:
        continue

    cherry_01.open_picture()
    cherry_01.cherry_detection(hsv_1_min=hsv_1_min, hsv_1_max=hsv_1_max, hsv_2_min=hsv_2_min, hsv_2_max=hsv_2_max, area_filter_min=area_filter_min, area_filter_max=area_filter_max)

    cherry_01.combine(["original", "cherry_monochrome_img"])
    hist_h, hist_l, hist_s = get_hist(cherry_01.original_combine, cherry_01.cherry_monochrome_img_combine)

    hist = {"h":hist_h, "l":hist_l, "s":hist_s}
    histograms[str(num)] = hist

with open(hist_data_pass, "wb") as f:
    pickle.dump(histograms, f)