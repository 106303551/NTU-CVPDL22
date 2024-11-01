cd yolov7
git checkout fix/problems_associated_with_the_latest_versions_of_pytorch_and_numpy
pip install -r requirements.txt
cd ..
wget https://www.dropbox.com/s/7v9xtymf0kso2ke/best.pt?dl=1 -O ./model.pt