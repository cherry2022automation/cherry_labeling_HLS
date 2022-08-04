from matplotlib import pyplot as plt
from numpy import histogram
import pickle
import cherry

hist_data_pass = "C:\\Users\\cherr\\Desktop\\data\\Program\\cherry_labeling_HLS\\HLS_hist_data.pkl"

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)

with open(hist_data_pass, "rb") as f:
    histograms = pickle.load(f)

for num in [1,3,9,15,1121]:

    print("\rread No.{}".format(num), end="")

    cherry_01 = cherry.cherry(num)

    hist_h = histograms[str(num)]['h']
    hist_l = histograms[str(num)]['l']
    hist_s = histograms[str(num)]['s']

    hist_h, hist_l, hist_s = cherry_01.calc_hist(hist_h, hist_l, hist_s, percent=True, mooving_ave_size_HLS=[0,4,3])
    
    # ax.plot(hist_h, label=cherry_01.file_name + "_h")
    ax.plot(hist_l, label=cherry_01.file_name + "_l")
    # ax.plot(hist_s, label=cherry_01.file_name + "_s")

plt.legend()
plt.show()