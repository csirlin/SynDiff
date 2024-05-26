# some initial testing to see how the loaded data should be formatted
from dataset import *

data = LoadDataSet('SynDiff_sample_data/data_train_T1.mat')

print(type(data))
print(data.shape)

min_num = 100
max_num = -100

for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        for k in range(data.shape[2]):
            for l in range(data.shape[3]):
                min_num = min(min_num, data[i][j][k][l])
                max_num = max(max_num, data[i][j][k][l])

print(min_num, max_num)