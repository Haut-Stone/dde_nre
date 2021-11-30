

class DataDivider:

    def __init__(self):
        pass

    @staticmethod
    def divide_rel_data(wide):
        data_file = open('raw_data_from_ner/relations.txt', encoding='utf-8')
        dde_test_file = open('../data/dde/dde_test.txt', 'w', encoding='utf-8')
        dde_train_file = open('../data/dde/dde_train.txt', 'w', encoding='utf-8')
        dde_val_file = open('../data/dde/dde_val.txt', 'w', encoding='utf-8')

        counter = 0

        while True:
            data = data_file.readline()
            if not data:
                break
            counter = (counter + 1) % wide  # 8:1:1 划分
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


if __name__ == '__main__':
    DataDivider.divide_rel_data(10)
