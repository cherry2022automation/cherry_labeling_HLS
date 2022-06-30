import cv2
import cherry

output_dir = "C:\\Users\\cherr\\Desktop\\data\\cherry_photo\\trimming_01\\"

trm_size = 2500
picture_num = 812

# 画像の読み込み、表示テスト
if __name__ == "__main__":

    for i in range(1, picture_num+1):

        try:

            cherry_01 = cherry.cherry(i)

            # さくらんぼ検出
            cherry_01.cherry_detection()

            # トリミング
            cherry_01.trimming(trm_size)
            
            for dir in cherry_01.pictures:
                cv2.imwrite(output_dir + cherry_01.file_name + "_" + dir + ".bmp", cherry_01.pictures[dir].trim_img)

            print("{} done".format(i))
        except:
            pass