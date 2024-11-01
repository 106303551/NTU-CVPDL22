## 安裝

請先執行以下命令，假設root在hw3_r11944050:
cd O2net/models/ops
sh ./make.sh
潛在問題:1.路徑有中文時ninja會報錯。2.路徑太長ninja會報錯。

## 額外安裝選項
如果執行有error，透過以下方法解決。

我使用的cuda版本為11.7。如果有報錯需要重新安裝並安裝相對應版本的cuDNN。

需要安裝MSVC，我是透過安裝visual studio 2019才安裝成功。
下載:Visual Studio Community 2019 (version 16.11)
https://my.visualstudio.com/Downloads?q=visual%20studio%202019&wt.mc_id=o~msft~vscom~older-downloads
選擇C++桌面開發及python開發進行安裝。
需要加入path至environment variable
EX:C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\bin\Hostx86\x64

如果需要另外安裝對應版本的torchvision，請至requirements.txt開啟。

安裝mmcv(可能不需要)有報錯以下訊息才需要安裝。ImportError: DLL load failed while importing MultiScaleDeformableAttention: 找不到指定的程序。 

git clone https://github.com/open-mmlab/mmcv 
cd mmcv
pip install -r requirements.txt
python setup.py build_ext
python setup.py develop
以上如果安裝失敗，請至requirements.txt開啟。

預設資料夾內的格式是如同作業給的一樣

EX:bash hw3_train.sh "O2net/data/train_dir/" "O2net/data/val_dir/" "best_model.pth" "best_fog_model.pth"
O2net/data/train_dir/ 裡面是 fog及org，然後分別有train及val，annotation也是放在O2net/data/train_dir/fog/及O2net/data/train_dir/org/

如果不是的話，請到O2net/datasets/DA_coco.py build_city2foggy_cocostyle_source及build_city2foggy_cocostyle，前者對應到source train 後者對應到target train。
test部分也是對應到build_city2foggy_cocostyle。
