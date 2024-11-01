import data
import torch
from models import imagebind_model
from models.imagebind_model import ModalityType
from PIL import Image
import os
import argparse
import shutil

def delete_files_in_folder(folder_path):
    # 取得資料夾內所有檔案列表
    file_list = os.listdir(folder_path)
    
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)  # 取得檔案的完整路徑
        if os.path.isfile(file_path):  # 確認該路徑是檔案而非子資料夾
            os.remove(file_path)  # 刪除檔案

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



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_image', type=str, default='', help='target_image')
    parser.add_argument('--source_folder', type=str, default='', help='source_folder')
    parser.add_argument('--output_folder', type=str, default='destination', help='output_folder')
    opt = parser.parse_args()
    source_folder=opt.source_folder
    output_folder=opt.output_folder
    images=opt.target_image
    delete_files_in_folder(output_folder)
    for image in sorted(os.listdir(images)):
        image_path=os.path.join(images, image)
        if os.path.isfile(image_path):
           target_name = os.path.basename(image_path)
           image_name = os.path.splitext(target_name)[0]
           target_folder=os.path.join(source_folder, image_name)
           print(image_path)
           print(target_folder)
           target=imagebind(image_path, target_folder)           
           shutil.move(target,output_folder)
           
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        if os.path.isfile(file_path):
            file_name, file_ext = os.path.splitext(filename)
            if len(file_name) > 3:
                new_file_name = file_name[:-4] + file_ext
                new_file_path = os.path.join(output_folder, new_file_name)
                os.rename(file_path, new_file_path)
