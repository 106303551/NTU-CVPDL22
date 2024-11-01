import glob
import numpy as np
from PIL import Image
import cv2
from tqdm import tqdm
import os 
#疊加相同time step圖片 圖片放到out裡
files = glob.glob("out/**/*.png")
file_dict={}
files_list=[]
if files is not None:
    files = sorted(files)
    for tpath in files:
        root,file = os.path.split(tpath)
        if file not in file_dict.keys():
            file_dict[file]=np.array(Image.open(tpath))
        else:
            file_dict[file] = cv2.addWeighted(file_dict[file],0.5,np.array(Image.open(tpath)),0.5,0)
    for k,v in file_dict.items():
        files_list.append(v)
    height, width, _ = files_list[0].shape

    fps = 30
    video_name = "default.mp4"

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    for img in tqdm(files_list):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        video_writer.write(img)
    video_writer.release()