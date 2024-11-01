#  video_style_transfer

## Overview

![overview1](https://github.com/jeff3071/video_style_transfer/assets/17506757/fd06e3f9-c5db-4c47-a2ed-aa52d3ef6138)
![overview2](https://github.com/jeff3071/video_style_transfer/assets/17506757/67018b37-6c05-42aa-b0be-8e9d07461d9f)

## video2img

```python
python video2img.py 
  --video <path_to_video>
```

## img2img

To run this program, you need to install [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) first. Modify the COMMANDLINE_ARGS of webui-user.bat. 
`set  COMMANDLINE_ARGS=--enable-insecure-extension-access --xformers --no-half-vae --api`.

We use [OrangeMixs](https://huggingface.co/WarriorMama777/OrangeMixs/blob/main/Models/AbyssOrangeMix3/AOM3A3_orangemixs.safetensors) and [VAE](https://huggingface.co/WarriorMama777/OrangeMixs/blob/main/VAEs/orangemix.vae.pt) to transfer keyframe's style. To make the image consistent, we use [Controlnet](https://huggingface.co/lllyasviel/ControlNet/tree/main/models). 


```python
python img2img.py 
  --source_folder <path_to_source_images_folder> 
  --pose <path_to_pose_image> 
  --prompt <prompt_for_img2img> 
  --n_prompt <negative_prompt_for_img2img>
```

## imagebind

We use [imagebind](https://github.com/facebookresearch/ImageBind) to choose the most similar image as final keyframe.

```python
python imagebind.py 
  --target_image <path_to_target_image> --source_folder <path_to_source_folder>
```
