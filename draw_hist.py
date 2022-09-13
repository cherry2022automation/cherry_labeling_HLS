from matplotlib import pyplot as plt
from numpy import histogram
import pickle
import cherry

hist_data_pass = "C:\\Users\\cherr\\Desktop\\data\\Program\\cherry_labeling_HLS\\HLS_hist_data.pkl"
output_dir = "C:\\Users\\cherr\\Desktop\\data\\histogram\\satonishiki_all\\"

grade_color = {"特秀":"b", "秀":"g", "マル秀":"r", "ハネ出し":"c", "捨て":"m"}

# hls_data = [239,251,244,327,673,684] # 特秀Lまとめ
# hls_data = [1,251,307,569,673,1420,1427] # 特秀Hまとめ
# hls_data = [303,341,350,576,620,653,1137,] # 特秀まとめ
# hls_data = [182,489,845,881,993,1014] # 秀Lまとめ
# hls_data = [6,65,444,1005,1015,1232] # 秀Hまとめ
# hls_data = [14,189,210,217,539,925,1042] # マル秀Hまとめ
# hls_data = [14,185,201,525,1044,1274]
# hls_data = [576,620,1137,1384,1397] # 特秀Sまとめ
# hls_data = [57,158,734,987,1248] # 秀Sまとめ
hls_data = [13,14,191,538,924,937,1045] # マル秀Sまとめ


with open(hist_data_pass, "rb") as f:
    histograms = pickle.load(f)

def add_hist(num):

    print("\rread No.{}".format(num), end="")

    cherry_01 = cherry.cherry(num)

    hist_h = histograms[str(num)]['h']
    hist_l = histograms[str(num)]['l']
    hist_s = histograms[str(num)]['s']

    hist_h_x, hist_h_y, hist_l, hist_s = cherry_01.calc_hist(hist_h, hist_l, hist_s, percent=True, mooving_ave_size_HLS=[0,4,3], H_range=[-5, 15])
    
    # ax_h.plot(hist_h_x, hist_h_y, label=cherry_01.file_name + "_h", color=grade_color[cherry_01.grade])
    # ax_l.plot(hist_l, label=cherry_01.file_name + "_l", color=grade_color[cherry_01.grade])
    # ax_s.plot(hist_s, label=cherry_01.file_name + "_s", color=grade_color[cherry_01.grade])

    # ax_h.plot(hist_h_x, color=grade_color[cherry_01.grade])
    # ax_l.plot(hist_l, color=grade_color[cherry_01.grade])
    # ax_s.plot(hist_s, color=grade_color[cherry_01.grade])

    ax_h.plot(hist_h_x, hist_h_y, label=cherry_01.file_name + "_h",)
    ax_l.plot(hist_l, label=cherry_01.file_name + "_l",)
    ax_s.plot(hist_s, label=cherry_01.file_name + "_s",)

def save_hist(cycle):
    ax_h.figure.savefig(output_dir + "h_No" + str(cycle+1) + ".png")
    ax_l.figure.savefig(output_dir + "l_No" + str(cycle+1) + ".png")
    ax_s.figure.savefig(output_dir + "s_No" + str(cycle+1) + ".png")

def draw_hist():
    ax_h.legend()
    ax_h.set_title('Hue')
    ax_h.set_ylabel("Percentage of pixels")
    ax_h.set_xlabel("Value")

    ax_l.legend()
    ax_l.set_title('Lightness')
    ax_l.set_ylabel("Percentage of pixels")
    ax_l.set_xlabel("Value")

    ax_s.legend()
    ax_s.set_title('Saturation')
    ax_s.set_ylabel("Percentage of pixels")
    ax_s.set_xlabel("Value")

fig_h = plt.figure(figsize=(12,8))
ax_h = fig_h.add_subplot(111)
fig_l = plt.figure(figsize=(12,8))
ax_l = fig_l.add_subplot(111)
fig_s = plt.figure(figsize=(12,8))
ax_s = fig_s.add_subplot(111)

for num in hls_data:

    add_hist(num)

draw_hist()
plt.show()