import glob
import numpy as np
from PIL import Image
import cv2
from tqdm import tqdm

files = glob.glob("out_000/*.png")

if files is not None and files != []:
    files = sorted(files)
    files = [np.array(Image.open(f)) for f in files]
    height, width, _ = files[0].shape

    fps = 30
    video_name = "default.mp4"

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    for img in tqdm(files):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        video_writer.write(img)
    video_writer.release()