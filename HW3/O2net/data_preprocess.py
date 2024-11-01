import os
import cv2
import json
import argparse
import glob

def get_args_parser():
    parser = argparse.ArgumentParser('Deformable DETR Detector', add_help=False)
    parser.add_argument('--img_path', default="./O2net/input/test_dir/", type=str)
    parser.add_argument('--save_file',default="",type=str)
    return parser

def get_file_names(folder_path,count):
    images = []
    mask = len(folder_path)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if "png" in file:
                path2=root+"/"+file
                img=cv2.imread(path2)
                path2 = path2[mask:]
                path2 = os.path.normpath(path2)
                path2 = path2.replace("\\",'/')
                size=img.shape
                img_dict={"id":count,"width":size[1],"height":size[0],"file_name":path2}
                images.append(img_dict)
                count+=1
    return images,count
save_dict={}
parser =get_args_parser()
args = parser.parse_args()
folder_path = args.img_path
count=0
images,_ = get_file_names(folder_path,count)
save_dict['images']=images
save_path = args.img_path+"/"+args.save_file
with open(save_path, "w") as outfile:
    json_object = json.dumps(save_dict,ensure_ascii=False)
    outfile.write(json_object) 

