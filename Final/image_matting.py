from rembg import remove
import cv2
import os

def Image_Matting(img_dir,output_dir):
    file_names = os.listdir(img_dir)
    for file_name in file_names:
        input_path = os.path.join(img_dir,file_name)
        output_path = os.path.join(output_dir,file_name)
        input = cv2.imread(input_path)
        output = remove(input)
        cv2.imwrite(output_path, output)

