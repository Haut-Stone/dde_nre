import json
import csv
import random
import nltk.stem as ns


class WordFilter:

    def __init__(self):
        self.json_file = json.load(open('./检查用/neo4j_use_relation.json'))
        self.rows_rel = []
        self.rel_pair = set()
        self.nodeset = set()
        self.links_dict = dict()
        self.nodes_dict = dict()
        self.nodes = []
        self.links = []
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
        print(name)
        words = name.split()
        lemmatizer = ns.WordNetLemmatizer()
        for i in range(len(words)):
            words[i] = lemmatizer.lemmatize(words[i], pos='n')
            words[i] = lemmatizer.lemmatize(words[i], pos='v')
            # words[i] = lemmatizer.lemmatize(words[i], pos='a')  # 形容词
            # words[i] = lemmatizer.lemmatize(words[i], pos='r')  # 副词
        name1 = ' '.join(words)
        print(name1)

        # 解决首字母大小写
        name1 = name1.capitalize()
        return name1

    def gen_echart_data(self):
        for data in self.json_file:  # 这里去做一个过滤后数据的生成，添加一些echart中要用到的参数。
            data['h']['name'] = self.data_filter(data['h']['name'])
            data['t']['name'] = self.data_filter(data['t']['name'])
            self.rows_rel.append(data)

            node1 = (data['h']['name'], data['h']['type'].split('_')[-1])
            node2 = (data['t']['name'], data['t']['type'].split('_')[-1])
            self.nodeset.add(node1)
            self.nodeset.add(node2)

        counter = 0
        for item in self.nodeset:
            node = {
                'name': item[0],
                'category': self.cate_map[item[1]],
                'symbolSize': 10,
                'id': str(counter),
                'x': random.random()*1200,
                'y': random.random()*800,
                'value': random.random()*100
            }
            counter += 1
            self.nodes_dict[item[0] + '@@@' + item[1]] = node
            # print(item[0] + '@@@' + item[1])

        for data in self.rows_rel:
            a = data['h']['name'] + '@@@' + data['h']['type'].split('_')[-1]
            b = data['t']['name'] + '@@@' + data['t']['type'].split('_')[-1]

            if self.nodes_dict[a]['symbolSize'] <= 40:  # 对重复的节点提高节点的大小
                self.nodes_dict[a]['symbolSize'] += 3
            if self.nodes_dict[b]['symbolSize'] <= 40:
                self.nodes_dict[b]['symbolSize'] += 3

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
                self.links_dict[link['source'] + '@@@' + link['target'] + '@@@' + link['value']]['lineStyle']['width'] += 1

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
    a = WordFilter()
    # a.data_filter('is')
    a.gen_echart_data()
    a.save_ins_dict()
