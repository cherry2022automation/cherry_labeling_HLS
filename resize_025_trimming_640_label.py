import resize
import trimming
import cherry
import put_label

# リサイズ元ディレクトリ
resize.open_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\original\\"

# 出力先ディレクトリ
resize.output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025\\"

# 拡大率
resize.magnification = 0.25

# トリミング元ディレクトリ
trimming.open_dir = resize.output_dir

# 出力先ディレクトリ
trimming.output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640\\"

trimming.trm_size = 640

trimming.hsv_1_min = [0, 80, 10]
trimming.hsv_1_max = [30, 255, 255]
trimming.hsv_2_min = [160, 80, 10]
trimming.hsv_2_max = [179, 255, 255]

trimming.area_filter_min = 20000
trimming.area_filter_max = 250000

# ラベルつけ
put_label.open_dir = trimming.output_dir
put_label.output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640_label\\"


resize_failed = resize.resize()
trim_failed = trimming.trim()
label_failed = put_label.put_label()

print("---------------------------------")

print("")
print("resize_failed")
print(resize_failed)

print("")
print("trim_failed")
print(trim_failed)