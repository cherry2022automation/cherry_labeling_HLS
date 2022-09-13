import matplotlib
from matplotlib import pyplot as plt
from numpy import histogram
import pickle
import cherry
import numpy as np

matplotlib.use('Agg')

hist_value_list_data_pass = "C:\\Users\\cherr\\Desktop\\data\\Program\\cherry_labeling_HLS\\hist_value_list.pkl"
output_dir = "C:\\Users\\cherr\\Desktop\\data\\result\\all_pattern_boxplot\\"

grade_color = {"特秀":"b", "秀":"g", "マル秀":"r", "ハネ出し":"c", "捨て":"m"}

with open(hist_value_list_data_pass, "rb") as f:
    data = pickle.load(f)
    cherry_num_lists, hist_value_lists, grade_lists = data

def grade_value_list(hist_value_lists, k_h, k_l, k_s, o_h, o_l, o_s):

    grade_value_list = []

    for data in hist_value_lists:

        value_h, value_l, value_s = data
        
        grade_value = k_h*value_h+o_h + k_l*value_l+o_l + k_s*value_s+o_s
        grade_value_list.append(grade_value)

    return grade_value_list

def output_boxplot(num, k_h, k_l, k_s, o_h, o_l, o_s):

    grade_value_list_tokushu = grade_value_list(hist_value_lists[0], k_h, k_l, k_s, o_h, o_l, o_s)
    grade_value_list_shu = grade_value_list(hist_value_lists[1], k_h, k_l, k_s, o_h, o_l, o_s)
    grade_value_list_marushu = grade_value_list(hist_value_lists[2], k_h, k_l, k_s, o_h, o_l, o_s)

    # grade_value_lists = grade_value_list_tokushu + grade_value_list_shu + grade_value_list_marushu
    # grade_lists = [3]*len(grade_value_list_tokushu) + [2]*len(grade_value_list_shu) + [1]*len(grade_value_list_marushu)

    boxplot_name = "{}_Hx({})+({})_Lx({})+({})_Sx({})+({})".format(num, k_h,o_h, k_l,o_l, k_s,o_s)
    output_pass = "{}{}.png".format(output_dir, boxplot_name)

    # 箱ひげ図
    fig, ax = plt.subplots()
    ax.boxplot([grade_value_list_marushu, grade_value_list_shu, grade_value_list_tokushu], labels=['marushu', 'shu', 'tokushu'], vert=False)
    ax.set_title(boxplot_name)

    plt.savefig(output_pass, format="png", dpi=300)
    # plt.show()
    #図形クリア
    plt.clf()
    #window閉じる
    plt.close()

k_range = np.arange(-1, 1, 0.1)
o_range = np.arange(-100, 100, 5)

for i in range(len(k_range)):
    k_range[i] = round(k_range[i], 1)

process_num = len(k_range)**3 #* len(o_range)**3
num = 1

o_h = 0
o_l = 0
o_s = 0

failed = []

for k_h in k_range:
    for k_l in k_range:
        for k_s in k_range:
            # for o_h in o_range:
            #     for o_l in o_range:
            #         for o_s in o_range:
            try:
                output_boxplot(num, k_h, k_l, k_s, o_h, o_l, o_s)
                print("\rprocess : {} / {}".format(num, process_num), end="")
                num += 1

            except:
                print("failed")
                failed.append(num)

print(failed)