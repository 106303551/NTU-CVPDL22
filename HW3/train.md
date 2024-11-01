## command
bash hw3_train.sh $1 $2 $3

## explantation

$1:training images directory(eg data/train_dir/)

$2:validation images directory(eg data/val_dir/)

$3:path of best trained model checkpoint of source(eg best_model.pth)

$4:path of best trained model checkpoint of target(eg best_fog_model.pth)

預設資料夾內的格式是如同作業給的一樣

EX:bash hw3_train.sh "O2net/data/train_dir/" "O2net/data/val_dir/" "best_model.pth" "best_fog_model.pth"
O2net/data/train_dir/ 裡面是 fog及org，然後分別有train及val，annotation也是放在O2net/data/train_dir/fog/及O2net/data/train_dir/org/

如果不是的話，請到O2net/datasets/DA_coco.py build_city2foggy_cocostyle_source及build_city2foggy_cocostyle，前者對應到source train 後者對應到target train。
test部分也是對應到build_city2foggy_cocostyle。