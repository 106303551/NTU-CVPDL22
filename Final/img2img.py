import requests
import io
import os
import cv2
import base64
import argparse
from PIL import Image, PngImagePlugin
from base64 import b64encode

url = "http://127.0.0.1:7860"


def option_img2img():
    option_payload = {
    "do_not_add_watermark": True,
    "sd_model_checkpoint": "2D\\abyssorangemix3AOM3_aom3a1b.safetensors",
    "sd_vae":"orangemix.vae.pt"
    }

    requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)

def img2img(prompt, negative_prompt, im):
   
    img_bytes = io.BytesIO()
    im.save(img_bytes, format='PNG')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # retval, buffer = cv2.imencode('.jpg', im)
    # img_base64 = b64encode(buffer).decode("utf-8")
    

    file_name_without_extension = os.path.splitext(file_name)[0]
    os.makedirs("output/"+file_name_without_extension, exist_ok=True)
    img2img_payload = {
        "init_images": [img_base64],
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "denoising_strength": 0.7,
        "width": 512,
        "height": 768,
        "cfg_scale": 7,         
        # "seed_resize_from_w": 768,
        # "seed_resize_from_h": 512,
        "sampler_name": "DPM++ 2M Karras",
        "restore_faces": False,
        "steps": 25,
        "batch_size":8,
        "n_iter":1,
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    
                    # {
                    #     "input_image": img_base64,
                    #     "module": "normal_bae",
                    #     "model": "control_v11p_sd15_normalbae",
                    #     "resize_mode": "Crop and Resize",
                    #     "pixel_perfect":True,
                    #     "control_mode": "My prompt is more important",
                    # },
                    {
                        "input_image": img_base64,
                        "module":"canny",
                        "model": "control_v11p_sd15_canny",
                        "resize_mode": "Crop and Resize",
                        "pixel_perfect":True,
                        "weight":1.7,
                        "control_mode": "My prompt is more important",
                    },
                    {
                        "input_image": img_base64,
                        "module": "t2ia_color_grid",
                        "model": "t2iadapter_color_sd14v1",
                        "resize_mode": "Crop and Resize",
                        # "pixel_perfect":True,
                        # "control_mode": "My prompt is more important",
                    }
            
                ]
            }
        }        
    }

    img2img_response = requests.post(url=f'{url}/sdapi/v1/img2img', json=img2img_payload)

    r = img2img_response.json()
    j=1
    for i in r['images'][:-1]:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        filename ="output/"+file_name_without_extension+"/"+file_name_without_extension+"--"+str(j).zfill(2)+".png"
        image.save(filename, pnginfo=pnginfo)
        j=j+1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_folder", type=str, default="./source")
    # parser.add_argument("--pose", type=str, default="./pose/lin.jpg")
    parser.add_argument("--prompt", type=str, default="highres, hdr, (masterpiece:1.2), (best quality:1.2),illustration,perfect eyes,perfect face,<lora:kakuya:0.8:FACE>,shinomiya_kaguya, 1girl,black_hair, solo, folded_ponytail, hair_ribbon, red_eyes, sidelocks, parted_bangs,(simple background),")
    parser.add_argument("--n_prompt", type=str, default="(bad_prompt_version2:0.7), ng_deepnegative_v1_75t, lowres, bad anatomy, bad hands, bad-hands-5, text, error, mutilated hands, missing fingers, extra fingers, extra arms, deformed, extra digit, fewer digits, cropped, (low quality, worst quality:1.4), normal quality, jpeg artifacts, signature, watermark, username, blurry, monochrome, ")
    args = parser.parse_args()#"highres, hdr, (masterpiece:1.2), (best quality:1.2),illustration,perfect eyes,perfect face,<lora:kakuya:0.7:FACE>,shinomiya_kaguya, 1girl,black_hair, solo, folded_ponytail, hair_ribbon, red_eyes, sidelocks, parted_bangs,(simple background),"
    folder_path = args.source_folder
    prompt=args.prompt
    negative_prompt=args.n_prompt
    # pose_path=args.pose
    # pose = cv2.imread(pose_path)[:, :, ::-1]
    file_list = os.listdir(folder_path)    
    option_img2img()
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            im = Image.open(file_path)
            img2img(prompt, negative_prompt, im)
            # 取得圖片檔名（不含副檔名）


