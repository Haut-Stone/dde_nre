"""
不添加 attention 机制的普通 bert 有监督学习
效果非常的显著！！达到了 60% 的
"""

import torch
import numpy as np
import json
import opennre
from opennre import encoder, model, framework
import sys
import os
import argparse
import logging
import random

use_gpu = torch.cuda.is_available()  # 查看是否可用 GPU
print(torch.version.cuda)
print(use_gpu)


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


parser = argparse.ArgumentParser()
parser.add_argument('--pretrain_path', default='bert-base-uncased',  # 默认使用最多的那个不分大小写的 bert huggingface 的
                    help='Pre-trained ckpt path / model name (hugginface)')
parser.add_argument('--ckpt', default='',  # 检查点名称
                    help='Checkpoint name')
parser.add_argument('--pooler', default='entity', choices=['cls', 'entity'],
                    help='Sentence representation pooler')
parser.add_argument('--only_test', action='store_true',
                    help='Only run test')
parser.add_argument('--mask_entity', action='store_true',
                    help='Mask entity mentions')

# Data
parser.add_argument('--metric', default='micro_f1', choices=['micro_f1', 'acc'],
                    help='Metric for picking up best checkpoint')
parser.add_argument('--dataset', default='none', choices=['none', 'semeval', 'wiki80', 'tacred', 'dde'],
                    help='Dataset. If not none, the following args can be ignored')
parser.add_argument('--train_file', default='', type=str,
                    help='Training data file')
parser.add_argument('--val_file', default='', type=str,
                    help='Validation data file')
parser.add_argument('--test_file', default='', type=str,
                    help='Test data file')
parser.add_argument('--rel2id_file', default='', type=str,
                    help='Relation to ID file')

# Hyper-parameters
parser.add_argument('--batch_size', default=60, type=int,  # 这里原始的值是64显卡吃不下
                    help='Batch size')
parser.add_argument('--lr', default=2e-5, type=float,
                    help='Learning rate')
parser.add_argument('--max_length', default=128, type=int,
                    help='Maximum sentence length')
parser.add_argument('--max_epoch', default=10, type=int,  # 默认是 3
                    help='Max number of training epochs')

# Seed
parser.add_argument('--seed', default=42, type=int,
                    help='Seed')

args = parser.parse_args()

# Set random seed
set_seed(args.seed)

# 一些设置，
root_path = '..'
sys.path.append(root_path)
if not os.path.exists('ckpt'):
    os.mkdir('ckpt')
if len(args.ckpt) == 0:
    args.ckpt = '{}_{}_{}'.format(args.dataset, args.pretrain_path, args.pooler)
ckpt = 'ckpt/{}.pth.tar'.format(args.ckpt)

if args.dataset != 'none':
    args.train_file = os.path.join(root_path, 'data', args.dataset, '{}_train.txt'.format(args.dataset))
    args.val_file = os.path.join(root_path, 'data', args.dataset, '{}_val.txt'.format(args.dataset))
    args.test_file = os.path.join(root_path, 'data', args.dataset, '{}_test.txt'.format(args.dataset))
    if not os.path.exists(args.test_file):
        logging.warn("Test file {} does not exist! Use val file instead".format(args.test_file))
        args.test_file = args.val_file
    args.rel2id_file = os.path.join(root_path, 'data', args.dataset, '{}_rel2id.json'.format(args.dataset))
    if args.dataset == 'wiki80':
        args.metric = 'acc'
    else:
        args.metric = 'micro_f1'
else:
    if not (os.path.exists(args.train_file) and os.path.exists(args.val_file) and os.path.exists(
            args.test_file) and os.path.exists(args.rel2id_file)):
        raise Exception(
            '--train_file, --val_file, --test_file and --rel2id_file are not specified or files do not exist. Or specify --dataset')

logging.info('Arguments:')
for arg in vars(args):
    logging.info('{}: {}'.format(arg, getattr(args, arg)))

rel2id = json.load(open(args.rel2id_file))

# Define the sentence encoder
if args.pooler == 'entity':
    sentence_encoder = opennre.encoder.BERTEntityEncoder(
        max_length=args.max_length,
        pretrain_path=args.pretrain_path,
        mask_entity=args.mask_entity
    )
elif args.pooler == 'cls':
    sentence_encoder = opennre.encoder.BERTEncoder(
        max_length=args.max_length,
        pretrain_path=args.pretrain_path,
        mask_entity=args.mask_entity
    )
else:
    raise NotImplementedError

# Define the model
model = opennre.model.SoftmaxNN(sentence_encoder, len(rel2id), rel2id)

# Define the whole training framework
framework = opennre.framework.SentenceRE(
    train_path=args.train_file,
    val_path=args.val_file,
    test_path=args.test_file,
    model=model,
    ckpt=ckpt,
    batch_size=args.batch_size,
    max_epoch=args.max_epoch,
    lr=args.lr,
    opt='adamw'
)

# Train the model
if not args.only_test:
    framework.train_model('micro_f1')

# Test
framework.load_state_dict(torch.load(ckpt)['state_dict'])
result = framework.eval_model(framework.test_loader)

# Print the result
logging.info('Test set results:')
logging.info('Accuracy: {}'.format(result['acc']))
logging.info('Micro precision: {}'.format(result['micro_p']))
logging.info('Micro recall: {}'.format(result['micro_r']))
logging.info('Micro F1: {}'.format(result['micro_f1']))
