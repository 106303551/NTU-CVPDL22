import cv2
import os
import yaml
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from base64 import b64encode
import ImageBind.data as data
import torch
from ImageBind.models import imagebind_model
from ImageBind.models.imagebind_model import ModalityType
import argparse

def video2img(config):
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


def option_img2img(url):
    option_payload = {
    "do_not_add_watermark": True,
    "sd_model_checkpoint": "2D\\abyssorangemix3AOM3_aom3a1b.safetensors",
    "sd_vae":"orangemix.vae.pt"
    }
    requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)

def img2img(config, im, url):
    prompt=config['STABLE_DIFFUSION']['PROMPT']
    negative_prompt=config['STABLE_DIFFUSION']['N_PROMPT']
    output_dir = config['STABLE_DIFFUSION']['OUTPUT_DIR']

    img_bytes = io.BytesIO()
    im.save(img_bytes, format='PNG')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')    

    file_name_without_extension = os.path.splitext(file_name)[0]
    os.makedirs(output_dir+file_name_without_extension, exist_ok=True)
    img2img_payload = {
        "init_images": [img_base64],
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "denoising_strength": 0.6,
        "width": 512,
        "height": 768,
        "cfg_scale": 7,
        "sampler_name": "DPM++ 2M Karras",
        "restore_faces": False,
        "steps": 26,
        "batch_size":5,
        "n_iter":2,
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "input_image": img_base64,
                        "module": "canny",
                        "model": "control_sd15_canny [fef5e48e]",
                        "processor_res":512,
                    }
                ]
            }
        }        
    }

    img2img_response = requests.post(url=f'{url}/sdapi/v1/img2img', json=img2img_payload)

    r = img2img_response.json()
    j=1
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        filename = output_dir+file_name_without_extension+"/img"+str(j)+".png"
        image.save(filename, pnginfo=pnginfo)
        j=j+1


def imagebind(source_image_path, target_folder_path):
    file_list = os.listdir(target_folder_path)      
    file_count = len(file_list)                     
    max_simility = 0
    image_paths=[source_image_path]
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = imagebind_model.imagebind_huge(pretrained=True)
    model.eval()
    model.to(device)
    inputs = {
        ModalityType.VISION: data.load_and_transform_vision_data(image_paths, device),
    }
    with torch.no_grad():
        source_embeddings = model(inputs)

    for i in range(len(file_list)):
        file_path = os.path.join(target_folder_path, file_list[i])
        target_image_paths=[file_path]
        inputs = {
            ModalityType.VISION: data.load_and_transform_vision_data(target_image_paths, device),
        }
        with torch.no_grad():
            embeddings2 = model(inputs)
        current_simility = source_embeddings[ModalityType.VISION] @ embeddings2[ModalityType.VISION].T
        if max_simility < current_simility:
            max_simility = current_simility
            max_simility_path = file_path
    print(max_simility, max_simility_path)
    return max_simility_path

if __name__ == "__main__":
  with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
  video2img(config)

  folder_path = config['VIDEO_FRAME_DIR']
  file_list = os.listdir(folder_path)
  url = config['STABLE_DIFFUSION']['URL']
  option_img2img(url)

  for file_name in file_list:
      file_path = os.path.join(folder_path, file_name)
      if os.path.isfile(file_path) and file_name.lower().endswith((".png", ".jpg", ".jpeg")):
          im = Image.open(file_path)
          img2img(config, im, url)

