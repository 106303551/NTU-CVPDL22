python ./O2net/data_preprocess.py --img_path $1 --save_file public_test_data.json #ok
python ./O2net/DA_main.py --test --coco_path $1 --result_dir $2 --resume ./O2net/$3.pth --checkpoint ./O2net/$3.pth #ok

