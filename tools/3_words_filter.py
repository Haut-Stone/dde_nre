import json
import csv


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
    # name1 = name1.replace('', '')
    # name1 = name1.replace('', '')
    # name1 = name1.replace('', '')
    # name1 = name1.replace('', '')
    # name1 = name1.replace('', '')
    # name1 = name1.replace('', '')
    return name1


for data in json_file:
    data['h']['name'] = data_filter(data['h']['name'])
    data['t']['name'] = data_filter(data['t']['name'])
    rows_rel.append(data)
    rel_pair.add((data['h']['name'], data['t']['name']))


print(len(rel_pair))
with open('./检查用/relation_filtered.json', 'w', encoding='utf-8') as f:
    json.dump(rows_rel, f)

