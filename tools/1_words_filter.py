import json
import csv
import random
import nltk.stem as ns


class WordFilter:

    def __init__(self, file_path):
        self.json_file = json.load(open(file_path))
        self.rows_rel = []
        self.rel_pair = set()
        self.nodeset = set()
        self.links_dict = dict()
        self.nodes_dict = dict()
        self.nodes = []
        self.links = []
        self.node_change_map = dict()
        self.node_type_dict = dict()
        self.cate_map = {
            'ROCK': 0,
            'TECT': 1,
            'ALTE': 2,
            'PHYS': 3,
            'CHEM': 4,
            'CHRO': 5,
            'MINE': 6,
            'DEPO': 7,
            'DEEP': 8,
            'ELEM': 9
        }
        self.category = [
            {'name': 'ROCK'},
            {'name': 'TECT'},
            {'name': 'ALTE'},
            {'name': 'PHYS'},
            {'name': 'CHEM'},
            {'name': 'CHRO'},
            {'name': 'MINE'},
            {'name': 'DEPO'},
            {'name': 'DEEP'},
            {'name': 'ELEM'},
        ]

    @staticmethod
    def data_filter(name):
        """
        进行一些实体节点的过滤，保证同义节点均合并在一起
        主要去除名词大小写，单复数，时态
        """

        # 解决单复数
        # print(name)
        words = name.split()
        lemmatizer = ns.WordNetLemmatizer()
        for i in range(len(words)):
            words[i] = lemmatizer.lemmatize(words[i], pos='n')
            # words[i] = lemmatizer.lemmatize(words[i], pos='v')
            # words[i] = lemmatizer.lemmatize(words[i], pos='a')  # 形容词
            # words[i] = lemmatizer.lemmatize(words[i], pos='r')  # 副词
        name1 = ' '.join(words)
        # print(name1)
        # 解决首字母大小写
        name1 = name1.capitalize()
        # todo 后续这里用一个changeMap 来代替多个if
        # if name1 == 'Adakites':
        #     name1 = 'Adakite'
        return name1

    def data_joiner(self, node):
        """
        对不同类型同名实体进行归并
        """
        if node['name'] not in self.node_type_dict:
            self.node_type_dict[node['name']] = [{'type': node['type'], 'num': 1}]
        else:
            have = False
            for item in self.node_type_dict[node['name']]:
                if item['type'] == node['type']:
                    have = True
                    item['num'] += 1
                    break
            if not have:
                self.node_type_dict[node['name']].append({'type': node['type'], 'num': 1})

    def gen_echart_data(self):
        # todo 检查这一部分代码，进行一下 check，因为很容易出错
        for data in self.json_file:  # 这里去做一个过滤后数据的生成，添加一些echart中要用到的参数。
            data['h']['name'] = self.data_filter(data['h']['name']) # 替换成正确的名称和类型
            data['t']['name'] = self.data_filter(data['t']['name'])
            data['h']['type'] = data['h']['type'].split('_')[-1]
            data['t']['type'] = data['t']['type'].split('_')[-1]
            self.data_joiner(data['h'])  # 统计同名不同类实体
            self.data_joiner(data['t'])

        for key, values in self.node_type_dict.items():  # 对于每一个实体名称 例如 Cu
            max_num_type = ''
            max_num = -1
            all_num = 0
            for node_type in values:  # 对于Cu出现的所有类
                all_num += node_type['num']
                if node_type['num'] > max_num:
                    max_num = node_type['num']
                    max_num_type = node_type['type']
            pre = key + '@@@'
            for node_type in values:
                self.node_change_map[pre + node_type['type']] = pre + max_num_type

        for data in self.json_file:
            name1 = data['h']['name']
            type1 = data['h']['type']
            name2 = data['t']['name']
            type2 = data['t']['type']
            new1 = self.node_change_map[name1 + '@@@' + type1]
            new2 = self.node_change_map[name2 + '@@@' + type2]
            data['h']['type'] = new1.split('@@@')[-1]
            data['t']['type'] = new2.split('@@@')[-1]  # 到此为止类型被更换完成了
            self.rows_rel.append(data)
            node1 = (data['h']['name'], data['h']['type'])
            node2 = (data['t']['name'], data['t']['type'])
            self.nodeset.add(node1)
            self.nodeset.add(node2)

        counter = 0
        for item in self.nodeset:  # 构造初始的node字典
            node = {
                'name': item[0],
                'category': self.cate_map[item[1]],
                'symbolSize': 10,
                'id': str(counter),
                'x': random.random()*1200,
                'y': random.random()*800,
                'value': item[1]
            }
            counter += 1
            self.nodes_dict[item[0] + '@@@' + item[1]] = node
            # print(item[0] + '@@@' + item[1])

        for data in self.rows_rel:  # 对关系中出现的所有节点进行计算个数
            a = data['h']['name'] + '@@@' + data['h']['type'].split('_')[-1]
            b = data['t']['name'] + '@@@' + data['t']['type'].split('_')[-1]
            self.nodes_dict[a]['symbolSize'] += 1
            self.nodes_dict[b]['symbolSize'] += 1
            link = {
                'source': self.nodes_dict[a]['id'],
                'target': self.nodes_dict[b]['id'],
                'value': data['relation'],
                'lineStyle': {
                    'width': 1
                },
                'label': {
                    'formatter': '{c}'
                }
            }
            if link['source'] + '@@@' + link['target'] + '@@@' + link['value'] not in self.links_dict:  # 对重复的关系提高线的宽度
                self.links_dict[link['source'] + '@@@' + link['target'] + '@@@' + link['value']] = link
            else:
                self.links_dict[link['source'] + '@@@' + link['target'] + '@@@' + link['value']]['lineStyle']['width'] += 2

        for key, value in self.nodes_dict.items():
            self.nodes.append(value)
        for key, value in self.links_dict.items():
            self.links.append(value)

        echart_data = {
            'nodes': self.nodes,
            'links': self.links,
            'categories': self.category
        }
        # rel_pair.add((data['h']['name'], data['t']['name']))

        with open('./检查用/echart_use_data.json', 'w', encoding='utf-8') as f:
            json.dump(echart_data, f)
        with open('./检查用/relation_filtered.json', 'w', encoding='utf-8') as f:
            json.dump(self.rows_rel, f)

    def save_ins_dict(self):
        """
        将所有的实体全部保存下来用来，检查去重
        """
        header = ['ins', 'type']
        res = []
        for item in self.nodeset:
            res.append(item)
        with open('./检查用/echart_ins_set.csv', 'w', encoding='utf-8', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(header)
            f_csv.writerows(res)


if __name__ == '__main__':
    a = WordFilter('./检查用/neo4j_use_relation.json')
    # a = WordFilter('./out_data/predict_result.json')
    a.gen_echart_data()
    a.save_ins_dict()
