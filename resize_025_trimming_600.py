import resize
import trimming
import cherry

# リサイズ元ディレクトリ
resize.open_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\original\\"

# 出力先ディレクトリ
resize.output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025\\"

# 拡大率
resize.magnification = 0.25

# トリミング元ディレクトリ
trimming.open_dir = resize.output_dir

# 出力先ディレクトリ
trimming.output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_600\\"

trimming.trm_size = 600

trimming.hsv_1_min = [0, 80, 30]
trimming.hsv_1_max = [15, 255, 255]
trimming.hsv_2_min = [160, 80, 30]
trimming.hsv_2_max = [179, 255, 255]

trimming.area_filter_min = 10000
trimming.area_filter_max = 250000


resize_failed = resize.resize()
trim_failed = trimming.trim()

print("---------------------------------")

print("")
print("resize_failed")
print(resize_failed)

print("")
print("trim_failed")
print(trim_failed)