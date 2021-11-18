import json
import csv

json_file = json.load(open('./检查用/relation_filtered.json'))

rows_rel = []
rows_ins = []

inss = set()

for data in json_file:
    line_rel = [data['h']['name'], data['h']['type'], data['t']['name'], data['t']['type'], data['relation'], data['project'], data['example']]
    rows_rel.append(line_rel)
    inss.add((data['h']['name'], data['h']['type']))
    inss.add((data['t']['name'], data['t']['type']))

for ins in inss:
    line_ins = [ins[0], ins[1]]
    rows_ins.append(line_ins)

headers = ['ins1', 'type1', 'ins2', 'type2', 'relation', 'project', 'example']
headers2 = ['ins', 'type']

with open('./neo4j_data/relation.csv', 'w', encoding='utf-8', newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows_rel)
with open('./neo4j_data/instance.csv', 'w', encoding='utf-8', newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers2)
    f_csv.writerows(rows_ins)
