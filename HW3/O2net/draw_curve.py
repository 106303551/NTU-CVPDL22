import matplotlib.pyplot as plt

# 讀取txt文件中的資料
name='source_fog_valid_map50'
with open(name+'.txt', 'r') as file:
    lines = file.readlines()
data=[]
epoch=[]
count=4
for line in lines:
    line=line.split(',')
    map=line[1]
    data.append(float(map))
    epoch.append(count)
    count+=10
# 提取資料


# 繪製資料
plt.plot(epoch,data)
plt.scatter(epoch,data, marker='o', color='blue', label='資料點')
plt.xlabel('epoch')
plt.ylabel('map50')
plt.ylim(0,1)
plt.title('source_fog_valid_map50')
plt.savefig(name+'.png')
plt.show()
