pip install -q datasets transformers
pip install -q evaluate timm albumentations
python3 detr_train.py --input_path $1 --valid_path $2