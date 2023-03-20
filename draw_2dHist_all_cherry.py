# https://qiita.com/supersaiakujin/items/ca47200393180a693bdf

import numpy as np
import matplotlib.cm as cm
import cherry
from matplotlib import pyplot as plt

pic_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640\\"

# 代表の番号
tokushu_num = [1,46,47,48,49,50,51,239,240,242,243,245,247,251,252,253,254,255,256,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,276,277,278,279,281,282,284,285,287,288,289,290,291,293,295,296,298,299,304,306,307,308,309,311,314,315,316,318,319,321,322,325,334,337,340,342,345,347,348,349,351,352,357,360,361,362,364,367,368,370,372,373,374,375,377,378,380,382,383,384,386,392,393,394,399,401,402,407,568,571,575,579,580,583,589,590,592,601,602,605,606,608,609,615,617,618,621,624,631,632,641,656,666,668,674,816,1138,1139,1144,1146,1155,1161,1162,1167,1169,1176,1179,1183,1184,1185,1188,1190,1191,1386,1387,1393,1400,1409,1419,1423,1427,1438,1443]
shu_num = [4,5,52,53,59,60,64,66,67,73,74,75,82,84,86,87,88,90,93,94,97,100,101,102,109,111,117,121,127,128,133,134,137,139,142,144,145,149,153,157,158,162,163,169,170,172,173,175,177,178,179,181,415,419,441,443,446,459,461,464,467,472,473,475,477,487,491,494,502,505,699,702,704,712,739,750,755,765,766,768,772,782,796,799,804,805,811,827,832,833,837,839,841,842,847,848,849,850,854,856,857,863,865,871,873,876,879,880,886,892,896,901,905,909,911,915,919,1003,1005,1012,1016,1018,1019,1020,1027,1033,1034,1035,1036,1193,1195,1197,1198,1199,1200,1205,1206,1207,1208,1211,1215,1216,1217,1219,1225,1227,1230,1232,1233,1236,1240,1247,1249,1253,1254,1255,1258]
marushu_num = [13,186,202,205,206,210,214,218,524,527,529,531,532,535,536,539,543,547,548,549,550,934,937,938,1037,1038,1040,1041,1042,1043,1045,1046,1048,1050,1051,1052,1053,1056,1058,1059,1060,1063,1064,1065,1066,1067,1068,1069,1071,1072,1260,1261,1263,1267,1271,1272,1274,1277,1279,1280,1282,1284,1288,1289,1290,1291,1294,1295,1296,1297,1300,1301,1302,1303]
hanedashi_num = [1101,1105,1305,1306,1307,1308,1309,1310,1311,1312,1313,1316,1319,1321]
all_num = tokushu_num, shu_num, marushu_num, hanedashi_num

# 対象データを選択
data_num = marushu_num

# 果実表面値域
hsv_1_min = [0, 80, 10]
hsv_1_max = [30, 255, 255]
hsv_2_min = [160, 80, 10]
hsv_2_max = [179, 255, 255]

area_filter_min = 20000
area_filter_max = 250000

all_h = None
all_l = None
all_s = None

for num in data_num:

    print("\rget_histgram No.{}".format(num), end="")

    # データ読み込み
    cherry_01 = cherry.cherry(num, picture_dir=pic_dir)
    if cherry_01.enable == False:
        continue

    # 画像読み込み
    cherry_01.open_picture()
    # 果実領域検出
    cherry_01.cherry_detection(hsv_1_min=hsv_1_min, hsv_1_max=hsv_1_max, hsv_2_min=hsv_2_min, hsv_2_max=hsv_2_max, area_filter_min=area_filter_min, area_filter_max=area_filter_max)

    # 結合画像生成
    cherry_01.combine(["original", "cherry_monochrome_img", "cherry_masked_img"])
    # 果実領域画素のhls値を取得(各1次元)
    h, l, s = cherry_01.get_hist_for_2dhist(cherry_01.original_combine, cherry_01.cherry_monochrome_img_combine)

    # 画素データを全果実分結合
    if all_h is None:
        all_h = h
        all_l = l
        all_s = s
    else:
        all_h = np.concatenate([all_h, h], 0)
        all_l = np.concatenate([all_l, l], 0)
        all_s = np.concatenate([all_s, s], 0)

# ヒストグラム分割数
bins = 180

fig = plt.figure()
ax_hl = fig.add_subplot(2, 2, 3)
ax_sl = fig.add_subplot(2, 2, 4)
ax_hs = fig.add_subplot(2, 2, 1)

H_hl = ax_hl.hist2d(all_h, all_l, bins=bins, cmap=cm.jet, cmin=1)
ax_hl.set_title('Hue-Lightness')
ax_hl.set_xlabel('Hue')
ax_hl.set_ylabel('Lightness')

H_ls = ax_sl.hist2d(all_s, all_l, bins=bins, cmap=cm.jet, cmin=1)
ax_sl.set_title('Saturation-Lightness')
ax_sl.set_xlabel('Saturation')
ax_sl.set_ylabel('Lightness')

H_hs = ax_hs.hist2d(all_h, all_s, bins=bins, cmap=cm.jet, cmin=1)
ax_hs.set_title('Hue-Saturation')
ax_hs.set_xlabel('Hue')
ax_hs.set_ylabel('Saturation')

fig.colorbar(H_hl[3],ax=ax_hl)
fig.colorbar(H_ls[3],ax=ax_sl)
fig.colorbar(H_hs[3],ax=ax_hs)

plt.subplots_adjust(wspace=0.6, hspace=0.6)

plt.show()