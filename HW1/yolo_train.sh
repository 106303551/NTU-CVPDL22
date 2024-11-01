python3 yolov7_train_preprocess.py --input_path $1 --valid_path $2
cd yolov7
git checkout fix/problems_associated_with_the_latest_versions_of_pytorch_and_numpy
pip install -r requirements.txt
wget https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7_training.pt
python3 train.py --batch 8 --epochs 100 --data ./c_datasets/data.yaml --weights 'yolov7_training.pt' --device 0