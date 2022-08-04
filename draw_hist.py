from matplotlib import pyplot as plt
from numpy import histogram
import pickle
import cherry

hist_data_pass = "C:\\Users\\cherr\\Desktop\\data\\Program\\cherry_labeling_HLS\\HLS_hist_data.pkl"

fig_h = plt.figure(figsize=(12,8))
ax_h = fig_h.add_subplot(111)
fig_l = plt.figure(figsize=(12,8))
ax_l = fig_l.add_subplot(111)
fig_s = plt.figure(figsize=(12,8))
ax_s = fig_s.add_subplot(111)

with open(hist_data_pass, "rb") as f:
    histograms = pickle.load(f)

for num in [1,3,9,15,1121]:

    print("\rread No.{}".format(num), end="")

    cherry_01 = cherry.cherry(num)

    hist_h = histograms[str(num)]['h']
    hist_l = histograms[str(num)]['l']
    hist_s = histograms[str(num)]['s']

    hist_h_x, hist_h_y, hist_l, hist_s = cherry_01.calc_hist(hist_h, hist_l, hist_s, percent=True, mooving_ave_size_HLS=[0,4,3], H_range=[-5, 15])
    
    ax_h.plot(hist_h_x, hist_h_y, label=cherry_01.file_name + "_h")
    ax_l.plot(hist_l, label=cherry_01.file_name + "_l")
    ax_s.plot(hist_s, label=cherry_01.file_name + "_s")

plt.legend()
plt.show()