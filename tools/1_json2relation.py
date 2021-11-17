"""
重要的数据转换代码，用来将从doccano数据库中提取出的标注数据转换为模型直接可用的数据，本代码实现两个功能
1. 整理关系数据
TODO 2. 去除停用词
"""

import json

json_data = json.load(open('./raw_data/relations.json', encoding='utf-8'))

res = []
res2 = []


def pos_calculator(sen, ins_start, ins_end):
    """
    计算单词位置
    """
    pos_tag = [-1 for _ in range(len(sen))]
    tag = 0
    flag = True  # 用来记录遇到空格后是否再遇到单词，来处理句子中出现多于一个空格的情况：例如( t )  ( +1 to +12 )
    for i in range(len(sen)):
        if sen[i] == ' ' and flag:
            tag += 1
            flag = False
        else:
            pos_tag[i] = tag
            flag = True

    # 对实体词组前后空格进行修正，去掉标注时多勾画的前后空格
    for i in range(ins_start, ins_end):
        if sen[i] == ' ':
            ins_start += 1
        else:
            break
    for i in range(ins_end-1, ins_start-1, -1):
        if sen[i] == ' ':
            ins_end -= 1
        else:
            break

    return [pos_tag[ins_start], pos_tag[ins_end-1]+1]


for data in json_data:
    ori_sen = data['原文']
    token = ori_sen.split()
    instance1_ori = ori_sen[data['实体 1 起始字符位置']:data['实体 1 结束字符位置']]  # 检查用的对照组
    instance2_ori = ori_sen[data['实体 2 起始字符位置']:data['实体 2 结束字符位置']]
    pos1 = pos_calculator(ori_sen, data['实体 1 起始字符位置'], data['实体 1 结束字符位置'])
    pos2 = pos_calculator(ori_sen, data['实体 2 起始字符位置'], data['实体 2 结束字符位置'])
    ins1 = ' '.join(token[pos1[0]:pos1[1]])
    ins2 = ' '.join(token[pos2[0]:pos2[1]])
    rel = data['关系名称']
    relation = {
        'token': token,
        'h': {
            'name': ins1,
            'pos': pos1
        },
        't': {
            'name': ins2,
            'pos': pos2
        },
        'relation': rel
    }
    relation2 = {
        'token': token,
        'h': {
            'name': ins1,
            'pos': pos1,
            'type': data['实体 1 类型']
        },
        't': {
            'name': ins2,
            'pos': pos2,
            'type': data['实体 2 类型']
        },
        'relation': rel,
        'project': data['项目 名称'],
        'example': data['原文']
    }
    res.append(relation)  # 模型用的数据
    res2.append(relation2)  # 检查用的数据


with open('./模型用/relation.txt', 'w', encoding='utf-8') as f:
    for re in res:
        f.write(str(re))
        f.write('\n')
    f.close()
with open('./检查用/relation.json', 'w', encoding='utf-8') as f:
    json.dump(res2, f)
    f.close()

