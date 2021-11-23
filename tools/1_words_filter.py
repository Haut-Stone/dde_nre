import json
import csv
import random

json_file = json.load(open('./检查用/relation.json'))

rows_rel = []
rel_pair = set()


def data_filter(name):
    name1 = name.replace('Apatite', 'apatite')
    name1 = name1.replace('Apa - tites', 'apatite')
    name1 = name1.replace('Apatites', 'apatite')
    name1 = name1.replace('apatites', 'apatite')
    name1 = name1.replace('apa - tites', 'apatite')
    name1 = name1.replace('MORs', 'MOR')
    name1 = name1.replace('PCD forma - tion', 'PCD formation')
    name1 = name1.replace('PCDs', 'PCD')
    name1 = name1.replace('REEs', 'REE')
    name1 = name1.replace('W skarns', 'W skarn')
    name1 = name1.replace('magmatic arcs', 'magmatic arc')
    name1 = name1.replace('porphy - ries', 'porphyry')
    name1 = name1.replace('porphyries', 'porphyry')
    name1 = name1.replace('High', 'high')
    name1 = name1.replace('Low', 'low')
    name1 = name1.replace('car - bonatites', 'carbonatites')
    name1 = name1.replace('carbon - atites', 'carbonatites')
    name1 = name1.replace('high - est', 'highest')
    name1 = name1.replace('oxy - gen', 'oxygen')
    name1 = name1.replace('por - phyry', 'porphyry')
    name1 = name1.replace('unmineral - ized', 'unmineralized')
    name1 = name1.replace('low - est', 'lowest')
    # name1 = name1.replace('', '')
    return name1


nodeset = set()
links_dict = dict()
nodes_dict = dict()
nodes = []
links = []
cate_map = {
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
category = [
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

for data in json_file:  # 这里去做一个过滤后数据的生成，添加一些echart中要用到的参数。
    data['h']['name'] = data_filter(data['h']['name'])
    data['t']['name'] = data_filter(data['t']['name'])
    rows_rel.append(data)

    node1 = (data['h']['name'], data['h']['type'])
    node2 = (data['t']['name'], data['t']['type'])
    nodeset.add(node1)
    nodeset.add(node2)

counter = 0
for item in nodeset:
    node = {
        'name': item[0],
        'category': cate_map[item[1]],
        'symbolSize': 10,
        'id': str(counter),
        'x': random.random()*1200,
        'y': random.random()*800,
        'value': random.random()*100
    }
    counter += 1
    nodes_dict[item[0] + '@@@' + item[1]] = node
    print(item[0] + '@@@' + item[1])

for data in rows_rel:
    a = data['h']['name'] + '@@@' + data['h']['type']
    b = data['t']['name'] + '@@@' + data['t']['type']

    if nodes_dict[a]['symbolSize'] <= 40:  # 对重复的节点提高节点的大小
        nodes_dict[a]['symbolSize'] += 3
    if nodes_dict[b]['symbolSize'] <= 40:
        nodes_dict[b]['symbolSize'] += 3

    link = {
        'source': nodes_dict[a]['id'],
        'target': nodes_dict[b]['id'],
        'value': data['relation'],
        'lineStyle': {
            'width': 1
        },
        'label': {
            'formatter': '{c}'
        }
    }
    if link['source'] + '@@@' + link['target'] + '@@@' + link['value'] not in links_dict:  # 对重复的关系提高线的宽度
        links_dict[link['source'] + '@@@' + link['target'] + '@@@' + link['value']] = link
    else:
        links_dict[link['source'] + '@@@' + link['target'] + '@@@' + link['value']]['lineStyle']['width'] += 1

for key, value in nodes_dict.items():
    nodes.append(value)
for key, value in links_dict.items():
    links.append(value)

echart_data = {
    'nodes': nodes,
    'links': links,
    'categories': category
}
# rel_pair.add((data['h']['name'], data['t']['name']))

# print(len(rel_pair))
with open('./检查用/echart_use_data.json', 'w', encoding='utf-8') as f:
    json.dump(echart_data, f)
with open('./检查用/relation_filtered.json', 'w', encoding='utf-8') as f:
    json.dump(rows_rel, f)

