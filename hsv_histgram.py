import cherry
import cv2
from matplotlib import pyplot as plt

pic_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025\\"

hsv_1_min = [0, 80, 10]
hsv_1_max = [30, 255, 255]
hsv_2_min = [160, 80, 10]
hsv_2_max = [179, 255, 255]

area_filter_min = 20000
area_filter_max = 250000

cherry_01 = cherry.cherry(1348, picture_dir=pic_dir)
cherry_01.cherry_detection(hsv_1_min=hsv_1_min, hsv_1_max=hsv_1_max, hsv_2_min=hsv_2_min, hsv_2_max=hsv_2_max, area_filter_min=area_filter_min, area_filter_max=area_filter_max)

img2 = cv2.cvtColor(cherry_01.original_combine, cv2.COLOR_BGR2HLS)
h, l, s = img2[:,:,0], img2[:,:,1], img2[:,:,2]
mask = cherry_01.cherry_monochrome_img_combine[:,:,0]
hist_h = cv2.calcHist([h],[0],mask,[256],[0,256])
hist_l = cv2.calcHist([l],[0],mask,[256],[0,256])
hist_s = cv2.calcHist([s],[0],mask,[256],[0,256])
plt.plot(hist_h, color='r', label="h")
plt.plot(hist_l, color='g', label="l")
plt.plot(hist_s, color='b', label="s")
plt.legend()
plt.show()