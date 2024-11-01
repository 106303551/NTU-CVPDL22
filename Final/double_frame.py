import cv2
import os

def double_frame(img_dir,output_dir):
    file_names = os.listdir(img_dir)
    count = 0
    for file_name in file_names:
        input_path = os.path.join(img_dir,file_name)
        input = cv2.imread(input_path)
        for i in range(2):
            output_path = os.path.join(output_dir,f"{str(count).zfill(3)}.jpg")
            cv2.imwrite(output_path, input)
            count+=1

double_frame('frame','double_frame')