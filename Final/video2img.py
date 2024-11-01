import cv2
import argparse
import os
import yaml

def main(config):
  path = config['VIDEO_PATH']
  vidcap = cv2.VideoCapture(path)
  success,image = vidcap.read()
  count = 0
  output_dir = config['VIDEO_FRAME_DIR']
  if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

  while success:
    image = cv2.resize(image, (512, 768))  
    cv2.imwrite(f"{output_dir}{str(count).zfill(3)}.jpg", image)    
    success,image = vidcap.read()
    count += 1

if __name__ == "__main__":
  with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
  main(config)