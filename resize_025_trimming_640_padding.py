import resize
import trimming
import padding
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
trimming.output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640\\"
# トリミングサイズ
trimming.trm_size = 640
# hsv閾値
trimming.hsv_1_min = [0, 80, 10]
trimming.hsv_1_max = [30, 255, 255]
trimming.hsv_2_min = [160, 80, 10]
trimming.hsv_2_max = [179, 255, 255]
# 面積フィルタ
trimming.area_filter_min = 20000
trimming.area_filter_max = 250000

# パディング元ディレクトリ
padding.open_dir = trimming.output_dir
# 出力先ディレクトリ
padding.output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\resize_025_trim_640_padding\\"
# hsv閾値
padding.hsv_1_min = [0, 80, 10]
padding.hsv_1_max = [30, 255, 255]
padding.hsv_2_min = [160, 80, 10]
padding.hsv_2_max = [179, 255, 255]
# 面積フィルタ
padding.area_filter_min = 20000
padding.area_filter_max = 250000

resize_failed = resize.resize()
trim_failed = trimming.trim()
padding_failed = padding.padding()

print("---------------------------------")

print("")
print("resize_failed")
print(resize_failed)

print("")
print("trim_failed")
print(trim_failed)

print("")
print("padding failed")
print(padding_failed)