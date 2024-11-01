pip install -q datasets transformers
pip install -q evaluate timm albumentations
python3 detr_test.py --test_path $1 --output_path $2 --model_path ./model