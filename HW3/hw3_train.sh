python ./O2net/main.py --train_dir $1 --valid_dir $2 --best_path $3 --num_workers 4 #ok 
python ./O2net/DA_main.py --train_dir $1 --valid_dir $2 --checkpoint $3 --best_path $4  --num_workers 4