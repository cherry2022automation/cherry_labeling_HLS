from tabnanny import NannyNag
import cherry

output_dir = "C:\\Users\\cherr\\Desktop\\data\\Program\\cherry_labeling_HLS\\sorted_number.csv"

variety_jp = {"Takasago":"高砂", "Satonishiki":"佐藤錦", "Benishuho":"紅秀峰", "Nanyo":"南陽"}
grade_jp = {"Tokushu":"特秀", "Shu":"秀", "Marushu":"マル秀", "Hanedashi":"ハネ出し", "Sute":"捨て"}

list = {}

for v_key in variety_jp:
    for g_Key in grade_jp:
        list_key = variety_jp[v_key]+grade_jp[g_Key]
        list[list_key] = []

for num in range(1, 1931+1):

    cherry_01 = cherry.cherry(num)
    
    if cherry_01.enable == False:
        continue

    key = cherry_01.variety + cherry_01.grade

    list[key].append(num)


# テキスト生成
output_text = ""
for key in list:
    output_text += key
    output_text += ","
    for num in list[key]:
        output_text += str(num)
        output_text += ","

    output_text += "\n"

# csvで保存
with open(output_dir, 'w') as data:
    data.write(output_text)
