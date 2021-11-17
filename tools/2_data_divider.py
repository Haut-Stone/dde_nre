import json

data_file = open('模型用/relation.txt', encoding='utf-8')
dde_test_file = open('../data/dde/dde_test.txt', 'w', encoding='utf-8')
dde_train_file = open('../data/dde/dde_train.txt', 'w', encoding='utf-8')
dde_val_file = open('../data/dde/dde_val.txt', 'w', encoding='utf-8')

LINES = 4145
counter = 0

for i in range(LINES):
    data = data_file.readline()
    counter = (counter + 1) % 10  # 8:1:1 划分
    if counter < 8:
        dde_train_file.write(data)
    elif counter < 9:
        dde_test_file.write(data)
    else:
        dde_val_file.write(data)

data_file.close()
dde_val_file.close()
dde_test_file.close()
dde_train_file.close()