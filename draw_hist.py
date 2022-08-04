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

    # %へ変換
    # hist_h = [n/sum(hist_h)*100 for n in hist_h]
    hist_l = [n/sum(hist_l)*100 for n in hist_l]
    # hist_s = [n/sum(hist_s)*100 for n in hist_s]
    
    # ax.plot(hist_h, label=cherry_01.file_name + "_h")
    ax.plot(hist_l, label=cherry_01.file_name + "_l")
    # ax.plot(hist_s, label=cherry_01.file_name + "_s")

plt.legend()
plt.show()